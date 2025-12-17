import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.testclient import WebSocketDenialResponse
from starlette.websockets import WebSocket

app = FastAPI()

oid = OpenIdConnect(openIdConnectUrl="/openid")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(oid)):
    user = User(username=oauth_header)
    return user


@app.websocket("/ws/users/me")
async def read_current_user(
    websocket: WebSocket, current_user: User = Depends(get_current_user)
):
    await websocket.accept()
    await websocket.send_json(current_user.model_dump())


client = TestClient(app)


def test_security_openid_connect_ws():
    with client.websocket_connect(
        "/ws/users/me", headers={"Authorization": "Bearer footokenbar"}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"username": "Bearer footokenbar"}


def test_security_openid_connect_other_header_ws():
    with client.websocket_connect(
        "/ws/users/me", headers={"Authorization": "Other footokenbar"}
    ) as websocket:
        data = websocket.receive_json()
        assert data == {"username": "Other footokenbar"}


def test_security_openid_connect_no_header_ws():
    with pytest.raises(WebSocketDenialResponse):
        with client.websocket_connect("/ws/users/me"):
            pass
