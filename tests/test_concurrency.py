import asyncio
from contextlib import AbstractContextManager
from threading import Event, get_ident
from traceback import extract_tb
from types import TracebackType
from typing import Literal

import anyio
import anyio.from_thread
import anyio.to_thread
import httpx
import pytest
from anyio import wait_all_tasks_blocked
from anyio.abc import TaskStatus
from fastapi import Depends, FastAPI
from fastapi.concurrency import contextmanager_in_threadpool

pytestmark = pytest.mark.anyio


class BaseError(BaseException):
    pass


class RecordingContextManager(AbstractContextManager[str]):
    def __init__(
        self,
        *,
        enter_error: BaseException | None = None,
        exit_error: BaseException | None = None,
        suppress: bool = False,
    ) -> None:
        self.enter_error = enter_error
        self.exit_error = exit_error
        self.suppress = suppress
        self.enter_threads: list[int] = []
        self.exit_threads: list[int] = []
        self.exit_args: list[
            tuple[
                type[BaseException] | None, BaseException | None, TracebackType | None
            ]
        ] = []

    def __enter__(self) -> str:
        self.enter_threads.append(get_ident())
        if self.enter_error is not None:
            raise self.enter_error
        return "value"

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.exit_threads.append(get_ident())
        self.exit_args.append((exc_type, exc_value, traceback))
        if self.exit_error is not None:
            raise self.exit_error
        return self.suppress


def assert_exited_in_worker(cm: RecordingContextManager) -> None:
    assert len(cm.exit_threads) == 1
    assert cm.exit_threads[0] != get_ident()


async def test_contextmanager_returns_value_and_exits_in_worker() -> None:
    cm = RecordingContextManager()
    async with contextmanager_in_threadpool(cm) as value:
        assert value == "value"
    assert cm.enter_threads[0] != get_ident()
    assert_exited_in_worker(cm)
    assert cm.exit_args == [(None, None, None)]


@pytest.mark.parametrize("error_type", [ValueError, BaseError])
async def test_failed_enter_does_not_call_exit(
    error_type: type[BaseException],
) -> None:
    error = error_type("entry failed")
    cm = RecordingContextManager(enter_error=error)
    with pytest.raises(error_type) as caught:
        async with contextmanager_in_threadpool(cm):
            pytest.fail("Entry should fail")  # pragma: no cover
    assert caught.value is error
    assert cm.exit_threads == []


@pytest.mark.parametrize("error_type", [ValueError, BaseError])
@pytest.mark.parametrize("suppress", [False, True])
async def test_exit_receives_body_exception(
    error_type: type[BaseException], suppress: bool
) -> None:
    error = error_type("body failed")
    cm = RecordingContextManager(suppress=suppress)

    async def use() -> None:
        async with contextmanager_in_threadpool(cm):
            raise error

    if suppress:
        await use()
    else:
        with pytest.raises(error_type) as caught:
            await use()
        assert caught.value is error
    assert_exited_in_worker(cm)
    exc_type, exc_value, traceback = cm.exit_args[0]
    assert exc_type is error_type
    assert exc_value is error
    assert traceback is not None
    assert extract_tb(traceback)[-1].name == "use"


@pytest.mark.parametrize("body_state", ["success", "exception", "cancelled"])
async def test_cleanup_exception_propagates(body_state: str) -> None:
    error = ValueError("cleanup failed")
    cm = RecordingContextManager(exit_error=error)
    with pytest.raises(ValueError) as caught, anyio.CancelScope() as scope:
        async with contextmanager_in_threadpool(cm):
            if body_state == "exception":
                raise RuntimeError("body failed")
            if body_state == "cancelled":
                scope.cancel()
                await anyio.sleep(0)
    assert caught.value is error
    assert_exited_in_worker(cm)
    if body_state == "exception":
        assert isinstance(error.__context__, RuntimeError)
    elif body_state == "cancelled":
        assert isinstance(error.__context__, anyio.get_cancelled_exc_class())


async def test_cancelled_body_exits_in_worker() -> None:
    cm = RecordingContextManager()
    with anyio.CancelScope() as scope:
        async with contextmanager_in_threadpool(cm):
            scope.cancel()
            await anyio.sleep(0)
    assert scope.cancelled_caught
    assert_exited_in_worker(cm)
    assert isinstance(cm.exit_args[0][1], anyio.get_cancelled_exc_class())


async def test_cancelled_scope_exits_before_next_checkpoint() -> None:
    cm = RecordingContextManager()
    with anyio.CancelScope() as scope:
        async with contextmanager_in_threadpool(cm):
            scope.cancel()
    assert_exited_in_worker(cm)
    assert cm.exit_args == [(None, None, None)]


