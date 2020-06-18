from fastapi import APIRouter, Depends, FastAPI, WebSocket
from fastapi.testclient import TestClient

router = APIRouter()
prefix_router = APIRouter()
app = FastAPI()


@app.websocket_route("/")
async def index(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!")
    await websocket.close()


@router.websocket_route("/router")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@prefix_router.websocket_route("/")
async def routerprefixindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router with prefix!")
    await websocket.close()


@router.websocket("/router2")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


async def ws_dependency():
    return "Socket Dependency"


@router.websocket("/router-ws-depends/")
async def router_ws_decorator_depends(
    websocket: WebSocket, data=Depends(ws_dependency)
):
    await websocket.accept()
    await websocket.send_text(data)
    await websocket.close()


app.include_router(router)
app.include_router(prefix_router, prefix="/prefix")


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, world!"


def test_router():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router!"


def test_prefix_router():
    client = TestClient(app)
    with client.websocket_connect("/prefix/") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router with prefix!"


def test_router2():
    client = TestClient(app)
    with client.websocket_connect("/router2") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router!"


def test_router_ws_depends():
    client = TestClient(app)
    with client.websocket_connect("/router-ws-depends/") as websocket:
        assert websocket.receive_text() == "Socket Dependency"


def test_router_ws_depends_with_override():
    client = TestClient(app)
    app.dependency_overrides[ws_dependency] = lambda: "Override"
    with client.websocket_connect("/router-ws-depends/") as websocket:
        assert websocket.receive_text() == "Override"
