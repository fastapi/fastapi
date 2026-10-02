import pytest
from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

security = HTTPBearer()


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


def test_security_http_bearer_ws():
    with client.websocket_connect(
        "/ws/users/me", headers={"Authorization": "Bearer foobar"}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"scheme": "Bearer", "credentials": "foobar"}


def test_security_http_bearer_no_credentials_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/users/me"):
            pass


def test_security_http_bearer_incorrect_scheme_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect(
            "/ws/users/me", headers={"Authorization": "Basic notreally"}
        ):
            pass
