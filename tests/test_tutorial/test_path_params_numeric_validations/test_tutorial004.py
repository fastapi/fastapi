import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_an_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest) -> TestClient:
    mod = importlib.import_module(
        f"docs_src.path_params_numeric_validations.{request.param}"
    )
    return TestClient(mod.app)


@pytest.mark.parametrize(
    "path,expected_response",
    [
        ("/items/42?q=", {"item_id": 42}),
        ("/items/1?q=somequery", {"item_id": 1, "q": "somequery"}),
    ],
)
def test_read_items(client: TestClient, path, expected_response):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == expected_response


def test_read_items_non_int_item_id(client: TestClient):
    response = client.get("/items/invalid_id?q=somequery")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "input": "invalid_id",
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "type": "int_parsing",
            }
        ]
    }


def test_read_items_item_id_less_than_one(client: TestClient):
    response = client.get("/items/0?q=somequery")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "input": "0",
                "msg": "Input should be greater than or equal to 1",
                "type": "greater_than_equal",
                "ctx": {"ge": 1},
            }
        ]
    }


def test_read_items_missing_q(client: TestClient):
    response = client.get("/items/42")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "q"],
                "input": None,
                "msg": "Field required",
                "type": "missing",
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
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {
                                "title": "The ID of the item to get",
                                "type": "integer",
                                "minimum": 1,
                            },
                            "name": "item_id",
                            "in": "path",
                        },
                        {
                            "required": True,
                            "schema": {
                                "type": "string",
                                "title": "Q",
                            },
                            "name": "q",
                            "in": "query",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {},
                                }
                            },
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
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
    }
