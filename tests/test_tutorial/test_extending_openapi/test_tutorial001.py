from fastapi.testclient import TestClient

from docs_src.extending_openapi.tutorial001 import app

client = TestClient(app)


def test():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "Foo"}]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {
            "title": "Custom title",
            "summary": "This is a very custom OpenAPI schema",
            "description": "Here's a longer description of the custom **OpenAPI** schema",
            "version": "2.5.0",
            "x-logo": {
                "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
            },
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
    openapi_schema = response.json()
    # Request again to test the custom cache
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
