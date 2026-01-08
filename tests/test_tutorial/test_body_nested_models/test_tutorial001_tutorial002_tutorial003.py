import importlib

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310

UNTYPED_LIST_SCHEMA = {"type": "array", "items": {}}

LIST_OF_STR_SCHEMA = {"type": "array", "items": {"type": "string"}}

SET_OF_STR_SCHEMA = {"type": "array", "items": {"type": "string"}, "uniqueItems": True}


@pytest.fixture(
    name="mod_name",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
    ],
)
def get_mod_name(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(name="client")
def get_client(mod_name: str):
    mod = importlib.import_module(f"docs_src.body_nested_models.{mod_name}")

    client = TestClient(mod.app)
    return client


def test_put_all(client: TestClient, mod_name: str):
    if mod_name.startswith("tutorial003"):
        tags_expected = IsList("foo", "bar", check_order=False)
    else:
        tags_expected = ["foo", "bar", "foo"]

    response = client.put(
        "/items/123",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": ["foo", "bar", "foo"],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "item_id": 123,
        "item": {
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": tags_expected,
        },
    }


def test_put_only_required(client: TestClient):
    response = client.put(
        "/items/5",
        json={"name": "Foo", "price": 35.4},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "item_id": 5,
        "item": {
            "name": "Foo",
            "description": None,
            "price": 35.4,
            "tax": None,
            "tags": [],
        },
    }


def test_put_empty_body(client: TestClient):
    response = client.put(
        "/items/5",
        json={},
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
            {
                "loc": ["body", "price"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_put_missing_required(client: TestClient):
    response = client.put(
        "/items/5",
        json={"description": "A very nice Item"},
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "input": {"description": "A very nice Item"},
                "msg": "Field required",
                "type": "missing",
            },
            {
                "loc": ["body", "price"],
                "input": {"description": "A very nice Item"},
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_openapi_schema(client: TestClient, mod_name: str):
    tags_schema = {"default": [], "title": "Tags"}
    if mod_name.startswith("tutorial001"):
        tags_schema.update(UNTYPED_LIST_SCHEMA)
    elif mod_name.startswith("tutorial002"):
        tags_schema.update(LIST_OF_STR_SCHEMA)
    elif mod_name.startswith("tutorial003"):
        tags_schema.update(SET_OF_STR_SCHEMA)

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "put": {
                    "parameters": [
                        {
                            "in": "path",
                            "name": "item_id",
                            "required": True,
                            "schema": {
                                "title": "Item Id",
                                "type": "integer",
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
                    "summary": "Update Item",
                    "operationId": "update_item_items__item_id__put",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Item",
                                }
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Item": {
                    "properties": {
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                        "description": {
                            "title": "Description",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "price": {
                            "title": "Price",
                            "type": "number",
                        },
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
                        },
                        "tags": tags_schema,
                    },
                    "required": [
                        "name",
                        "price",
                    ],
                    "title": "Item",
                    "type": "object",
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
