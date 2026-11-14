import gc
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import replace
from threading import Event, Lock
from typing import Annotated, Any
from weakref import ref

import anyio
import anyio.from_thread
import anyio.to_thread
import httpx
import pytest
from anyio import wait_all_tasks_blocked
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.exceptions import ResponseValidationError
from starlette.responses import StreamingResponse

pytestmark = pytest.mark.anyio


@asynccontextmanager
async def client_for(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        with anyio.fail_after(5):
            yield client


def semaphore_for(declaration: Any) -> anyio.Semaphore:
    return declaration._concurrency.get_semaphore()


@pytest.mark.parametrize("kind", ["async", "sync", "async_yield", "sync_yield"])
@pytest.mark.parametrize("override", [False, True])
async def test_shared_declaration_limits_both_routes_before_worker_entry(
    kind, override
):
    started = anyio.Event()
    release = anyio.Event()
    active = peak = calls = 0

    def enter():
        nonlocal active, peak, calls
        active += 1
        peak = max(peak, active)
        calls += 1
        if calls == 2:
            started.set()

    def exit():
        nonlocal active
        active -= 1

    async def asynchronous():
        enter()
        try:
            await release.wait()
            return "ok"
        finally:
            exit()

    def synchronous():
        anyio.from_thread.run_sync(enter)
        try:
            anyio.from_thread.run(release.wait)
            return "ok"
        finally:
            anyio.from_thread.run_sync(exit)

    async def async_generator():
        enter()
        try:
            await release.wait()
            yield "ok"
        finally:
            exit()

    def sync_generator():
        anyio.from_thread.run_sync(enter)
        try:
            anyio.from_thread.run(release.wait)
            yield "ok"
        finally:
            anyio.from_thread.run_sync(exit)

    async def original():
        raise AssertionError("The override should run")  # pragma: no cover

    dependency = {
        "async": asynchronous,
        "sync": synchronous,
        "async_yield": async_generator,
        "sync_yield": sync_generator,
    }[kind]
    declaration = Depends(original if override else dependency, max_concurrency=2)
    Value = Annotated[str, declaration]
    app = FastAPI()
    if override:
        app.dependency_overrides[original] = dependency

    @app.get("/one")
    @app.get("/two")
    async def endpoint(value: Value):
        return value

    workers = anyio.to_thread.current_default_thread_limiter()
    responses = []
    async with client_for(app) as client:

        async def send(path):
            responses.append((await client.get(path)).json())

        async with anyio.create_task_group() as group:
            for index in range(6):
                group.start_soon(send, "/one" if index % 2 else "/two")
            await started.wait()
            await wait_all_tasks_blocked()
            assert active == calls == 2
            assert semaphore_for(declaration).statistics().tasks_waiting == 4
            assert workers.borrowed_tokens == (2 if kind.startswith("sync") else 0)
            release.set()
    assert responses == ["ok"] * 6
    assert calls == 6
    assert peak == 2
    assert active == 0
    assert semaphore_for(declaration).value == 2


@pytest.mark.parametrize("acquire_at", ["dependency", "endpoint"])
@pytest.mark.parametrize("scope", ["function", "request"])
async def test_resource_limit_allows_sync_endpoint_and_response_validation(
    acquire_at, scope
):
    resource = Lock()
    acquired = anyio.Event()
    release = Event()
    app = FastAPI()

    def dependency():
        owns_resource = False

        def acquire():
            nonlocal owns_resource
            assert resource.acquire(timeout=3)
            owns_resource = True
            anyio.from_thread.run_sync(acquired.set)
            assert release.wait(3)

        try:
            if acquire_at == "dependency":
                acquire()
            yield acquire
        finally:
            if owns_resource:
                resource.release()

    declaration = Depends(dependency, max_concurrency=1, scope=scope)

    @app.get("/", response_model=int)
    def endpoint(acquire: Annotated[Callable[[], None], declaration]):
        if acquire_at == "endpoint":
            acquire()
        return "1"

    workers = anyio.to_thread.current_default_thread_limiter()
    original_tokens = workers.total_tokens
    workers.total_tokens = 2
    responses = []
    try:
        async with client_for(app) as client:

            async def send():
                response = await client.get("/")
                assert response.status_code == 200
                responses.append(response.json())

            async with anyio.create_task_group() as group:
                try:
                    group.start_soon(send)
                    await acquired.wait()
                    for _ in range(5):
                        group.start_soon(send)
                    # Queue the other requests while the first holds the resource.
                    await wait_all_tasks_blocked()
                finally:
                    release.set()
    finally:
        workers.total_tokens = original_tokens

    assert responses == [1] * 6
    assert not resource.locked()
    assert semaphore_for(declaration).value == 1


@pytest.mark.parametrize("second_limit", [1, 2])
async def test_separate_declarations_are_independent_even_with_identical_annotations(
    second_limit,
):
    entered = 0
    all_entered = anyio.Event()
    release = anyio.Event()

    async def dependency():
        nonlocal entered
        entered += 1
        if entered == 1 + second_limit:
            all_entered.set()
        yield "ok"

    first = Depends(dependency, max_concurrency=1)
    second = Depends(dependency, max_concurrency=second_limit)
    First = Annotated[str, first]
    Second = Annotated[str, second]
    app = FastAPI()

    @app.get("/one")
    async def one(value: First):
        await release.wait()
        return value

    @app.get("/two")
    async def two(value: Second):
        await release.wait()
        return value

    async with client_for(app) as client:

        async def send(path):
            assert (await client.get(path)).json() == "ok"

        async with anyio.create_task_group() as group:
            group.start_soon(send, "/one")
            for _ in range(second_limit):
                group.start_soon(send, "/two")
            await all_entered.wait()
            assert semaphore_for(first).value == semaphore_for(second).value == 0
            release.set()
    assert semaphore_for(first).value == 1
    assert semaphore_for(second).value == second_limit


@pytest.mark.parametrize("use_cache,expected", [(True, 1), (False, 2)])
async def test_cached_reuse_and_separate_executions_with_default_dependencies(
    use_cache, expected
):
    entered = []
    exited = []

    async def dependency():
        value = len(entered)
        entered.append(value)
        try:
            yield value
        finally:
            exited.append(value)

    declaration = Depends(dependency, use_cache=use_cache, max_concurrency=2)
    app = FastAPI()

    @app.get("/")
    async def endpoint(a=declaration, b=declaration):
        assert semaphore_for(declaration).value == 2 - expected
        return [a, b]

    async with client_for(app) as client:
        assert (await client.get("/")).json() == ([0, 0] if use_cache else [0, 1])
    assert entered == list(range(expected))
    assert exited == list(reversed(entered))
    assert semaphore_for(declaration).value == 2


@pytest.mark.parametrize("location", ["app", "router", "route", "inferred"])
async def test_declaration_survives_parameterless_and_inferred_dependencies(location):
    entered = anyio.Event()
    release = anyio.Event()
    calls = 0

    def record_entry():
        nonlocal calls
        calls += 1
        entered.set()

    async def dependency():
        record_entry()
        yield "ok"

    class InferredDependency:
        def __init__(self):
            anyio.from_thread.run_sync(record_entry)
            anyio.from_thread.run(release.wait)

    declaration = Depends(
        None if location == "inferred" else dependency, max_concurrency=1
    )
    Value = Annotated[InferredDependency, declaration]
    app = FastAPI(dependencies=[declaration] if location == "app" else [])
    router = APIRouter(dependencies=[declaration] if location == "router" else [])

    if location == "inferred":

        @router.get("/one")
        @router.get("/two")
        async def endpoint(value: Value):
            await release.wait()
            return "ok"
    else:

        @router.get("/one", dependencies=[declaration] if location == "route" else [])
        @router.get("/two", dependencies=[declaration] if location == "route" else [])
        async def endpoint():
            await release.wait()
            return "ok"

    app.include_router(router)
    async with client_for(app) as client:

        async def send(path):
            assert (await client.get(path)).json() == "ok"

        async with anyio.create_task_group() as group:
            group.start_soon(send, "/one")
            await entered.wait()
            group.start_soon(send, "/two")
            await wait_all_tasks_blocked()
            assert calls == 1
            assert semaphore_for(declaration).statistics().tasks_waiting == 1
            release.set()
    assert calls == 2
    assert semaphore_for(declaration).value == 1


async def test_override_installed_by_earlier_dependency_applies_immediately():
    app = FastAPI()

    async def original():
        return "original"  # pragma: no cover

    async def replacement():
        return "replacement"

    async def configure():
        app.dependency_overrides[original] = replacement

    @app.get("/")
    async def endpoint(
        _: Annotated[None, Depends(configure)],
        value: Annotated[str, Depends(original, max_concurrency=1)],
    ):
        return value

    async with client_for(app) as client:
        assert (await client.get("/")).json() == "replacement"


@pytest.mark.parametrize("failure", ["entry", "endpoint", "validation", "exit"])
async def test_errors_return_capacity(failure):
    async def dependency(request: Request):
        failed_request = request.url.path == "/fail"
        if failed_request and failure == "entry":
            raise RuntimeError("entry")
        try:
            yield 1
        finally:
            await anyio.sleep(0)
            assert semaphore_for(declaration).value == 0
            if failed_request and failure == "exit":
                raise RuntimeError("exit")

    declaration = Depends(dependency, max_concurrency=1)
    app = FastAPI()

    @app.get("/{action}", response_model=int)
    async def endpoint(action: str, value: Annotated[int, declaration]):
        if action == "fail":
            if failure == "endpoint":
                raise RuntimeError("endpoint")
            if failure == "validation":
                return "not an integer"
        return value

    async with client_for(app) as client:
        with pytest.raises(
            ResponseValidationError if failure == "validation" else RuntimeError
        ):
            await client.get("/fail")
        assert semaphore_for(declaration).value == 1
        assert (await client.get("/ok")).json() == 1
    assert semaphore_for(declaration).value == 1


@pytest.mark.parametrize("after_release", [False, True])
async def test_cancelled_waiter_does_not_leak_capacity(after_release):
    events = []

    async def dependency():
        events.append("entered")
        try:
            yield
        finally:
            await anyio.sleep(0)
            events.append("closed")

    declaration = Depends(dependency, max_concurrency=1)
    app = FastAPI()
    semaphore = semaphore_for(declaration)

    @app.get("/")
    async def endpoint(_: Annotated[None, declaration]):
        await anyio.sleep(0)
        return "ok"

    await semaphore.acquire()
    held = True
    try:
        async with client_for(app) as client:

            async def send(*, task_status):
                with anyio.CancelScope() as cancel:
                    task_status.started(cancel)
                    await client.get("/")

            async with anyio.create_task_group() as group:
                cancel = await group.start(send)
                await wait_all_tasks_blocked()
                assert semaphore.statistics().tasks_waiting == 1
                if after_release:
                    semaphore.release()
                    held = False
                cancel.cancel()
            assert semaphore.statistics().tasks_waiting == 0
            if held:
                semaphore.release()
                held = False
            assert semaphore.value == 1
            assert events in ([], ["entered", "closed"])
            assert (await client.get("/")).json() == "ok"
    finally:
        if held:  # pragma: no cover
            semaphore.release()
    assert semaphore.value == 1


@pytest.mark.parametrize("scope", ["function", "request"])
@pytest.mark.parametrize("cancel", [False, True])
async def test_cleanup_can_own_a_task_group(scope, cancel):
    external = anyio.CancelScope()
    events = []
    app = FastAPI()

    async def child():
        try:
            await anyio.sleep_forever()
        finally:
            assert semaphore_for(declaration).value == 0
            events.append("child stopped")

    async def dependency():
        try:
            async with anyio.create_task_group() as group:
                group.start_soon(child)
                try:
                    yield
                finally:
                    group.cancel_scope.cancel()
        finally:
            await anyio.sleep(0)
            assert semaphore_for(declaration).value == 0
            events.append("cleanup finished")

    declaration = Depends(dependency, scope=scope, max_concurrency=1)

    @app.get("/")
    async def endpoint(_: Annotated[None, declaration]):
        if cancel:
            external.cancel()
            await anyio.sleep(0)
        return "ok"

    async with client_for(app) as client:
        with external:
            await client.get("/")
    assert external.cancelled_caught is cancel
    assert events == ["child stopped", "cleanup finished"]
    assert semaphore_for(declaration).value == 1


@pytest.mark.parametrize("scope", ["function", "request"])
async def test_cancelled_admission_cleans_up_earlier_dependency(scope):
    events = []

    async def preparation():
        try:
            events.append("prepared")
            yield
        finally:
            await anyio.sleep(0)
            events.append("closed")

    async def dependency():
        raise AssertionError("Capacity was never available")  # pragma: no cover
        yield

    declaration = Depends(dependency, max_concurrency=1)
    app = FastAPI()
    semaphore = semaphore_for(declaration)

    @app.get("/")
    async def endpoint(
        before: Annotated[None, Depends(preparation, scope=scope)],
        value: Annotated[None, declaration],
    ):
        return value  # pragma: no cover

    await semaphore.acquire()
    try:
        async with client_for(app) as client:

            async def send(*, task_status):
                with anyio.CancelScope() as cancel:
                    task_status.started(cancel)
                    await client.get("/")

            async with anyio.create_task_group() as group:
                cancel = await group.start(send)
                await wait_all_tasks_blocked()
                assert events == ["prepared"]
                assert semaphore.statistics().tasks_waiting == 1
                cancel.cancel()
        assert events == ["prepared", "closed"]
        assert semaphore.statistics().tasks_waiting == 0
    finally:
        semaphore.release()


@pytest.mark.parametrize("scope", ["function", "request"])
async def test_capacity_follows_scope_through_streaming_and_background_work(scope):
    events = []

    async def dependency():
        try:
            yield
        finally:
            await anyio.sleep(0)
            events.append("cleanup")

    declaration = Depends(dependency, scope=scope, max_concurrency=1)
    app = FastAPI()

    async def background():
        assert semaphore_for(declaration).value == (1 if scope == "function" else 0)
        events.append("background")

    async def body():
        assert semaphore_for(declaration).value == (1 if scope == "function" else 0)
        events.append("stream")
        yield "ok"

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks, _: Annotated[None, declaration]):
        tasks.add_task(background)
        return StreamingResponse(body())

    async with client_for(app) as client:
        assert (await client.get("/")).text == "ok"
    assert events == (
        ["cleanup", "stream", "background"]
        if scope == "function"
        else ["stream", "background", "cleanup"]
    )
    assert semaphore_for(declaration).value == 1


