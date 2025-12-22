import importlib

from fastapi.testclient import TestClient


def get_client() -> TestClient:
    from docs_src.conditional_openapi import tutorial001_py39

    importlib.reload(tutorial001_py39)

    client = TestClient(tutorial001_py39.app)
    return client


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


def test_root():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


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
