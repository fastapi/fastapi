import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial002_py310", "tutorial002_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_forms.{request.param}")
    return TestClient(mod.app)


def test_unchecked_checkbox(client: TestClient):
    response = client.post("/preferences/")
    assert response.status_code == 200
    assert response.json() == {"subscribe": False}


def test_checked_checkbox(client: TestClient):
    response = client.post("/preferences/", data={"subscribe": "on"})
    assert response.status_code == 200
    assert response.json() == {"subscribe": True}
