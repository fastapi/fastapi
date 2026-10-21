import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial005_py310", "tutorial005_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")
    return TestClient(mod.app)


@pytest.mark.parametrize("profile", [{}, {"name": "Rick", "age": "70"}])
def test_optional_profile(client: TestClient, profile):
    response = client.post("/profiles/", data={"token": "secret", **profile})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "token": "secret",
        "profile": {"name": "Rick", "age": 70} if profile else None,
    }


@pytest.mark.parametrize("name", ["Rick", ""])
def test_incomplete_profile(client: TestClient, name):
    response = client.post("/profiles/", data={"token": "secret", "name": name})
    assert response.status_code == 422
    assert response.json()["detail"][-1]["loc"] == ["body", "age"]