@pytest.mark.parametrize("value", [0, -1, True, 1.5, "2"])
def test_invalid_max_concurrency(value):
    with pytest.raises(ValueError, match="positive integer or None"):
        Depends(max_concurrency=value)


def test_app_can_be_reused_across_event_loops():
    async def dependency():
        await anyio.sleep(0)
        return "ok"

    declaration = Depends(dependency, max_concurrency=1)
    app = FastAPI()

    @app.get("/")
    async def endpoint(value: Annotated[str, declaration]):
        return value

    async def send():
        async with client_for(app) as client:
            response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == "ok"

    anyio.run(send, backend="asyncio")
    anyio.run(send, backend="asyncio")
    anyio.run(send, backend="trio")


async def test_discarded_declaration_releases_semaphore():
    declaration = Depends(max_concurrency=1)
    semaphore_ref = ref(semaphore_for(declaration))
    gc.collect()
    assert semaphore_ref() is semaphore_for(declaration)

    del declaration
    gc.collect()
    assert semaphore_ref() is None


@pytest.mark.parametrize("scope", ["function", "request"])
async def test_cancellation_holds_capacity_until_sync_cleanup_finishes(scope):
    ready, cleanup_started = anyio.Event(), anyio.Event()
    release = Event()
    app = FastAPI()
    second_finished = anyio.Event()

    def dependency():
        try:
            yield
        finally:
            anyio.from_thread.run_sync(cleanup_started.set)
            assert release.wait(3)

    declaration = Depends(dependency, max_concurrency=1, scope=scope)

    @app.get("/")
    async def endpoint(request: Request, _: Annotated[None, declaration]):
        if request.headers.get("x-first"):
            ready.set()
            await anyio.sleep_forever()
        return "ok"

    async with client_for(app) as client:

        async def first(*, task_status):
            with anyio.CancelScope() as cancel:
                task_status.started(cancel)
                await client.get("/", headers={"x-first": "true"})

        async def second():
            assert (await client.get("/")).status_code == 200
            second_finished.set()

        async with anyio.create_task_group() as group:
            try:
                cancel = await group.start(first)
                await ready.wait()
                group.start_soon(second)
                await wait_all_tasks_blocked()
                cancel.cancel()
                await cleanup_started.wait()
                assert semaphore_for(declaration).value == 0
                assert semaphore_for(declaration).statistics().tasks_waiting == 1
                assert not second_finished.is_set()
            finally:
                release.set()
    assert second_finished.is_set()
    assert semaphore_for(declaration).value == 1


