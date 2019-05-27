import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from websockets.tutorial001 import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


def test_websocket():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws") as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == f"Message text was: {message}"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == f"Message text was: {message}"
