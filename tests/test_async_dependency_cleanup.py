from collections.abc import AsyncIterator
from contextvars import ContextVar
from pathlib import Path
from typing import Literal

import anyio
import anyio.from_thread
import httpx
import pytest
from anyio import wait_all_tasks_blocked
from anyio.abc import TaskStatus
from fastapi import Depends, FastAPI
from fastapi.responses import Response, StreamingResponse
from starlette.background import BackgroundTask
from starlette.types import Message, Scope

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("scope", ["function", "request"])
@pytest.mark.parametrize("cancel_during", ["endpoint", "cleanup", "before_cleanup"])
async def test_cancellation_waits_for_async_dependency_cleanup(
    scope: Literal["function", "request"], cancel_during: str
) -> None:
    entered = anyio.Event()
    cleanup_started = anyio.Event()
    release_cleanup = anyio.Event()
    finished = anyio.Event()
    events = []
    state: dict[str, anyio.CancelScope] = {}
    app = FastAPI()

    async def dependency() -> AsyncIterator[None]:
        events.append("enter")
        try:
            yield
        finally:
            events.append("cleanup start")
            cleanup_started.set()
            await release_cleanup.wait()
            events.append("cleanup end")

    @app.get("/")
    async def endpoint(_=Depends(dependency, scope=scope)):
        entered.set()
        if cancel_during == "endpoint":
            await anyio.sleep_forever()
        elif cancel_during == "before_cleanup":
            state["scope"].cancel()
        return "ok"

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:

            async def request(*, task_status: TaskStatus[anyio.CancelScope]) -> None:
                with anyio.CancelScope() as cancel:
                    state["scope"] = cancel
                    task_status.started(cancel)
                    await client.get("/")
                finished.set()

            async with anyio.create_task_group() as group:
                cancel = await group.start(request)
                try:
                    if cancel_during == "endpoint":
                        await entered.wait()
                        cancel.cancel()
                    await cleanup_started.wait()
                    if cancel_during == "cleanup":
                        cancel.cancel()
                    await wait_all_tasks_blocked()
                    assert not finished.is_set()
                finally:
                    release_cleanup.set()
                await finished.wait()
    assert events == ["enter", "cleanup start", "cleanup end"]
    assert cancel.cancelled_caught


async def test_dependency_entry_remains_cancellable():
    started, finished = anyio.Event(), anyio.Event()
    events = []
    app = FastAPI()

    async def dependency():
        started.set()
        try:
            await anyio.sleep_forever()
            yield  # pragma: no cover
        finally:
            events.append("entry interrupted")

    @app.get("/")
    async def endpoint(_=Depends(dependency)):
        pytest.fail("Entry should be cancelled")  # pragma: no cover

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:

            async def request(*, task_status):
                with anyio.CancelScope() as cancel:
                    task_status.started(cancel)
                    await client.get("/")
                finished.set()

            async with anyio.create_task_group() as group:
                cancel = await group.start(request)
                await started.wait()
                cancel.cancel()
                await finished.wait()
    assert events == ["entry interrupted"]


@pytest.mark.parametrize("owner_scope", ["function", "request"])
@pytest.mark.parametrize("owner_first", [False, True])
@pytest.mark.parametrize("plain_sync", [False, True])
@pytest.mark.parametrize("cancel", [False, True])
async def test_cancel_scope_dependency_and_mixed_cleanup_order(
    owner_scope: Literal["function", "request"],
    owner_first: bool,
    cancel: bool,
    plain_sync: bool,
):
    events = []
    app = FastAPI()
    other_scope = "request" if owner_scope == "function" else "function"
    external = anyio.CancelScope()

    async def owner():
        with anyio.CancelScope():
            events.append("owner enter")
            try:
                yield
            finally:
                await anyio.sleep(0)
                events.append("owner cleanup")

    async def plain():
        events.append("plain enter")
        try:
            yield
        finally:
            await anyio.sleep(0)
            events.append("plain cleanup")

    def sync_plain():
        events.append("plain enter")
        try:
            yield
        finally:
            anyio.from_thread.run(anyio.sleep, 0)
            events.append("plain cleanup")

    dependencies = [
        Depends(owner, scope=owner_scope),
        Depends(sync_plain if plain_sync else plain, scope=other_scope),
    ]
    if not owner_first:
        dependencies.reverse()

    @app.get("/", dependencies=dependencies)
    async def endpoint():
        if cancel:
            external.cancel()
            await anyio.sleep(0)
        return "ok"

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with external:
                await client.get("/")
    assert events[-2:] == (
        ["owner cleanup", "plain cleanup"]
        if owner_scope == "function"
        else ["plain cleanup", "owner cleanup"]
    )


