import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="app")
def get_app():
    from docs_src.websockets.tutorial003_py39 import app

    return app


@pytest.fixture(name="html")
def get_html():
    from docs_src.websockets.tutorial003_py39 import html

    return html


@pytest.fixture(name="client")
def get_client(app: FastAPI):
    client = TestClient(app)

    return client


@needs_py39
def test_get(client: TestClient, html: str):
    response = client.get("/")
    assert response.text == html


@needs_py39
def test_websocket_handle_disconnection(client: TestClient):
    with client.websocket_connect("/ws/1234") as connection, client.websocket_connect(
        "/ws/5678"
    ) as connection_two:
        connection.send_text("Hello from 1234")
        data1 = connection.receive_text()
        assert data1 == "You wrote: Hello from 1234"
        data2 = connection_two.receive_text()
        client1_says = "Client #1234 says: Hello from 1234"
        assert data2 == client1_says
        data1 = connection.receive_text()
        assert data1 == client1_says
        connection_two.close()
        data1 = connection.receive_text()
        assert data1 == "Client #5678 left the chat"
