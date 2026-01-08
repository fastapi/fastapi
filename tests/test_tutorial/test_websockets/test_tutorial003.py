import importlib
from types import ModuleType

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.websockets.{request.param}")

    return mod


@pytest.fixture(name="html")
def get_html(mod: ModuleType):
    return mod.html


@pytest.fixture(name="client")
def get_client(mod: ModuleType):
    client = TestClient(mod.app)

    return client


def test_get(client: TestClient, html: str):
    response = client.get("/")
    assert response.text == html


def test_websocket_handle_disconnection(client: TestClient):
    with (
        client.websocket_connect("/ws/1234") as connection,
        client.websocket_connect("/ws/5678") as connection_two,
    ):
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