@pytest.mark.parametrize("scope", ["function", "request"])
@pytest.mark.parametrize("cancel", [False, True])
async def test_task_group_dependency_exits_in_its_original_task(scope, cancel):
    events = []
    external = anyio.CancelScope()
    app = FastAPI()
    value = ContextVar("value", default="outside")
    tasks = []

    async def child():
        try:
            await anyio.sleep_forever()
        finally:
            events.append("child stopped")

    async def dependency():
        tasks.append(anyio.get_current_task().id)
        token = value.set("inside")
        try:
            async with anyio.create_task_group() as group:
                group.start_soon(child)
                try:
                    yield
                finally:
                    group.cancel_scope.cancel()
        finally:
            await anyio.sleep(0)
            value.reset(token)
            tasks.append(anyio.get_current_task().id)
            events.append("cleanup end")

    @app.get("/")
    async def endpoint(_=Depends(dependency, scope=scope)):
        assert value.get() == "inside"
        tasks.append(anyio.get_current_task().id)
        if cancel:
            external.cancel()
            await anyio.sleep(0)
        return "ok"

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with external:
                await client.get("/")
    assert events == ["child stopped", "cleanup end"]
    assert external.cancelled_caught is cancel
    assert len(tasks) == 3 and len(set(tasks)) == 1
    assert value.get() == "outside"


@pytest.mark.parametrize("scope", ["function", "request"])
@pytest.mark.parametrize(
    "kind, cancel",
    [
        pytest.param("http", False, id="http-error"),
        pytest.param("http", True, id="http-cancelled"),
        pytest.param("websocket", True, id="websocket-cancelled"),
        pytest.param("frontend", True, id="frontend-cancelled"),
    ],
)
async def test_cleanup_after_later_dependency_fails(
    scope, kind, cancel, tmp_path: Path
):
    events = []
    caught = []
    external = anyio.CancelScope()
    error = ValueError("later dependency failed")

    async def dependency():
        events.append("enter")
        try:
            yield
        except BaseException as exc:
            caught.append(exc)
            raise
        finally:
            await anyio.sleep(0)
            events.append("cleanup")

    async def later_dependency():
        if cancel:
            external.cancel()
            await anyio.sleep(0)
        raise error

    app = FastAPI(
        dependencies=[
            Depends(dependency, scope=scope),
            Depends(later_dependency),
        ]
    )

    async def endpoint():
        pytest.fail("The endpoint must not run")  # pragma: no cover

    if kind == "http":
        app.get("/")(endpoint)
    elif kind == "websocket":
        app.websocket("/")(endpoint)
    else:
        app.frontend("/", directory=tmp_path)

    async def receive() -> Message:
        pytest.fail("No request body is needed")  # pragma: no cover

    async def send(message: Message) -> None:
        pass

    request_scope: Scope = {
        "type": "websocket" if kind == "websocket" else "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "root_path": "",
        "query_string": b"",
        "headers": [],
    }
    with anyio.fail_after(5):
        with external:
            if cancel:
                await app(request_scope, receive, send)
                pytest.fail("Cancellation must propagate")  # pragma: no cover
            else:
                with pytest.raises(ValueError) as exc_info:
                    await app(request_scope, receive, send)
                assert exc_info.value is error
    assert external.cancelled_caught is cancel
    assert events == ["enter", "cleanup"]
    assert len(caught) == 1
    if cancel:
        assert isinstance(caught[0], anyio.get_cancelled_exc_class())
    else:
        assert caught[0] is error


@pytest.mark.parametrize("scope", ["function", "request"])
async def test_cleanup_error_preserves_context_and_remaining_cleanup(scope):
    events = []
    external = anyio.CancelScope()
    cleanup_error = RuntimeError("cleanup failed")
    app = FastAPI()

    async def outer():
        try:
            yield
        except RuntimeError as exc:
            assert exc is cleanup_error
            raise
        finally:
            await anyio.sleep(0)
            events.append("outer cleanup")

    async def inner(_=Depends(outer, scope=scope)):
        try:
            yield
        finally:
            await anyio.sleep(0)
            events.append("inner cleanup")
            raise cleanup_error

    @app.get("/")
    async def endpoint(_=Depends(inner, scope=scope)):
        external.cancel()
        await anyio.sleep(0)
        pytest.fail("Cancellation must propagate")  # pragma: no cover

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with external:
                with pytest.raises(RuntimeError) as exc_info:
                    await client.get("/")
    assert exc_info.value is cleanup_error
    assert isinstance(cleanup_error.__context__, anyio.get_cancelled_exc_class())
    assert events == ["inner cleanup", "outer cleanup"]


