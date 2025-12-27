import importlib
from textwrap import dedent

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310

DESCRIPTIONS = {
    "tutorial003": "Create an item with all the information, name, description, price, tax and a set of unique tags",
    "tutorial004": dedent("""
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
    """).strip(),
}


@pytest.fixture(
    name="mod_name",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
        pytest.param("tutorial004_py39"),
        pytest.param("tutorial004_py310", marks=needs_py310),
    ],
)
def get_mod_name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(name="client")
def get_client(mod_name: str) -> TestClient:
    mod = importlib.import_module(f"docs_src.path_operation_configuration.{mod_name}")
    return TestClient(mod.app)


def test_post_items(client: TestClient):
    response = client.post(
        "/items/",
        json={
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": ["bar", "baz"],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "description": "Item description",
        "price": 42.0,
        "tax": 3.2,
        "tags": IsList("bar", "baz", check_order=False),
    }


def test_openapi_schema(client: TestClient, mod_name: str):
    mod_name = mod_name[:11]

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
                    "summary": "Create an item",
                    "description": DESCRIPTIONS[mod_name],
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                }
                            },
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
                },
            },
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
                "Item": {
                    "properties": {
                        "description": {
                            "anyOf": [
                                {
                                    "type": "string",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Description",
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                        "price": {
                            "title": "Price",
                            "type": "number",
                        },
                        "tags": {
                            "default": [],
                            "items": {
                                "type": "string",
                            },
                            "title": "Tags",
                            "type": "array",
                            "uniqueItems": True,
                        },
                        "tax": {
                            "anyOf": [
                                {
                                    "type": "number",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Tax",
                        },
                    },
                    "required": [
                        "name",
                        "price",
                    ],
                    "title": "Item",
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
