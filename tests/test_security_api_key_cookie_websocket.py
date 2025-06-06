import pytest
from fastapi import Depends, FastAPI, Security, WebSocket
from fastapi.security import APIKeyCookie
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.testclient import WebSocketDenialResponse

app = FastAPI()

api_key = APIKeyCookie(name="key")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    return User(username=oauth_header)


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: User = Depends(get_current_user),
):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"{data}:{current_user.username}")


def test_security_api_key():
    client = TestClient(app, cookies={"key": "secret"})
    with client.websocket_connect("/ws") as websocket:
        message = "test"
        websocket.send_text(message)
        data = websocket.receive_text()
        assert data == f"{message}:{client.cookies['key']}"


def test_security_api_key_no_key():
    client = TestClient(app)

    with pytest.raises(WebSocketDenialResponse) as exc:
        with client.websocket_connect("/ws"):
            pass
    assert exc.value.status_code == 403, exc.value.text


def test_openapi_schema():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {},
    }
