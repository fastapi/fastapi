from starlette.testclient import TestClient

from query_params_str_validations.tutorial010 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                "summary": "Read Items Get",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "description": "Query string for the items to search in the database that have a good match",
                        "required": False,
                        "deprecated": True,
                        "schema": {
                            "title": "Query string",
                            "maxLength": 50,
                            "minLength": 3,
                            "pattern": "^fixedquery$",
                            "type": "string",
                            "description": "Query string for the items to search in the database that have a good match",
                        },
                        "name": "item-query",
                        "in": "query",
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


def test_openapi_scheme():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema
