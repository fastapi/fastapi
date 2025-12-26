import importlib

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial006_py39"),
        pytest.param("tutorial006_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_nested_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_put_all(client: TestClient):
    response = client.put(
        "/items/123",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": ["foo", "bar", "foo"],
            "images": [
                {"url": "http://example.com/image.png", "name": "example image"}
            ],
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
            "tags": IsList("foo", "bar", check_order=False),
            "images": [
                {"url": "http://example.com/image.png", "name": "example image"}
            ],
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
            "images": None,
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


def test_put_images_not_list(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "price": 35.4,
            "images": {"url": "http://example.com/image.png", "name": "example image"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "images"],
                "input": {
                    "url": "http://example.com/image.png",
                    "name": "example image",
                },
                "msg": "Input should be a valid list",
                "type": "list_type",
            },
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
                "Image": {
                    "properties": {
                        "url": {
                            "title": "Url",
                            "type": "string",
                            "format": "uri",
                            "maxLength": 2083,
                            "minLength": 1,
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                    },
                    "required": ["url", "name"],
                    "title": "Image",
                    "type": "object",
                },
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
                        "tags": {
                            "title": "Tags",
                            "default": [],
                            "type": "array",
                            "items": {"type": "string"},
                            "uniqueItems": True,
                        },
                        "images": {
                            "anyOf": [
                                {
                                    "items": {
                                        "$ref": "#/components/schemas/Image",
                                    },
                                    "type": "array",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Images",
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
