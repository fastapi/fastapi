import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyCookie
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

api_key = APIKeyCookie(name="key")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    user = User(username=oauth_header)
    return user


@app.websocket("/ws/users/me")
async def read_current_user(
    websocket: WebSocket, current_user: User = Depends(get_current_user)
):
    await websocket.accept()
    await websocket.send_text(current_user.username)


def test_security_api_key_ws():
    client = TestClient(app, cookies={"key": "secret"})
    with client.websocket_connect("/ws/users/me") as websocket:
        data = websocket.receive_text()
        assert data == "secret"


def test_security_api_key_no_key_ws():
    client = TestClient(app)
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/users/me"):
            pass
