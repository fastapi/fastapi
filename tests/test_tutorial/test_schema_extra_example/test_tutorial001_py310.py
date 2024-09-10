import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310, needs_pydanticv2


@pytest.fixture(name="client")
def get_client():
    from docs_src.schema_extra_example.tutorial001_py310 import app

    client = TestClient(app)
    return client


@needs_py310
@needs_pydanticv2
def test_post_body_example(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    )
    assert response.status_code == 200


@needs_py310
@needs_pydanticv2
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    # insert_assert(response.json())
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "put": {
                    "summary": "Update Item",
                    "operationId": "update_item_items__item_id__put",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer", "title": "Item Id"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                    },
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
                }
            }
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "Item": {
                    "properties": {
                        "name": {"type": "string", "title": "Name"},
                        "description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Description",
                        },
                        "price": {"type": "number", "title": "Price"},
                        "tax": {
                            "anyOf": [{"type": "number"}, {"type": "null"}],
                            "title": "Tax",
                        },
                    },
                    "type": "object",
                    "required": ["name", "price"],
                    "title": "Item",
                    "examples": [
                        {
                            "description": "A very nice Item",
                            "name": "Foo",
                            "price": 35.4,
                            "tax": 3.2,
                        }
                    ],
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }
