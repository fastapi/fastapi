import pytest
from fastapi.testclient import TestClient

from query_params.tutorial005 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
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
                "summary": "Read User Item",
                "operationId": "read_user_item_items__item_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Needy", "type": "string"},
                        "name": "needy",
                        "in": "query",
                    },
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


query_required = {
    "detail": [
        {
            "loc": ["query", "needy"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/openapi.json", 200, openapi_schema),
        ("/items/foo?needy=very", 200, {"item_id": "foo", "needy": "very"}),
        ("/items/foo", 422, query_required),
        ("/items/foo", 422, query_required),
    ],
)
def test(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
