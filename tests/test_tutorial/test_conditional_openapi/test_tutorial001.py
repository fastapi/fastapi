import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_pydanticv1


@pytest.fixture(name="client")
def get_client():
    from docs_src.conditional_openapi import tutorial001

    importlib.reload(tutorial001)

    client = TestClient(tutorial001.app)
    return client


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_disable_openapi(monkeypatch, client: TestClient):
    monkeypatch.setenv("OPENAPI_URL", "")
    response = client.get("/openapi.json")
    assert response.status_code == 404, response.text
    response = client.get("/docs")
    assert response.status_code == 404, response.text
    response = client.get("/redoc")
    assert response.status_code == 404, response.text


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# TODO: pv2 add version with Pydantic v2
@needs_pydanticv1
def test_default_openapi(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    response = client.get("/openapi.json")
    assert response.json() == {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "get": {
                    "summary": "Root",
                    "operationId": "root__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            }
        },
    }