async def test_cancellation_waiting_for_entry_worker_releases_ownership():
    limiter = anyio.to_thread.current_default_thread_limiter()
    original = limiter.total_tokens
    limiter.total_tokens = 1
    borrower = object()
    await limiter.acquire_on_behalf_of(borrower)
    events = []
    app = FastAPI()

    def dependency():  # pragma: no cover
        events.append("enter")
        try:
            yield
        finally:
            events.append("exit")

    declaration = Depends(dependency, max_concurrency=1)

    @app.get("/")
    async def endpoint(_: Annotated[None, declaration]):
        return "ok"  # pragma: no cover

    try:
        async with client_for(app) as client:

            async def request(*, task_status):
                with anyio.CancelScope() as scope:
                    task_status.started(scope)
                    await client.get("/")

            async with anyio.create_task_group() as group:
                scope = await group.start(request)
                await wait_all_tasks_blocked()
                assert semaphore_for(declaration).value == 0
                assert limiter.statistics().tasks_waiting == 1
                assert not events
                scope.cancel()
    finally:
        limiter.release_on_behalf_of(borrower)
        limiter.total_tokens = original
    assert not events
    assert semaphore_for(declaration).value == 1


@pytest.mark.parametrize("mounted", [False, True])
async def test_shared_declaration_limits_across_apps(mounted):
    apps = [FastAPI(), FastAPI()]
    started = anyio.Event()
    release = anyio.Event()
    entered = []

    async def dependency(request: Request):
        entered.append(request.app)
        started.set()
        yield "ok"

    declaration = Depends(dependency, max_concurrency=1)
    Value = Annotated[str, declaration]
    router = APIRouter()

    @router.get("/")
    async def endpoint(value: Value):
        await release.wait()
        return value

    for app in apps:
        app.include_router(router)
    if mounted:
        parent = FastAPI()
        parent.mount("/one", apps[0])
        parent.mount("/two", apps[1])
        targets = [parent, parent]
        paths = ["/one/", "/two/"]
    else:
        targets = apps
        paths = ["/", "/"]

    async with client_for(targets[0]) as first, client_for(targets[1]) as second:

        async def send(client, path):
            assert (await client.get(path)).json() == "ok"

        async with anyio.create_task_group() as group:
            group.start_soon(send, first, paths[0])
            await started.wait()
            group.start_soon(send, second, paths[1])
            await wait_all_tasks_blocked()
            semaphore = semaphore_for(declaration)
            assert entered == [apps[0]]
            assert semaphore.value == 0
            assert semaphore.statistics().tasks_waiting == 1
            release.set()
    assert entered == apps
    assert semaphore.value == 1
    assert semaphore.statistics().tasks_waiting == 0


