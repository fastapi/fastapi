import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial004_py310", "tutorial004_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.query_param_models.{request.param}")
    return TestClient(mod.app)


def test_omitted_date_range(client: TestClient):
    response = client.get("/items/", params={"limit": "5"})
    assert response.status_code == 200, response.text
    assert response.json() == {"limit": 5, "date_range": None}


def test_date_range(client: TestClient):
    response = client.get(
        "/items/", params={"start": "2026-01-01", "end": "2026-01-31"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "limit": 10,
        "date_range": {"start": "2026-01-01", "end": "2026-01-31"},
    }


def test_incomplete_date_range(client: TestClient):
    response = client.get("/items/", params={"start": "2026-01-01"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "end"]


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/items/"]["get"]["parameters"] == [
        {
            "name": "limit",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 10, "title": "Limit"},
        },
        {
            "name": "start",
            "in": "query",
            "required": False,
            "schema": {"type": "string", "format": "date", "title": "Start"},
        },
        {
            "name": "end",
            "in": "query",
            "required": False,
            "schema": {"type": "string", "format": "date", "title": "End"},
        },
    ]
