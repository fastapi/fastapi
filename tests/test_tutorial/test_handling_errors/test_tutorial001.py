from starlette.testclient import TestClient

from handling_errors.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Read Item",
                "operationId": "read_item_items__item_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            }
        }
    },
    "components": {
        "schemas": {
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_get_item():
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"item": "The Foo Wrestlers"}


def test_get_item_not_found():
    response = client.get("/items/bar")
    assert response.status_code == 404
    assert response.headers.get("x-error") is None
    assert response.json() == {"detail": "Item not found"}
