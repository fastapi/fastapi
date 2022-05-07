from fastapi.testclient import TestClient

from docs_src.path_operation_advanced_configuration.tutorial006 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "post": {
                "summary": "Create Item",
                "operationId": "create_item_items__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "required": ["name", "price"],
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "price": {"type": "number"},
                                    "description": {"type": "string"},
                                },
                            }
                        }
                    },
                    "required": True,
                },
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_post():
    response = client.post("/items/", data=b"this is actually not validated")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "size": 30,
        "content": {
            "name": "Maaaagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }
