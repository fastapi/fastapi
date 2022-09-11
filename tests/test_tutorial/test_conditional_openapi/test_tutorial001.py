import importlib

from fastapi.testclient import TestClient

from docs_src.conditional_openapi import tutorial001

openapi_schema = {
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


def test_default_openapi():
    client = TestClient(tutorial001.app)
    response = client.get("/openapi.json")
    assert response.json() == openapi_schema
    response = client.get("/docs")
    assert response.status_code == 200, response.text
    response = client.get("/redoc")
    assert response.status_code == 200, response.text


def test_disable_openapi(monkeypatch):
    monkeypatch.setenv("OPENAPI_URL", "")
    importlib.reload(tutorial001)
    client = TestClient(tutorial001.app)
    response = client.get("/openapi.json")
    assert response.status_code == 404, response.text
    response = client.get("/docs")
    assert response.status_code == 404, response.text
    response = client.get("/redoc")
    assert response.status_code == 404, response.text


def test_root():
    client = TestClient(tutorial001.app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
