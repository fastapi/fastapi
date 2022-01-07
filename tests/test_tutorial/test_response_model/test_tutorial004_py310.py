import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
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
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
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
                    "tax": {"title": "Tax", "type": "number", "default": 10.5},
                    "tags": {
                        "title": "Tags",
                        "type": "array",
                        "items": {"type": "string"},
                        "default": [],
                    },
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
    from docs_src.response_model.tutorial004_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


@needs_py310
@pytest.mark.parametrize(
    "url,data",
    [
        ("/items/foo", {"name": "Foo", "price": 50.2}),
        (
            "/items/bar",
            {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        ),
        (
            "/items/baz",
            {
                "name": "Baz",
                "description": None,
                "price": 50.2,
                "tax": 10.5,
                "tags": [],
            },
        ),
    ],
)
def test_get(url, data, client: TestClient):
    response = client.get(url)
    assert response.status_code == 200, response.text
    assert response.json() == data
