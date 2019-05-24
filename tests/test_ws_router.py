from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

router = APIRouter()
app = FastAPI()


@router.websocket("/router")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@router.websocket_route("/ws")
async def starlette_websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, WebSocket!")
    await websocket.close()


app.include_router(router)


def test_router():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, router!"


def test_starlette_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, WebSocket!"
