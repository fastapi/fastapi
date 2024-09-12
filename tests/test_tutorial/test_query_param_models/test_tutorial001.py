import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from tests.utils import needs_py39, needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py39", marks=needs_py39),
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an",
        pytest.param("tutorial001_an_py39", marks=needs_py39),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.query_param_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_query_param_model(client: TestClient):
    response = client.get(
        "/items/",
        params={
            "limit": 10,
            "offset": 5,
            "order_by": "updated_at",
            "tags": ["tag1", "tag2"],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "limit": 10,
        "offset": 5,
        "order_by": "updated_at",
        "tags": ["tag1", "tag2"],
    }


def test_query_param_model_defaults(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "limit": 100,
        "offset": 0,
        "order_by": "created_at",
        "tags": [],
    }


def test_query_param_model_invalid(client: TestClient):
    response = client.get(
        "/items/",
        params={
            "limit": 150,
            "offset": -1,
            "order_by": "invalid",
        },
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["query", "limit"],
                    "msg": "Input should be less than or equal to 100",
                    "input": "150",
                    "ctx": {"le": 100},
                },
                {
                    "type": "greater_than_equal",
                    "loc": ["query", "offset"],
                    "msg": "Input should be greater than or equal to 0",
                    "input": "-1",
                    "ctx": {"ge": 0},
                },
                {
                    "type": "literal_error",
                    "loc": ["query", "order_by"],
                    "msg": "Input should be 'created_at' or 'updated_at'",
                    "input": "invalid",
                    "ctx": {"expected": "'created_at' or 'updated_at'"},
                },
            ]
        }
    )


def test_query_param_model_extra(client: TestClient):
    response = client.get(
        "/items/",
        params={
            "limit": 10,
            "offset": 5,
            "order_by": "updated_at",
            "tags": ["tag1", "tag2"],
            "extra": "plumbus",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "limit": 10,
        "offset": 5,
        "order_by": "updated_at",
        "tags": ["tag1", "tag2"],
    }


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
                                "name": "limit",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "maximum": 100,
                                    "exclusiveMinimum": 0,
                                    "default": 100,
                                    "title": "Limit",
                                },
                            },
                            {
                                "name": "offset",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "default": 0,
                                    "title": "Offset",
                                },
                            },
                            {
                                "name": "order_by",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "enum": ["created_at", "updated_at"],
                                    "type": "string",
                                    "default": "created_at",
                                    "title": "Order By",
                                },
                            },
                            {
                                "name": "tags",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "default": [],
                                    "title": "Tags",
                                },
                            },
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