@pytest.mark.parametrize("kind", ["stream", "background"])
async def test_response_remains_cancellable_after_function_cleanup(kind):
    events = []
    external = anyio.CancelScope()
    app = FastAPI()

    async def function_dependency():
        yield
        await anyio.sleep(0)
        events.append("function cleanup")

    async def request_dependency():
        try:
            yield
        finally:
            await anyio.sleep(0)
            events.append("request cleanup")

    async def response_work():
        events.append("response work")
        external.cancel()
        await anyio.sleep(0)
        pytest.fail("Response work must be cancelled")  # pragma: no cover

    async def stream():
        yield b"first"
        await response_work()

    @app.get("/")
    async def endpoint(
        _=Depends(function_dependency, scope="function"),
        __=Depends(request_dependency),
    ):
        if kind == "stream":
            return StreamingResponse(stream())
        return Response(background=BackgroundTask(response_work))

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with external:
                await client.get("/")
    assert external.cancelled_caught
    assert events == ["function cleanup", "response work", "request cleanup"]


@pytest.mark.parametrize("scope", ["function", "request"])
async def test_dependency_can_limit_its_own_cleanup(scope):
    external = anyio.CancelScope()
    events = []
    app = FastAPI()

    async def dependency():
        try:
            yield
        finally:
            with anyio.move_on_after(0) as cleanup_timeout:
                await anyio.sleep_forever()
            assert cleanup_timeout.cancelled_caught
            await anyio.sleep(0)
            events.append("cleanup")

    @app.get("/")
    async def endpoint(_=Depends(dependency, scope=scope)):
        external.cancel()
        await anyio.sleep(0)

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with external:
                await client.get("/")
    assert external.cancelled_caught
    assert events == ["cleanup"]


class CleanupBaseError(BaseException):
    pass


@pytest.mark.parametrize("scope", ["function", "request"])
@pytest.mark.parametrize("error_type", [ValueError, CleanupBaseError])
async def test_task_group_failure_preserves_error_and_finishes_cleanup(
    scope, error_type
):
    entered = anyio.Event()
    events = []
    error = error_type("child failed")

    async def child():
        await entered.wait()
        raise error

    async def dependency():
        try:
            async with anyio.create_task_group() as group:
                group.start_soon(child)
                yield
        finally:
            await anyio.sleep(0)
            events.append("cleanup")

    app = FastAPI()

    @app.get("/")
    async def endpoint(_=Depends(dependency, scope=scope)):
        entered.set()
        await anyio.sleep_forever()

    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with pytest.RaisesGroup(error_type) as exc_info:
                await client.get("/")
    assert exc_info.value.exceptions == (error,)
    assert events == ["cleanup"]


@pytest.mark.parametrize(
    "kind", ["none", "async", "sync", "sync_yield_function", "sync_yield_request"]
)
async def test_pending_cancellation_without_async_yield_keeps_response_timing(kind):
    cancel = anyio.CancelScope()
    events = []

    async def async_dependency():
        return 42

    def sync_dependency():
        return 42

    def sync_yield_dependency():
        try:
            yield 42
        finally:
            events.append("cleanup")

    dependencies = []
    if kind == "async":
        dependencies = [Depends(async_dependency)]
    elif kind == "sync":
        dependencies = [Depends(sync_dependency)]
    elif kind.startswith("sync_yield"):
        dependencies = [
            Depends(
                sync_yield_dependency,
                scope="function" if kind.endswith("function") else "request",
            )
        ]
    app = FastAPI(dependencies=dependencies)

    @app.get("/")
    async def endpoint():
        cancel.cancel()
        return {"ok": True}

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        with cancel:
            response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert cancel.cancel_called
    assert not cancel.cancelled_caught
    assert events == (["cleanup"] if kind.startswith("sync_yield") else [])


@pytest.mark.parametrize("use_async_yield", [False, True])
async def test_cleanup_follows_the_overridden_dependency(use_async_yield):
    cancel = anyio.CancelScope()
    events = []

    async def ordinary():
        return 42

    async def resource():
        events.append("enter")
        try:
            yield 42
        finally:
            await anyio.sleep(0)
            events.append("cleanup")

    original = ordinary if use_async_yield else resource
    replacement = resource if use_async_yield else ordinary
    app = FastAPI()

    @app.get("/")
    async def endpoint(value=Depends(original)):
        assert value == 42
        cancel.cancel()
        if use_async_yield:
            await anyio.sleep(0)
        return {"ok": True}

    app.dependency_overrides[original] = replacement
    response = None
    with anyio.fail_after(5):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            with cancel:
                response = await client.get("/")
    assert cancel.cancelled_caught is use_async_yield
    if use_async_yield:
        assert response is None
        assert events == ["enter", "cleanup"]
    else:
        assert response is not None
        assert response.status_code == 200
        assert events == []
