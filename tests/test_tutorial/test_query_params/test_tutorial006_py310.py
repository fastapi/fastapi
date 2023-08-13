import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.query_params.tutorial006_py310 import app

    c = TestClient(app)
    return c


@needs_py310
def test_foo_needy_very(client: TestClient):
    response = client.get("/items/foo?needy=very")
    assert response.status_code == 200
    assert response.json() == {
        "item_id": "foo",
        "needy": "very",
        "skip": 0,
        "limit": None,
    }


@needs_py310
def test_foo_no_needy(client: TestClient):
    response = client.get("/items/foo?skip=a&limit=b")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "needy"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "skip"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "a",
                    "url": match_pydantic_error_url("int_parsing"),
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "limit"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "b",
                    "url": match_pydantic_error_url("int_parsing"),
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "needy"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["query", "skip"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                },
                {
                    "loc": ["query", "limit"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                },
            ]
        }
    )


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
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
                        {
                            "required": False,
                            "schema": {
                                "title": "Skip",
                                "type": "integer",
                                "default": 0,
                            },
                            "name": "skip",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Limit",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Limit", "type": "integer"}
                            ),
                            "name": "limit",
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
