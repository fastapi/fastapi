from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Union

import pytest
from fastapi import APIRouter, FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel


class State(BaseModel):
    app_startup: bool = False
    app_shutdown: bool = False
    router_startup: bool = False
    router_shutdown: bool = False
    sub_router_startup: bool = False
    sub_router_shutdown: bool = False


@pytest.fixture
def state() -> State:
    return State()


@pytest.mark.filterwarnings(
    r"ignore:\s*on_event is deprecated, use lifespan event handlers instead.*:DeprecationWarning"
)
def test_router_events(state: State) -> None:
    app = FastAPI()

    @app.get("/")
    def main() -> Dict[str, str]:
        return {"message": "Hello World"}

    @app.on_event("startup")
    def app_startup() -> None:
        state.app_startup = True

    @app.on_event("shutdown")
    def app_shutdown() -> None:
        state.app_shutdown = True

    router = APIRouter()

    @router.on_event("startup")
    def router_startup() -> None:
        state.router_startup = True

    @router.on_event("shutdown")
    def router_shutdown() -> None:
        state.router_shutdown = True

    sub_router = APIRouter()

    @sub_router.on_event("startup")
    def sub_router_startup() -> None:
        state.sub_router_startup = True

    @sub_router.on_event("shutdown")
    def sub_router_shutdown() -> None:
        state.sub_router_shutdown = True

    router.include_router(sub_router)
    app.include_router(router)

    assert state.app_startup is False
    assert state.router_startup is False
    assert state.sub_router_startup is False
    assert state.app_shutdown is False
    assert state.router_shutdown is False
    assert state.sub_router_shutdown is False
    with TestClient(app) as client:
        assert state.app_startup is True
        assert state.router_startup is True
        assert state.sub_router_startup is True
        assert state.app_shutdown is False
        assert state.router_shutdown is False
        assert state.sub_router_shutdown is False
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"message": "Hello World"}
    assert state.app_startup is True
    assert state.router_startup is True
    assert state.sub_router_startup is True
    assert state.app_shutdown is True
    assert state.router_shutdown is True
    assert state.sub_router_shutdown is True


def test_app_lifespan_state(state: State) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        state.app_startup = True
        yield
        state.app_shutdown = True

    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    def main() -> Dict[str, str]:
        return {"message": "Hello World"}

    assert state.app_startup is False
    assert state.app_shutdown is False
    with TestClient(app) as client:
        assert state.app_startup is True
        assert state.app_shutdown is False
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"message": "Hello World"}
    assert state.app_startup is True
    assert state.app_shutdown is True


def test_router_nested_lifespan_state(state: State) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, bool], None]:
        state.app_startup = True
        yield {"app": True}
        state.app_shutdown = True

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, bool], None]:
        state.router_startup = True
        yield {"router": True}
        state.router_shutdown = True

    @asynccontextmanager
    async def subrouter_lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, bool], None]:
        state.sub_router_startup = True
        yield {"sub_router": True}
        state.sub_router_shutdown = True

    sub_router = APIRouter(lifespan=subrouter_lifespan)

    router = APIRouter(lifespan=router_lifespan)
    router.include_router(sub_router)

    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    @app.get("/")
    def main(request: Request) -> Dict[str, str]:
        assert request.state.app
        assert request.state.router
        assert request.state.sub_router
        return {"message": "Hello World"}

    assert state.app_startup is False
    assert state.router_startup is False
    assert state.sub_router_startup is False
    assert state.app_shutdown is False
    assert state.router_shutdown is False
    assert state.sub_router_shutdown is False

    with TestClient(app) as client:
        assert state.app_startup is True
        assert state.router_startup is True
        assert state.sub_router_startup is True
        assert state.app_shutdown is False
        assert state.router_shutdown is False
        assert state.sub_router_shutdown is False
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert response.json() == {"message": "Hello World"}

    assert state.app_startup is True
    assert state.router_startup is True
    assert state.sub_router_startup is True
    assert state.app_shutdown is True
    assert state.router_shutdown is True
    assert state.sub_router_shutdown is True


def test_router_nested_lifespan_state_overriding_by_parent() -> None:
    @asynccontextmanager
    async def lifespan(
        app: FastAPI,
    ) -> AsyncGenerator[Dict[str, Union[str, bool]], None]:
        yield {
            "app_specific": True,
            "overridden": "app",
        }

    @asynccontextmanager
    async def router_lifespan(
        app: FastAPI,
    ) -> AsyncGenerator[Dict[str, Union[str, bool]], None]:
        yield {
            "router_specific": True,
            "overridden": "router",  # should override parent
        }

    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    with TestClient(app) as client:
        assert client.app_state == {
            "app_specific": True,
            "router_specific": True,
            "overridden": "app",
        }


def test_merged_no_return_lifespans_return_none() -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    with TestClient(app) as client:
        assert not client.app_state


def test_merged_mixed_state_lifespans() -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, bool], None]:
        yield {"router": True}

    @asynccontextmanager
    async def sub_router_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield

    sub_router = APIRouter(lifespan=sub_router_lifespan)
    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    router.include_router(sub_router)
    app.include_router(router)

    with TestClient(app) as client:
        assert client.app_state == {"router": True}
