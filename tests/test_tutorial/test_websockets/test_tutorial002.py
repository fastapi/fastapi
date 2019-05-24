import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from websockets.tutorial002 import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


def test_websocket_with_cookie():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            "/items/1/ws", cookies={"session": "fakesession"}
        ) as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: fakesession"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 1"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: fakesession"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 1"


def test_websocket_with_header():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            "/items/2/ws", headers={"X-Client": "xmen"}
        ) as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: xmen"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: xmen"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"


def test_websocket_with_header_and_query():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            "/items/2/ws?q=baz", headers={"X-Client": "xmen"}
        ) as websocket:
            message = "Message one"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: xmen"
            data = websocket.receive_text()
            assert data == "Query parameter q is: baz"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"
            message = "Message two"
            websocket.send_text(message)
            data = websocket.receive_text()
            assert data == "Session Cookie or X-Client Header value is: xmen"
            data = websocket.receive_text()
            assert data == "Query parameter q is: baz"
            data = websocket.receive_text()
            assert data == f"Message text was: {message}, for item ID: 2"


def test_websocket_no_credentials():
    with pytest.raises(WebSocketDisconnect):
        client.websocket_connect("/items/2/ws")


def test_websocket_invalid_data():
    with pytest.raises(WebSocketDisconnect):
        client.websocket_connect("/items/foo/ws", headers={"X-Client": "xmen"})
