import sys
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient


def make_lifespan(
    name: str, log: list[str], state: dict[str, Any] | None = None
) -> Callable[[Any], AbstractAsyncContextManager[Any]]:
    @asynccontextmanager
    async def lifespan(app: Any) -> AsyncGenerator[Any, None]:
        log.append(f"{name}:startup")
        try:
            yield state
        finally:
            log.append(f"{name}:shutdown")

    return lifespan


def test_lifespan_of_router_included_after_parent_inclusion() -> None:
    log: list[str] = []
    app = FastAPI()
    router = APIRouter(lifespan=make_lifespan("router", log))
    app.include_router(router)

    # Included after `router` was already included in the app: its path
    # operations are served, so its lifespan has to run too.
    sub_router = APIRouter(lifespan=make_lifespan("sub_router", log))

    @sub_router.get("/items")
    def read_items() -> list[str]:
        return ["item"]

    router.include_router(sub_router)

    with TestClient(app) as client:
        assert client.get("/items").json() == ["item"]
        assert log == ["router:startup", "sub_router:startup"]
    assert log == [
        "router:startup",
        "sub_router:startup",
        "sub_router:shutdown",
        "router:shutdown",
    ]


def test_startup_and_shutdown_handlers_run_once_per_inclusion() -> None:
    log: list[str] = []
    app = FastAPI(
        on_startup=[lambda: log.append("app:startup")],
        on_shutdown=[lambda: log.append("app:shutdown")],
    )
    router = APIRouter(
        on_startup=[lambda: log.append("router:startup")],
        on_shutdown=[lambda: log.append("router:shutdown")],
    )
    sub_router = APIRouter(
        on_startup=[lambda: log.append("sub_router:startup")],
        on_shutdown=[lambda: log.append("sub_router:shutdown")],
    )
    router.include_router(sub_router)
    app.include_router(router)

    with TestClient(app):
        assert log == ["app:startup", "router:startup", "sub_router:startup"]
    assert log == [
        "app:startup",
        "router:startup",
        "sub_router:startup",
        "sub_router:shutdown",
        "router:shutdown",
        "app:shutdown",
    ]


def test_handler_added_after_inclusion_runs() -> None:
    log: list[str] = []
    app = FastAPI()
    router = APIRouter()
    app.include_router(router)
    router.add_event_handler("startup", lambda: log.append("router:startup"))

    with TestClient(app):
        assert log == ["router:startup"]


def test_router_with_lifespan_and_event_handlers() -> None:
    log: list[str] = []
    router = APIRouter(
        lifespan=make_lifespan("router", log),
        on_startup=[lambda: log.append("router:on_startup")],
        on_shutdown=[lambda: log.append("router:on_shutdown")],
    )
    app = FastAPI()
    app.include_router(router)

    with TestClient(app):
        assert log == ["router:on_startup", "router:startup"]
    assert log == [
        "router:on_startup",
        "router:startup",
        "router:shutdown",
        "router:on_shutdown",
    ]


def test_app_lifespan_ignores_app_event_handlers() -> None:
    # Unchanged behavior: an explicit app lifespan replaces the app's own
    # on_startup/on_shutdown handlers.
    log: list[str] = []
    app = FastAPI(
        lifespan=make_lifespan("app", log),
        on_startup=[lambda: log.append("app:on_startup")],
    )

    with TestClient(app):
        assert log == ["app:startup"]


def test_lifespan_order_and_state_precedence() -> None:
    log: list[str] = []
    app = FastAPI(lifespan=make_lifespan("app", log, {"key": "app", "app": 1}))
    router_1 = APIRouter(lifespan=make_lifespan("router_1", log, {"key": "router_1"}))
    router_1_sub = APIRouter(
        lifespan=make_lifespan("router_1_sub", log, {"key": "sub", "sub": 2})
    )
    router_2 = APIRouter(lifespan=make_lifespan("router_2", log, {"router_2": 3}))
    router_1.include_router(router_1_sub)
    app.include_router(router_1)
    app.include_router(router_2)

    with TestClient(app) as client:
        # Parents and earlier routers win, as with the nested composition.
        assert client.app_state == {"key": "app", "app": 1, "sub": 2, "router_2": 3}
    assert log == [
        "app:startup",
        "router_1:startup",
        "router_1_sub:startup",
        "router_2:startup",
        "router_2:shutdown",
        "router_1_sub:shutdown",
        "router_1:shutdown",
        "app:shutdown",
    ]


def test_router_included_twice_runs_lifespan_twice() -> None:
    log: list[str] = []
    router = APIRouter(lifespan=make_lifespan("router", log))
    app = FastAPI()
    app.include_router(router, prefix="/a")
    app.include_router(router, prefix="/b")

    with TestClient(app):
        assert log == ["router:startup", "router:startup"]


def test_startup_failure_shuts_down_started_lifespans() -> None:
    log: list[str] = []

    @asynccontextmanager
    async def failing_lifespan(app: Any) -> AsyncGenerator[None, None]:
        raise RuntimeError("startup failed")
        yield  # pragma: no cover

    app = FastAPI(lifespan=make_lifespan("app", log))
    app.include_router(APIRouter(lifespan=make_lifespan("router", log)))
    app.include_router(APIRouter(lifespan=failing_lifespan))

    with pytest.raises(RuntimeError, match="startup failed"):
        with TestClient(app):
            pass  # pragma: no cover
    assert log == [
        "app:startup",
        "router:startup",
        "router:shutdown",
        "app:shutdown",
    ]


def test_many_included_routers_do_not_reach_recursion_limit() -> None:
    log: list[str] = []
    app = FastAPI()
    for _ in range(sys.getrecursionlimit() + 100):
        app.include_router(APIRouter())
    last = APIRouter(lifespan=make_lifespan("last", log))
    app.include_router(last)

    with TestClient(app):
        assert log == ["last:startup"]


def test_assigned_lifespan_context_keeps_included_routers() -> None:
    log: list[str] = []
    app = FastAPI()
    app.include_router(APIRouter(lifespan=make_lifespan("router", log)))
    app.router.lifespan_context = make_lifespan("assigned", log)

    with TestClient(app):
        assert log == ["assigned:startup", "router:startup"]


@pytest.mark.anyio
async def test_lifespan_context_can_be_entered_directly() -> None:
    log: list[str] = []
    app = FastAPI(lifespan=make_lifespan("app", log, {"app": True}))
    app.include_router(
        APIRouter(lifespan=make_lifespan("router", log, {"router": True}))
    )

    async with app.router.lifespan_context(app) as state:
        assert state == {"app": True, "router": True}
        assert log == ["app:startup", "router:startup"]
    assert log == [
        "app:startup",
        "router:startup",
        "router:shutdown",
        "app:shutdown",
    ]
