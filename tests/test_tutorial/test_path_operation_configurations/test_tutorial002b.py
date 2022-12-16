from fastapi.testclient import TestClient

from docs_src.path_operation_configuration.tutorial002b import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "tags": ["items"],
                "summary": "Get Items",
                "operationId": "get_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
        "/users/": {
            "get": {
                "tags": ["users"],
                "summary": "Read Users",
                "operationId": "read_users_users__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get_items():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == ["Portal gun", "Plumbus"]


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    assert response.json() == ["Rick", "Morty"]
