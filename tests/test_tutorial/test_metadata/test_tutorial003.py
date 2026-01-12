from fastapi.testclient import TestClient

from docs_src.metadata.tutorial003_py39 import app

client = TestClient(app)


def test_items():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "Foo"}]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
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


def test_swagger_ui_default_url():
    response = client.get("/docs")
    assert response.status_code == 404, response.text


def test_swagger_ui_custom_url():
    response = client.get("/documentation")
    assert response.status_code == 200, response.text
    assert "<title>FastAPI - Swagger UI</title>" in response.text


def test_redoc_ui_default_url():
    response = client.get("/redoc")
    assert response.status_code == 404, response.text
