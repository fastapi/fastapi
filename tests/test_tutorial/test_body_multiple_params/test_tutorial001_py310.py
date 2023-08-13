import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_multiple_params.tutorial001_py310 import app

    client = TestClient(app)
    return client


@needs_py310
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


@needs_py310
def test_post_no_body_q_bar(client: TestClient):
    response = client.put("/items/5?q=bar", json=None)
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "bar"}


@needs_py310
def test_post_no_body(client: TestClient):
    response = client.put("/items/5", json=None)
    assert response.status_code == 200
    assert response.json() == {"item_id": 5}


@needs_py310
def test_post_id_foo(client: TestClient):
    response = client.put("/items/foo", json=None)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                    "url": match_pydantic_error_url("int_parsing"),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


@needs_py310
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
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Q",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Q", "type": "string"}
                            ),
                            "name": "q",
                            "in": "query",
                        },
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": IsDict(
                                    {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/Item"},
                                            {"type": "null"},
                                        ],
                                        "title": "Item",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {"$ref": "#/components/schemas/Item"}
                                )
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
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Description", "type": "string"}
                        ),
                        "price": {"title": "Price", "type": "number"},
                        "tax": IsDict(
                            {
                                "title": "Tax",
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Tax", "type": "number"}
                        ),
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
