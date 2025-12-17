import pytest
from fastapi import FastAPI, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

security = HTTPBase(scheme="Other")


@app.websocket("/ws/users/me")
async def read_current_user(
    websocket: WebSocket,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    await websocket.accept()
    await websocket.send_json(
        {"scheme": credentials.scheme, "credentials": credentials.credentials}
    )


client = TestClient(app)


def test_security_http_base_ws():
    with client.websocket_connect(
        "/ws/users/me", headers={"Authorization": "Other foobar"}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"scheme": "Other", "credentials": "foobar"}


def test_security_http_base_no_credentials_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/users/me"):
            pass
