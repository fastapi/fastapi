import importlib

from fastapi.testclient import TestClient

from ...utils import needs_pydanticv2


def get_client() -> TestClient:
    from docs_src.conditional_openapi import tutorial001

    importlib.reload(tutorial001)

    client = TestClient(tutorial001.app)
    return client


@needs_pydanticv2
def test_disable_openapi(monkeypatch):
    monkeypatch.setenv("OPENAPI_URL", "")
    # Load the client after setting the env var
    client = get_client()
    response = client.get("/openapi.json")
    assert response.status_code == 404, response.text
    response = client.get("/docs")
    assert response.status_code == 404, response.text
    response = client.get("/redoc")
    assert response.status_code == 404, response.text


@needs_pydanticv2
def test_root():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@needs_pydanticv2
def test_default_openapi():
    client = get_client()
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    response = client.get("/redoc")
    assert response.status_code == 200, response.text
    response = client.get("/openapi.json")
    assert response.json() == {
        "openapi": "3.1.0",
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
