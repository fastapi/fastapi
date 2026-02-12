import importlib

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect

from ...utils import needs_py310


@pytest.fixture(
    name="app",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
        pytest.param("tutorial002_an_py39"),
        pytest.param("tutorial002_an_py310", marks=needs_py310),
    ],
)
def get_app(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.websockets.{request.param}")

    return mod.app


def test_main(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert b"<!DOCTYPE html>" in response.content


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


def test_websocket_no_credentials(app: FastAPI):
    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/foo/ws"):
            pytest.fail(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover


def test_websocket_invalid_data(app: FastAPI):
    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/items/foo/ws?q=bar&token=some-token"):
            pytest.fail(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover
