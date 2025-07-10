import pytest
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRoute, APIWebSocketRoute
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    route: APIRoute = request.scope["route"]
    return {"user_id": user_id, "path": route.path}


@app.websocket("/items/{item_id}")
async def websocket_item(item_id: str, websocket: WebSocket):
    route: APIWebSocketRoute = websocket.scope["route"]
    await websocket.accept()
    await websocket.send_json({"item_id": item_id, "path": route.path})


client = TestClient(app)


def test_get():
    response = client.get("/users/rick")
    assert response.status_code == 200, response.text
    assert response.json() == {"user_id": "rick", "path": "/users/{user_id}"}


def test_invalid_method_doesnt_match():
    response = client.post("/users/rick")
    assert response.status_code == 405, response.text


def test_invalid_path_doesnt_match():
    response = client.post("/usersx/rick")
    assert response.status_code == 404, response.text


def test_websocket():
    with client.websocket_connect("/items/portal-gun") as websocket:
        data = websocket.receive_json()
        assert data == {"item_id": "portal-gun", "path": "/items/{item_id}"}


def test_websocket_invalid_path_doesnt_match():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/itemsx/portal-gun"):
            pass
