import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an_py39",
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_multiple_params.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_body_q_bar_content(client: TestClient):
    response = client.put("/items/5?q=bar", json={"name": "Foo", "price": 50.5})
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        },
        "q": "bar",
    }


def test_post_no_body_q_bar(client: TestClient):
    response = client.put("/items/5?q=bar", json=None)
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "bar"}


def test_post_no_body(client: TestClient):
    response = client.put("/items/5", json=None)
    assert response.status_code == 200
    assert response.json() == {"item_id": 5}


def test_post_id_foo(client: TestClient):
    response = client.put("/items/foo", json=None)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "item_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "foo",
            }
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
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
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Q",
                            },
                            "name": "q",
                            "in": "query",
                        },
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/Item"},
                                        {"type": "null"},
                                    ],
                                    "title": "Item",
                                }
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
                        "description": {
                            "title": "Description",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "price": {"title": "Price", "type": "number"},
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
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
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
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
