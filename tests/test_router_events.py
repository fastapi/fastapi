from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class State(BaseModel):
    app_startup: bool = False
    app_shutdown: bool = False
    router_startup: bool = False
    router_shutdown: bool = False
    sub_router_startup: bool = False
    sub_router_shutdown: bool = False


state = State()

app = FastAPI()


@app.on_event("startup")
def app_startup():
    state.app_startup = True


@app.on_event("shutdown")
def app_shutdown():
    state.app_shutdown = True


router = APIRouter()


@router.on_event("startup")
def router_startup():
    state.router_startup = True


@router.on_event("shutdown")
def router_shutdown():
    state.router_shutdown = True


sub_router = APIRouter()


@sub_router.on_event("startup")
def sub_router_startup():
    state.sub_router_startup = True


@sub_router.on_event("shutdown")
def sub_router_shutdown():
    state.sub_router_shutdown = True


@sub_router.get("/")
def main():
    return {"message": "Hello World"}


router.include_router(sub_router)
app.include_router(router)


def test_router_events():
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
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
    assert state.app_startup is True
    assert state.router_startup is True
    assert state.sub_router_startup is True
    assert state.app_shutdown is True
    assert state.router_shutdown is True
    assert state.sub_router_shutdown is True
