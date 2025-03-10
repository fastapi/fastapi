import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial003b import app


@pytest.fixture(name="client")
def get_client():
    return TestClient(app)


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == ["Rick", "Morty"]
