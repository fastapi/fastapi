import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect

from ...utils import needs_py310


@pytest.fixture(name="app")
def get_app():
    from docs_src.websockets.tutorial002_py310 import app

    return app


@needs_py310
def test_main(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert b"<!DOCTYPE html>" in response.content


@needs_py310
def test_websocket_with_cookie(app: FastAPI):
    client = TestClient(app, cookies={"session": "fakesession"})
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/foo/ws") as websocket:
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


@needs_py310
def test_websocket_with_header(app: FastAPI):
    client = TestClient(app)
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


@needs_py310
def test_websocket_with_header_and_query(app: FastAPI):
    client = TestClient(app)
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


@needs_py310
def test_websocket_no_credentials(app: FastAPI):
    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/foo/ws"):
            pytest.fail(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover


@needs_py310
def test_websocket_invalid_data(app: FastAPI):
    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/foo/ws?q=bar&token=some-token"):
            pytest.fail(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover
