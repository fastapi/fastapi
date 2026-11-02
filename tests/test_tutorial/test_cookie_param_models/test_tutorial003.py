import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial003_py310", "tutorial003_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.cookie_param_models.{request.param}")
    return TestClient(mod.app)


def test_omitted_preferences(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_preferences(client: TestClient):
    response = client.get("/items/", headers={"cookie": "theme=dark; locale=en"})
    assert response.status_code == 200, response.text
    assert response.json() == {"theme": "dark", "locale": "en"}


def test_incomplete_preferences(client: TestClient):
    response = client.get("/items/", headers={"cookie": "theme=dark"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["cookie", "locale"]


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/items/"]["get"]["parameters"] == [
        {
            "name": "theme",
            "in": "cookie",
            "required": False,
            "schema": {"type": "string", "title": "Theme"},
        },
        {
            "name": "locale",
            "in": "cookie",
            "required": False,
            "schema": {"type": "string", "title": "Locale"},
        },
    ]
