import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an_py39",
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.additional_status_codes.{request.param}")

    client = TestClient(mod.app)
    return client


def test_update(client: TestClient):
    response = client.put("/items/foo", json={"name": "Wrestlers"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Wrestlers", "size": None}


def test_create(client: TestClient):
    response = client.put("/items/red", json={"name": "Chillies"})
    assert response.status_code == 201, response.text
    assert response.json() == {"name": "Chillies", "size": None}
