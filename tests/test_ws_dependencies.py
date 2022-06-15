import json
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, WebSocket
from fastapi.testclient import TestClient


def dependency_list(deps: Optional[str] = None) -> List[str]:
    return [deps] if deps else []


def create_dependency(name: str):
    def fun(deps: List[str] = Depends(dependency_list)):
        print(f"create_dependency.fun({name})")
        deps.append(name)

    return Depends(fun)


router = APIRouter(dependencies=[create_dependency("router")])
prefix_router = APIRouter(dependencies=[create_dependency("prefix_router")])
app = FastAPI(dependencies=[create_dependency("app")])


@app.websocket("/", dependencies=[create_dependency("index")])
async def index(websocket: WebSocket, deps=Depends(dependency_list)):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


@router.websocket("/router", dependencies=[create_dependency("routerindex")])
async def routerindex(websocket: WebSocket, deps=Depends(dependency_list)):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


@prefix_router.websocket("/", dependencies=[create_dependency("routerprefixindex")])
async def routerprefixindex(websocket: WebSocket, deps=Depends(dependency_list)):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


app.include_router(router, dependencies=[create_dependency("router2")])
app.include_router(
    prefix_router, prefix="/prefix", dependencies=[create_dependency("prefix_router2")]
)


def test_index():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = json.loads(websocket.receive_text())
        assert data == ["app", "index"]


def test_routerindex():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = json.loads(websocket.receive_text())
        assert data == ["app", "router2", "router", "routerindex"]


def test_routerprefixindex():
    client = TestClient(app)
    with client.websocket_connect("/prefix/") as websocket:
        data = json.loads(websocket.receive_text())
        assert data == ["app", "prefix_router2", "prefix_router", "routerprefixindex"]
