import importlib

import pytest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.query_params.{request.param}")

    client = TestClient(mod.app)
    return client


@pytest.mark.parametrize(
    ("path", "expected_json"),
    [
        (
            "/items/foo",
            {
                "item_id": "foo",
                "description": "This is an amazing item that has a long description",
            },
        ),
        (
            "/items/bar?q=somequery",
            {
                "item_id": "bar",
                "q": "somequery",
                "description": "This is an amazing item that has a long description",
            },
        ),
        (
            "/items/baz?short=true",
            {"item_id": "baz"},
        ),
    ],
)
def test_read_user_item(client: TestClient, path, expected_json):
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == expected_json


@pytest.mark.parametrize("short", ["0", "false", "off", "no", "FaLsE"])
def test_boolean_query_false(client: TestClient, short: str):
    response = client.get("/items/foo", params={"short": short})
    assert response.status_code == 200
    assert response.json() == {
        "item_id": "foo",
        "description": "This is an amazing item that has a long description",
    }


@pytest.mark.parametrize("short", ["", "maybe"])
def test_invalid_boolean_query(client: TestClient, short: str):
    response = client.get("/items/foo", params={"short": short})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "bool_parsing",
                "loc": ["query", "short"],
                "msg": "Input should be a valid boolean, unable to interpret input",
                "input": short,
            }
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/{item_id}": {
                    "get": {
                        "summary": "Read Item",
                        "operationId": "read_item_items__item_id__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Item Id", "type": "string"},
                                "name": "item_id",
                                "in": "path",
                            },
                            {
                                "required": False,
                                "schema": {
                                    "title": "Q",
                                    "anyOf": [
                                        {
                                            "type": "string",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                },
                                "name": "q",
                                "in": "query",
                            },
                            {
                                "required": False,
                                "schema": {
                                    "title": "Short",
                                    "type": "boolean",
                                    "default": False,
                                },
                                "name": "short",
                                "in": "query",
                            },
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                            "422": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError",
                                        },
                                    },
                                },
                                "description": "Validation Error",
                            },
                        },
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
                            "input": {"title": "Input"},
                            "ctx": {"title": "Context", "type": "object"},
                        },
                    },
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                }
            },
        }
    )
