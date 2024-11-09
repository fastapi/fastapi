import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.dependencies.tutorial008b_an_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_get_no_item(client: TestClient):
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found"}


@needs_py39
def test_owner_error(client: TestClient):
    response = client.get("/items/plumbus")
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Owner error: Rick"}


@needs_py39
def test_get_item(client: TestClient):
    response = client.get("/items/portal-gun")
    assert response.status_code == 200, response.text
    assert response.json() == {"description": "Gun to create portals", "owner": "Rick"}
