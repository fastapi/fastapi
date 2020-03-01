from fastapi.testclient import TestClient

from application_configuration.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {
        "title": "My Super Project",
        "version": "2.5.0",
        "description": "This is a very fancy project, with auto docs for the API and everything",
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Items",
                "operationId": "read_items_items__get",
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"name": "Foo"}]
