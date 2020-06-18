import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from websockets.tutorial002 import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert b"<!DOCTYPE html>" in response.content


def test_websocket_with_cookie():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            "/items/foo/ws", cookies={"session": "fakesession"}
        ) as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: fakesession"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: foo"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: fakesession"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: foo"


def test_websocket_with_header():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/bar/ws?token=some-token") as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: some-token"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: bar"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: some-token"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: bar"


def test_websocket_with_header_and_query():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/2/ws?q=3&token=some-token") as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: some-token"
            data = websocket.receive_text()
            assert data == "Query parameter q is: 3"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session cookie or query token value is: some-token"
            data = websocket.receive_text()
            assert data == "Query parameter q is: 3"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"


def test_websocket_no_credentials():
    with pytest.raises(WebSocketDisconnect):
        client.websocket_connect("/items/foo/ws")


def test_websocket_invalid_data():
    with pytest.raises(WebSocketDisconnect):
        client.websocket_connect("/items/foo/ws?q=bar&token=some-token")
