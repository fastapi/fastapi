import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(
    name="client",
    params=[
        "tutorial003",
        pytest.param("tutorial003_py39", marks=needs_py39),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.websockets.{request.param}")

    client = TestClient(mod.app)
    client.html = mod.html
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.text == client.html


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
