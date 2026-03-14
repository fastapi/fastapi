"""Tests for lifespan-scoped dependencies (Depends(..., scope="lifespan"))."""

from contextlib import asynccontextmanager
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.exceptions import DependencyScopeError
from fastapi.testclient import TestClient


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


def test_lifespan_dependency_cannot_depend_on_request_scope() -> None:
    """Lifespan-scoped dependency that depends on request-scoped dep raises."""

    def request_scoped() -> int:
        return 1  # pragma: no cover

    # Inner dep must have explicit scope="request" so the scope check triggers
    def lifespan_dep(
        x: int = Depends(request_scoped, scope="request"),
    ) -> int:
        return x  # pragma: no cover

    def root(
        y: Annotated[int, Depends(lifespan_dep, scope="lifespan")],
    ) -> dict[str, int]:
        return {"y": y}  # pragma: no cover

    app = FastAPI()  # pragma: no cover
    with pytest.raises(DependencyScopeError) as exc_info:
        app.get("/")(root)
    assert "lifespan" in str(exc_info.value) and "cannot depend" in str(exc_info.value)


def test_lifespan_dependency_sync_callable() -> None:
    """Lifespan-scoped dependency that is a plain sync function (no generator) works."""

    def get_config() -> str:
        return "config"  # pragma: no cover

    app = FastAPI()

    @app.get("/")
    def root(
        cfg: Annotated[str, Depends(get_config, scope="lifespan")],
    ) -> dict[str, str]:
        return {"cfg": cfg}

    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"cfg": "config"}


def test_lifespan_dependency_async_callable() -> None:
    """Lifespan-scoped dependency that is an async function (no generator) works."""

    async def get_async_config() -> str:
        return "async_config"  # pragma: no cover

    app = FastAPI()

    @app.get("/")
    def root(
        cfg: Annotated[str, Depends(get_async_config, scope="lifespan")],
    ) -> dict[str, str]:
        return {"cfg": cfg}

    with TestClient(app) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"cfg": "async_config"}


def test_lifespan_dependency_not_initialized_raises() -> None:
    """Request that needs a lifespan dep which was not run (e.g. mounted sub-app) raises."""

    def lifespan_dep() -> str:
        yield "conn"  # pragma: no cover

    sub_app = FastAPI()

    @sub_app.get("/sub")
    def sub_root(
        x: Annotated[str, Depends(lifespan_dep, scope="lifespan")],
    ) -> dict[str, str]:
        return {"x": x}  # pragma: no cover

    main_app = FastAPI()
    main_app.mount("/mounted", sub_app)

    with TestClient(main_app) as client:
        # Sub-app's lifespan never ran, so lifespan dep is not in cache
        with pytest.raises(DependencyScopeError) as exc_info:
            client.get("/mounted/sub")
        assert "lifespan" in str(exc_info.value).lower()  # pragma: no cover
