import importlib

import pytest
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial010_py39"),
        pytest.param("tutorial010_py310", marks=needs_py310),
        pytest.param("tutorial010_an_py39"),
        pytest.param("tutorial010_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.query_params_str_validations.{request.param}"
    )

    client = TestClient(mod.app)
    return client


def test_query_params_str_validations_no_query(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}


def test_query_params_str_validations_item_query_fixedquery(client: TestClient):
    response = client.get("/items/", params={"item-query": "fixedquery"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
        "q": "fixedquery",
    }


def test_query_params_str_validations_q_fixedquery(client: TestClient):
    response = client.get("/items/", params={"q": "fixedquery"})
    assert response.status_code == 200
    assert response.json() == {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}


def test_query_params_str_validations_item_query_nonregexquery(client: TestClient):
    response = client.get("/items/", params={"item-query": "nonregexquery"})
    assert response.status_code == 422
    assert response.json() == {
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
                            "schema": {
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
                                # See https://github.com/pydantic/pydantic/blob/80353c29a824c55dea4667b328ba8f329879ac9f/tests/test_fastapi.sh#L25-L34.
                                **(
                                    {"deprecated": True}
                                    if PYDANTIC_VERSION_MINOR_TUPLE >= (2, 10)
                                    else {}
                                ),
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
