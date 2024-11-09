import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.additional_status_codes.tutorial001_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_update(client: TestClient):
    response = client.put("/items/foo", json={"name": "Wrestlers"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Wrestlers", "size": None}


@needs_py310
def test_create(client: TestClient):
    response = client.put("/items/red", json={"name": "Chillies"})
    assert response.status_code == 201, response.text
    assert response.json() == {"name": "Chillies", "size": None}
