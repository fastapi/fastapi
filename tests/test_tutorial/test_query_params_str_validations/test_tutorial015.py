import importlib

import pytest
from dirty_equals import IsStr
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial015_an_py39"),
        pytest.param("tutorial015_an_py310", marks=[needs_py310]),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.query_params_str_validations.{request.param}"
    )

    client = TestClient(mod.app)
    return client


def test_get_random_item(client: TestClient):
    response = client.get("/items")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": IsStr(), "name": IsStr()}


def test_get_item(client: TestClient):
    response = client.get("/items?id=isbn-9781529046137")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": "isbn-9781529046137",
        "name": "The Hitchhiker's Guide to the Galaxy",
    }


def test_get_item_does_not_exist(client: TestClient):
    response = client.get("/items?id=isbn-nope")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "isbn-nope", "name": None}


def test_get_invalid_item(client: TestClient):
    response = client.get("/items?id=wtf-yes")
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["query", "id"],
                    "msg": 'Value error, Invalid ID format, it must start with "isbn-" or "imdb-"',
                    "input": "wtf-yes",
                    "ctx": {"error": {}},
                }
            ]
        }
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "get": {
                        "summary": "Read Items",
                        "operationId": "read_items_items__get",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Id",
                                },
                            }
                        ],
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
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
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
    )
