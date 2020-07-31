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
        data = connection.receive_text()
        assert data == f"Client #5678 left the chat."