@pytest.mark.parametrize(
    "original_limit,new_limit", [(1, 3), (3, 1), (1, None), (None, 2), (1, 1)]
)
async def test_copied_declaration_uses_its_configured_limit(original_limit, new_limit):
    app = FastAPI()
    release = anyio.Event()
    started = anyio.Event()
    entered = closed = active = peak = 0

    async def dependency():
        nonlocal entered, closed, active, peak
        entered += 1
        active += 1
        peak = max(peak, active)
        started.set()
        try:
            yield "ok"
        finally:
            active -= 1
            closed += 1

    original = Depends(dependency, max_concurrency=original_limit)
    declaration = replace(original, max_concurrency=new_limit, use_cache=False)

    @app.get("/")
    async def endpoint(value: Annotated[str, declaration]):
        await release.wait()
        return value

    responses = []
    expected = 4 if new_limit is None else new_limit
    async with client_for(app) as client:

        async def send():
            responses.append((await client.get("/")).json())

        async with anyio.create_task_group() as group:
            try:
                for _ in range(4):
                    group.start_soon(send)
                await started.wait()
                await wait_all_tasks_blocked()
                assert entered == active == expected
                if original_limit is not None:
                    assert semaphore_for(original).value == (
                        0 if original_limit == new_limit else original_limit
                    )
            finally:
                release.set()
    assert responses == ["ok"] * 4
    assert entered == closed == 4
    assert peak == expected
    assert active == 0
    if new_limit is not None:
        assert semaphore_for(declaration).value == new_limit
    if original_limit is not None:
        assert semaphore_for(original).value == original_limit


