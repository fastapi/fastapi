import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "put": {
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
                "summary": "Update Item",
                "operationId": "update_item_items__item_id__put",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "The ID of the item to get",
                            "maximum": 1000.0,
                            "minimum": 0.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    },
                    {
                        "required": False,
                        "schema": {"title": "Q", "type": "string"},
                        "name": "q",
                        "in": "query",
                    },
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Item"}
                        }
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "title": "Item",
                "required": ["name", "price"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {"title": "Price", "type": "number"},
                    "description": {"title": "Description", "type": "string"},
                    "tax": {"title": "Tax", "type": "number"},
                },
            },
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


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_multiple_params.tutorial001_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


item_id_not_int = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


@needs_py310
@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/items/5?q=bar",
            {"name": "Foo", "price": 50.5},
            200,
            {
                "item_id": 5,
                "item": {
                    "name": "Foo",
                    "price": 50.5,
                    "description": None,
                    "tax": None,
                },
                "q": "bar",
            },
        ),
        ("/items/5?q=bar", None, 200, {"item_id": 5, "q": "bar"}),
        ("/items/5", None, 200, {"item_id": 5}),
        ("/items/foo", None, 422, item_id_not_int),
    ],
)
def test_post_body(path, body, expected_status, expected_response, client: TestClient):
    response = client.put(path, json=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response
