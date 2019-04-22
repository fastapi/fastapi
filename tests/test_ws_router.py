from fastapi import APIRouter, FastAPI, Header
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

router = APIRouter()
prefix_router = APIRouter()
app = FastAPI()


@app.websocket_route("/")
async def index(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!")
    await websocket.close()


@app.websocket_route("/header")
async def index_header(
    websocket: WebSocket, user_data: str = Header(None), user_age: int = Header(None)
):
    await websocket.accept()
    await websocket.send_json({"user_data": user_data, "user_age": user_age})
    await websocket.close()


@router.websocket_route("/router")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@router.websocket_route("/router/header")
async def routerindex_header(websocket: WebSocket, user_data: str = Header(None)):
    await websocket.accept()
    await websocket.send_json({"user_data": user_data})
    await websocket.close()


@prefix_router.websocket_route("/")
async def routerprefixindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router with prefix!")
    await websocket.close()


app.include_router(router)
app.include_router(prefix_router, prefix="/prefix")


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, world!"


def test_ws_header():
    client = TestClient(app)
    headers = {"User-Data": "foo"}
    with client.websocket_connect("/header", headers=headers) as websocket:
        data = websocket.receive_json()
        assert data["user_data"] == headers["User-Data"]
    with client.websocket_connect("/router/header", headers=headers) as websocket:
        data = websocket.receive_json()
        assert data["user_data"] == headers["User-Data"]


def test_ws_header_parse():
    client = TestClient(app)
    headers = {"User-Age": "5"}
    with client.websocket_connect("/header", headers=headers) as websocket:
        data = websocket.receive_json()
        assert data["user_age"] == 5


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
