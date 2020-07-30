from fastapi.testclient import TestClient

from docs_src.metadata.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {
        "title": "My API",
        "version": "0.0.1",
        "description": "This is my API, with auto docs for the API and everything",
        "termsOfService": "http://example.com/terms/",
        "contact": {
            "name": "John Doe",
            "url": "http://example.com/contact/",
            "email": "johndoe@example.com",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_items():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "Foo"}]