async def test_cancelled_wait_for_worker_does_not_enter_or_exit() -> None:
    cm = RecordingContextManager()
    limiter = anyio.to_thread.current_default_thread_limiter()
    original_tokens = limiter.total_tokens
    limiter.total_tokens = 1
    finished = anyio.Event()

    async def use(*, task_status: TaskStatus[anyio.CancelScope]) -> None:
        with anyio.CancelScope() as scope:
            task_status.started(scope)
            async with contextmanager_in_threadpool(cm):
                pytest.fail(
                    "No worker capacity should be available"
                )  # pragma: no cover
        finished.set()

    try:
        await limiter.acquire()
        async with anyio.create_task_group() as group:
            try:
                scope = await group.start(use)
                await wait_all_tasks_blocked()
                assert limiter.statistics().tasks_waiting == 1
                scope.cancel()
                with anyio.fail_after(2):
                    await finished.wait()
            finally:
                limiter.release()
    finally:
        limiter.total_tokens = original_tokens
    assert cm.enter_threads == []
    assert cm.exit_threads == []


@pytest.mark.parametrize("cancel_during", ["enter", "exit"])
async def test_cancellation_waits_for_worker_and_cleanup(cancel_during: str) -> None:
    started = anyio.Event()
    release = Event()
    finished = anyio.Event()

    def wait_in_worker() -> None:
        anyio.from_thread.run_sync(started.set)
        assert release.wait(5)

    class BlockingContextManager(RecordingContextManager):
        def __enter__(self) -> str:
            if cancel_during == "enter":
                wait_in_worker()
            return super().__enter__()

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
        ) -> bool:
            if cancel_during == "exit":
                wait_in_worker()
            return super().__exit__(exc_type, exc_value, traceback)

    cm = BlockingContextManager()

    async def use(*, task_status: TaskStatus[anyio.CancelScope]) -> None:
        with anyio.CancelScope() as scope:
            task_status.started(scope)
            async with contextmanager_in_threadpool(cm):
                await anyio.sleep(0)
        finished.set()

    async with anyio.create_task_group() as group:
        try:
            scope = await group.start(use)
            with anyio.fail_after(2):
                await started.wait()
            scope.cancel()
            await wait_all_tasks_blocked()
            assert not finished.is_set()
        finally:
            release.set()
        with anyio.fail_after(2):
            await finished.wait()
    assert_exited_in_worker(cm)


@pytest.mark.parametrize("cancel", [False, True])
async def test_cleanup_does_not_need_default_worker_capacity(cancel: bool) -> None:
    cm = RecordingContextManager()
    limiter = anyio.to_thread.current_default_thread_limiter()
    original_tokens = limiter.total_tokens
    limiter.total_tokens = 1
    entered = anyio.Event()
    capacity_held = anyio.Event()
    release_capacity = anyio.Event()
    finished = anyio.Event()

    async def hold_capacity() -> None:
        await entered.wait()
        async with limiter:
            capacity_held.set()
            await release_capacity.wait()

    async def use() -> None:
        with anyio.CancelScope() as scope:
            async with contextmanager_in_threadpool(cm):
                entered.set()
                await capacity_held.wait()
                if cancel:
                    scope.cancel()
                    await anyio.sleep(0)
        finished.set()

    try:
        async with anyio.create_task_group() as group:
            try:
                group.start_soon(hold_capacity)
                group.start_soon(use)
                with anyio.fail_after(2):
                    await finished.wait()
            finally:
                release_capacity.set()
    finally:
        limiter.total_tokens = original_tokens
    assert_exited_in_worker(cm)


@pytest.mark.parametrize("scope", ["request", "function"])
async def test_cancelled_request_closes_nested_sync_dependencies(
    scope: Literal["request", "function"],
) -> None:
    app = FastAPI()
    outer = RecordingContextManager()
    inner = RecordingContextManager()
    cleanup_order: list[str] = []
    ready = anyio.Event()
    finished = anyio.Event()

    def outer_dependency():
        with outer:
            try:
                yield
            finally:
                cleanup_order.append("outer")

    def inner_dependency(_=Depends(outer_dependency, scope=scope)):
        with inner:
            try:
                yield
            finally:
                cleanup_order.append("inner")

    @app.get("/")
    async def endpoint(_=Depends(inner_dependency, scope=scope)):
        ready.set()
        await anyio.sleep_forever()

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:

        async def request(*, task_status: TaskStatus[anyio.CancelScope]) -> None:
            with anyio.CancelScope() as cancel_scope:
                task_status.started(cancel_scope)
                await client.get("/")
            finished.set()

        async with anyio.create_task_group() as group:
            cancel_scope = await group.start(request)
            with anyio.fail_after(2):
                await ready.wait()
                cancel_scope.cancel()
                await finished.wait()

    assert cleanup_order == ["inner", "outer"]
    assert_exited_in_worker(inner)
    assert_exited_in_worker(outer)


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_asyncio_cancellation_in_body_runs_cleanup(anyio_backend: str) -> None:
    assert anyio_backend == "asyncio"
    cm = RecordingContextManager()
    ready = anyio.Event()

    async def use() -> None:
        async with contextmanager_in_threadpool(cm):
            ready.set()
            await anyio.sleep_forever()

    task = asyncio.create_task(use())
    try:
        with anyio.fail_after(2):
            await ready.wait()
    finally:
        task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert_exited_in_worker(cm)
    assert isinstance(cm.exit_args[0][1], asyncio.CancelledError)
