import importlib

import pytest
from fastapi.testclient import TestClient



@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial005_py310"),
    ],
)

def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body.{request.param}")
    client = TestClient(mod.app)
    return client


def test_required_nullable_field(client: TestClient):
    response = client.post("/items/", json={"description": None})
    assert response.status_code == 200
    assert response.json() == {"description": None}


def test_required_field_missing(client: TestClient):
    response = client.post("/items/", json={})
    assert response.status_code == 200
    assert response.json() == {"description": None}

