import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial004_py310", "tutorial004_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.header_param_models.{request.param}")
    return TestClient(mod.app)


def test_omitted_client_headers(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_client_headers(client: TestClient):
    response = client.get(
        "/items/", headers={"X-Client-Name": "example", "X-Client-Version": "1.0"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"x_client_name": "example", "x_client_version": "1.0"}


def test_incomplete_client_headers(client: TestClient):
    response = client.get("/items/", headers={"X-Client-Name": "example"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", "x-client-version"]


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/items/"]["get"]["parameters"] == [
        {
            "name": "x-client-name",
            "in": "header",
            "required": False,
            "schema": {"type": "string", "title": "X Client Name"},
        },
        {
            "name": "x-client-version",
            "in": "header",
            "required": False,
            "schema": {"type": "string", "title": "X Client Version"},
        },
    ]
