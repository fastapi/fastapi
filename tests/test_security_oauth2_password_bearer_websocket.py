import pytest
from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.websocket("/ws/token")
async def read_token(websocket: WebSocket, token: str = Security(oauth2_scheme)):
    await websocket.accept()
    await websocket.send_text(token)


client = TestClient(app)


def test_security_oauth2_password_bearer_ws():
    with client.websocket_connect(
        "/ws/token", headers={"Authorization": "Bearer faketoken"}
    ) as websocket:
        data = websocket.receive_text()
        assert data == "faketoken"


def test_security_oauth2_password_bearer_no_header_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/token"):
            pass


def test_security_oauth2_password_bearer_wrong_scheme_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect(
            "/ws/token", headers={"Authorization": "Basic nope"}
        ):
            pass
