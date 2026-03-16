"""Tests for lifespan-scoped dependencies (Depends(..., scope="lifespan"))."""

from contextlib import asynccontextmanager
from typing import Annotated

import pytest
from fastapi import APIRouter, Depends, FastAPI
from fastapi.exceptions import DependencyScopeError
from fastapi.testclient import TestClient
from starlette.requests import Request


def test_lifespan_dependency_single_request() -> None:
    """Lifespan-scoped dependency is created once and reused across requests."""
    started: list[str] = []
    stopped: list[str] = []

    def get_db() -> str:
        started.append("db")
        yield "db_conn"
        stopped.append("db")

    app = FastAPI()

    @app.get("/")
    def root(db: Annotated[str, Depends(get_db, scope="lifespan")]) -> dict[str, str]:
        return {"db": db}

    assert len(started) == 0
    assert len(stopped) == 0

    with TestClient(app) as client:
        assert len(started) == 1, "lifespan dep should start once at app startup"
        r1 = client.get("/")
        assert r1.status_code == 200
        assert r1.json() == {"db": "db_conn"}
        r2 = client.get("/")
        assert r2.status_code == 200
        assert r2.json() == {"db": "db_conn"}
        assert len(started) == 1, "lifespan dep should not restart per request"

    assert len(stopped) == 1, "lifespan dep should stop once at app shutdown"


def test_lifespan_dependency_with_custom_lifespan() -> None:
    """Lifespan-scoped dependency runs inside app lifespan and is cleaned up on shutdown."""
    started: list[str] = []
    stopped: list[str] = []

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        started.append("lifespan")
        yield
        stopped.append("lifespan")

    def get_pool() -> str:
        started.append("pool")
        yield "pool_conn"
        stopped.append("pool")

    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    def root(
        pool: Annotated[str, Depends(get_pool, scope="lifespan")],
    ) -> dict[str, str]:
        return {"pool": pool}

    with TestClient(app) as client:
        assert "lifespan" in started
        assert "pool" in started
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"pool": "pool_conn"}

    assert "pool" in stopped
    assert "lifespan" in stopped


def test_lifespan_dependency_same_instance_across_requests() -> None:
    """The same instance is injected for every request when scope is lifespan."""
    instances: list[object] = []

    def get_singleton() -> object:
        inst = object()
        instances.append(inst)
        yield inst

    app = FastAPI()

    @app.get("/")
    def root(
        s: Annotated[object, Depends(get_singleton, scope="lifespan")],
    ) -> dict[str, bool]:
        return {"is_singleton": len(instances) == 1 and s is instances[0]}

    with TestClient(app) as client:
        r1 = client.get("/")
        r2 = client.get("/")
        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.json()["is_singleton"] is True
        assert r2.json()["is_singleton"] is True
        assert len(instances) == 1


def test_collect_lifespan_dependants_route_level_scope() -> None:
    """Covers _collect_lifespan_dependants when route's flat dependant has computed_scope lifespan."""
    from fastapi.routing import _collect_lifespan_dependants

    router = APIRouter()

    @router.get("/")
    def root() -> dict[str, str]:
        return {"ok": "yes"}

    route = next(r for r in router.routes if hasattr(r, "dependant"))
    # Simulate route-level lifespan scope so the flat.computed_scope == "lifespan" branch is hit
    route.dependant.scope = "lifespan"
    result = _collect_lifespan_dependants(router)
    assert len(result) == 1
    assert result[0].computed_scope == "lifespan"


def test_lifespan_dependency_synthetic_request_receive_send() -> None:
    """Lifespan dep that uses Request.receive covers noop_receive during startup."""

    async def lifespan_dep(request: Request) -> str:
        await request.receive()
        return "ok"

    app = FastAPI()

    @app.get("/")
    def root(
        v: Annotated[str, Depends(lifespan_dep, scope="lifespan")],
    ) -> dict[str, str]:
        return {"v": v}

    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"v": "ok"}


def test_lifespan_dependency_nested() -> None:
    """Lifespan dep B depending on A covers dependency_cache hit path (utils.py line 685)."""
    order: list[str] = []

    def lifespan_a() -> str:
        order.append("a")
        yield "a"

    def lifespan_b(
        a: Annotated[str, Depends(lifespan_a, scope="lifespan")],
    ) -> str:
        order.append("b")
        yield a + "-b"

    app = FastAPI()

    @app.get("/")
    def root(
        b: Annotated[str, Depends(lifespan_b, scope="lifespan")],
    ) -> dict[str, str]:
        return {"b": b}

    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"b": "a-b"}
        assert order == ["a", "b"]


def test_lifespan_dependency_cannot_depend_on_request_scope() -> None:
    """Lifespan-scoped dependency that depends on request-scoped dep raises."""

    def request_scoped() -> int:
        return 1

    def lifespan_dep(
        x: Annotated[int, Depends(request_scoped, scope="request")],
    ) -> int:
        return x

    def root(
        y: Annotated[int, Depends(lifespan_dep, scope="lifespan")],
    ) -> dict[str, int]:
        return {"y": y}

    app = FastAPI()
    with pytest.raises(DependencyScopeError) as exc_info:
        app.get("/")(root)
    assert "lifespan" in str(exc_info.value) and "cannot depend" in str(exc_info.value)


def test_lifespan_dependency_not_initialized_raises() -> None:
    """Request that needs a lifespan dep which was not run (e.g. mounted sub-app) raises."""

    def lifespan_dep() -> str:
        yield "conn"

    sub_app = FastAPI()

    @sub_app.get("/sub")
    def sub_root(
        x: Annotated[str, Depends(lifespan_dep, scope="lifespan")],
    ) -> dict[str, str]:
        return {"x": x}

    main_app = FastAPI()
    main_app.mount("/mounted", sub_app)

    with TestClient(main_app) as client:
        with pytest.raises(DependencyScopeError) as exc_info:
            client.get("/mounted/sub")
        assert "lifespan" in str(exc_info.value).lower()
