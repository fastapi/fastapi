from base64 import b64encode

import pytest
from fastapi import FastAPI, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

security = HTTPBasic(realm="simple")


@app.websocket("/ws/users/me")
async def read_current_user(
    websocket: WebSocket, credentials: HTTPBasicCredentials = Security(security)
):
    await websocket.accept()
    await websocket.send_json(
        {"username": credentials.username, "password": credentials.password}
    )


client = TestClient(app)


def test_security_http_basic_ws():
    # Build Basic header
    payload = b64encode(b"john:secret").decode("ascii")
    auth_header = f"Basic {payload}"
    with client.websocket_connect(
        "/ws/users/me", headers={"Authorization": auth_header}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"username": "john", "password": "secret"}


def test_security_http_basic_no_credentials_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/users/me"):
            pass


def test_security_http_basic_invalid_credentials_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect(
            "/ws/users/me", headers={"Authorization": "Basic notbase64"}
        ):
            pass
