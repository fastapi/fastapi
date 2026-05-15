from fastapi import Depends, FastAPI
from fastapi.requests import HTTPConnection
from fastapi.testclient import TestClient
from starlette.websockets import WebSocket

app = FastAPI()
app.state.value = 42


async def extract_value_from_http_connection(conn: HTTPConnection):
    return conn.app.state.value


@app.get("/http")
async def get_value_by_http(value: int = Depends(extract_value_from_http_connection)):
    return value


@app.websocket("/ws")
async def get_value_by_ws(
    websocket: WebSocket, value: int = Depends(extract_value_from_http_connection)
):
    await websocket.accept()
    await websocket.send_json(value)
    await websocket.close()


client = TestClient(app)


def test_value_extracting_by_http():
    response = client.get("/http")
    assert response.status_code == 200
    assert response.json() == 42


def test_value_extracting_by_ws():
    with client.websocket_connect("/ws") as websocket:
        assert websocket.receive_json() == 42
