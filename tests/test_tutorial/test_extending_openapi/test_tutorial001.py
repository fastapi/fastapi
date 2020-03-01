from fastapi.testclient import TestClient

from extending_openapi.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {
        "title": "Custom title",
        "version": "2.5.0",
        "description": "This is a very custom OpenAPI schema",
        "x-logo": {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"},
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
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"name": "Foo"}]
