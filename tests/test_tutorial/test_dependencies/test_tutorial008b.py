import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial008b_py39"),
        pytest.param("tutorial008b_an_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.dependencies.{request.param}")

    client = TestClient(mod.app)
    return client


def test_get_no_item(client: TestClient):
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found"}


def test_owner_error(client: TestClient):
    response = client.get("/items/plumbus")
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Owner error: Rick"}


def test_get_item(client: TestClient):
    response = client.get("/items/portal-gun")
    assert response.status_code == 200, response.text
    assert response.json() == {"description": "Gun to create portals", "owner": "Rick"}