@pytest.mark.parametrize("reverse", [False, True])
async def test_cached_value_only_uses_capacity_from_the_first_declaration(reverse):
    app = FastAPI()
    entered = closed = 0

    async def dependency():
        nonlocal entered, closed
        entered += 1
        try:
            yield {"message": "ok"}
        finally:
            closed += 1

    first = Depends(dependency, max_concurrency=1)
    second = Depends(dependency, max_concurrency=2)
    declarations = [second, first] if reverse else [first, second]

    @app.get("/")
    async def endpoint(
        a: Annotated[dict[str, str], declarations[0]],
        b: Annotated[dict[str, str], declarations[1]],
    ):
        assert a is b
        assert entered == 1
        assert semaphore_for(first).value == (1 if reverse else 0)
        assert semaphore_for(second).value == (1 if reverse else 2)
        return a

    async with client_for(app) as client:
        assert (await client.get("/")).json() == {"message": "ok"}
    assert entered == closed == 1
    assert semaphore_for(first).value == 1
    assert semaphore_for(second).value == 2


@pytest.mark.parametrize("cancel", [False, True])
async def test_websocket_cleanup_releases_capacity_for_waiting_http_request(cancel):
    app = FastAPI()
    events = []

    async def dependency():
        events.append("enter")
        try:
            yield "ok"
        finally:
            await anyio.sleep(0)
            events.append("exit")

    declaration = Depends(dependency, max_concurrency=1)

    @app.websocket("/ws")
    async def websocket(ws: WebSocket, value: Annotated[str, declaration]):
        await ws.accept()
        try:
            await ws.receive_text()
        except WebSocketDisconnect:
            pass

    @app.get("/")
    async def endpoint(value: Annotated[str, declaration]):
        return value

    incoming_send, incoming_receive = anyio.create_memory_object_stream(1)
    outgoing_send, outgoing_receive = anyio.create_memory_object_stream(1)
    websocket_finished = anyio.Event()
    http_finished = anyio.Event()
    scope = {
        "type": "websocket",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "path": "/ws",
        "raw_path": b"/ws",
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "scheme": "ws",
        "subprotocols": [],
        "client": ("127.0.0.1", 123),
        "server": ("test", 80),
    }

    async def run_websocket(*, task_status):
        with anyio.CancelScope() as cancel_scope:
            task_status.started(cancel_scope)
            await app(scope, incoming_receive.receive, outgoing_send.send)
        assert cancel_scope.cancelled_caught is cancel
        websocket_finished.set()

    async with (
        incoming_send,
        incoming_receive,
        outgoing_send,
        outgoing_receive,
        client_for(app) as client,
    ):

        async def send_http():
            assert (await client.get("/")).json() == "ok"
            http_finished.set()

        async with anyio.create_task_group() as group:
            cancel_scope = await group.start(run_websocket)
            await incoming_send.send({"type": "websocket.connect"})
            assert (await outgoing_receive.receive())["type"] == "websocket.accept"
            group.start_soon(send_http)
            await wait_all_tasks_blocked()
            semaphore = semaphore_for(declaration)
            assert events == ["enter"]
            assert not http_finished.is_set()
            assert semaphore.value == 0
            assert semaphore.statistics().tasks_waiting == 1
            if cancel:
                cancel_scope.cancel()
            else:
                await incoming_send.send({"type": "websocket.disconnect", "code": 1000})
            await websocket_finished.wait()
            await http_finished.wait()
    assert events == ["enter", "exit", "enter", "exit"]
    assert semaphore.value == 1
    assert semaphore.statistics().tasks_waiting == 0
