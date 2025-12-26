import importlib

import pytest
from dirty_equals import IsList
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_py310", marks=needs_py310),
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
            "image": {"url": "http://example.com/image.png", "name": "example image"},
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
            "image": {"url": "http://example.com/image.png", "name": "example image"},
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
            "image": None,
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


def test_put_missing_required_in_item(client: TestClient):
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


def test_put_missing_required_in_image(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "price": 35.4,
            "image": {"url": "http://example.com/image.png"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "image", "name"],
                "input": {"url": "http://example.com/image.png"},
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_put_wrong_url(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "price": 35.4,
            "image": {"url": "not a valid url", "name": "example image"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "image", "url"],
                "input": "not a valid url",
                "msg": "Input should be a valid URL, relative URL without a base",
                "type": "url_parsing",
                "ctx": {"error": "relative URL without a base"},
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
                        "image": {
                            "anyOf": [
                                {"$ref": "#/components/schemas/Image"},
                                {"type": "null"},
                            ],
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
