from fastapi.testclient import TestClient

from metadata.tutorial004 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/": {
            "get": {
                "tags": ["users"],
                "summary": "Get Users",
                "operationId": "get_users_users__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
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
    },
    "tags": [
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "items",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
    ],
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_path_operations():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    response = client.get("/users/")
    assert response.status_code == 200, response.text
