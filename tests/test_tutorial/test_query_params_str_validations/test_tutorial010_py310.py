import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(name="client")
def get_client():
    from docs_src.query_params_str_validations.tutorial010_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_query_params_str_validations_no_query(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}


@needs_py310
def test_query_params_str_validations_item_query_fixedquery(client: TestClient):
    response = client.get("/items/", params={"item-query": "fixedquery"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
        "q": "fixedquery",
    }


@needs_py310
def test_query_params_str_validations_q_fixedquery(client: TestClient):
    response = client.get("/items/", params={"q": "fixedquery"})
    assert response.status_code == 200
    assert response.json() == {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}


@needs_py310
def test_query_params_str_validations_item_query_nonregexquery(client: TestClient):
    response = client.get("/items/", params={"item-query": "nonregexquery"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["query", "item-query"],
                    "msg": "String should match pattern '^fixedquery$'",
                    "input": "nonregexquery",
                    "ctx": {"pattern": "^fixedquery$"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "ctx": {"pattern": "^fixedquery$"},
                    "loc": ["query", "item-query"],
                    "msg": 'string does not match regex "^fixedquery$"',
                    "type": "value_error.str.regex",
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
                            "description": "Query string for the items to search in the database that have a good match",
                            "required": False,
                            "deprecated": True,
                            "schema": IsDict(
                                {
                                    "anyOf": [
                                        {
                                            "type": "string",
                                            "minLength": 3,
                                            "maxLength": 50,
                                            "pattern": "^fixedquery$",
                                        },
                                        {"type": "null"},
                                    ],
                                    "title": "Query string",
                                    "description": "Query string for the items to search in the database that have a good match",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {
                                    "title": "Query string",
                                    "maxLength": 50,
                                    "minLength": 3,
                                    "pattern": "^fixedquery$",
                                    "type": "string",
                                    "description": "Query string for the items to search in the database that have a good match",
                                }
                            ),
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
