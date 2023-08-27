import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial004_an import app

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/items",
            200,
            {
                "items": [
                    {"item_name": "Foo"},
                    {"item_name": "Bar"},
                    {"item_name": "Baz"},
                ]
            },
        ),
        (
            "/items?q=foo",
            200,
            {
                "items": [
                    {"item_name": "Foo"},
                    {"item_name": "Bar"},
                    {"item_name": "Baz"},
                ],
                "q": "foo",
            },
        ),
        (
            "/items?q=foo&skip=1",
            200,
            {"items": [{"item_name": "Bar"}, {"item_name": "Baz"}], "q": "foo"},
        ),
        (
            "/items?q=bar&limit=2",
            200,
            {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}], "q": "bar"},
        ),
        (
            "/items?q=bar&skip=1&limit=1",
            200,
            {"items": [{"item_name": "Bar"}], "q": "bar"},
        ),
        (
            "/items?limit=1&q=bar&skip=1",
            200,
            {"items": [{"item_name": "Bar"}], "q": "bar"},
        ),
    ],
)
def test_get(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_openapi_schema():
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
                            "schema": {
                                "title": "Limit",
                                "type": "integer",
                                "default": 100,
                            },
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
