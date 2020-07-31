import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect

from docs_src.websockets.tutorial003 import app

client = TestClient(app)


def test_websocket_handle_disconnection():
    with client.websocket_connect("/ws/1234") as connection, client.websocket_connect(
        "/ws/5678"
    ) as connection_two:
        connection_two.close()
        response = client.get("/")
        assert response.status_code == 200, response.text
        assert b"<!DOCTYPE html>" in response.content
