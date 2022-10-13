import pytest
from fastapi.testclient import TestClient

from docs_src.header_params.tutorial001 import app

client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
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
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "User-Agent", "type": "string"},
                        "name": "user-agent",
                        "in": "header",
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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


@pytest.mark.parametrize(
    "path,headers,expected_status,expected_response",
    [
        ("/openapi.json", None, 200, openapi_schema),
        ("/items", None, 200, {"User-Agent": "testclient"}),
        ("/items", {"X-Header": "notvalid"}, 200, {"User-Agent": "testclient"}),
        ("/items", {"User-Agent": "FastAPI test"}, 200, {"User-Agent": "FastAPI test"}),
    ],
)
def test(path, headers, expected_status, expected_response):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response
