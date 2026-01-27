import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial006_py39"),
        pytest.param("tutorial006_an_py39"),
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
        (
            "/items/0?q=&size=0.1",
            {"item_id": 0, "size": 0.1},
        ),
        (
            "/items/1000?q=somequery&size=10.4",
            {"item_id": 1000, "q": "somequery", "size": 10.4},
        ),
    ],
)
def test_read_items(client: TestClient, path, expected_response):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == expected_response


def test_read_items_item_id_less_than_zero(client: TestClient):
    response = client.get("/items/-1?q=somequery&size=5")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "input": "-1",
                "msg": "Input should be greater than or equal to 0",
                "type": "greater_than_equal",
                "ctx": {"ge": 0},
            }
        ]
    }


def test_read_items_item_id_greater_than_one_thousand(client: TestClient):
    response = client.get("/items/1001?q=somequery&size=5")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "input": "1001",
                "msg": "Input should be less than or equal to 1000",
                "type": "less_than_equal",
                "ctx": {"le": 1000},
            }
        ]
    }


def test_read_items_size_too_small(client: TestClient):
    response = client.get("/items/1?q=somequery&size=0.0")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "size"],
                "input": "0.0",
                "msg": "Input should be greater than 0",
                "type": "greater_than",
                "ctx": {"gt": 0.0},
            }
        ]
    }


def test_read_items_size_too_large(client: TestClient):
    response = client.get("/items/1?q=somequery&size=10.5")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "size"],
                "input": "10.5",
                "msg": "Input should be less than 10.5",
                "type": "less_than",
                "ctx": {"lt": 10.5},
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
                                "minimum": 0,
                                "maximum": 1000,
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
                        {
                            "in": "query",
                            "name": "size",
                            "required": True,
                            "schema": {
                                "exclusiveMaximum": 10.5,
                                "exclusiveMinimum": 0,
                                "title": "Size",
                                "type": "number",
                            },
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
