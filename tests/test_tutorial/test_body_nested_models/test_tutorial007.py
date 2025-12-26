import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial007_py39"),
        pytest.param("tutorial007_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_nested_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_all(client: TestClient):
    data = {
        "name": "Special Offer",
        "description": "This is a special offer",
        "price": 38.6,
        "items": [
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
                "tags": ["foo"],
                "images": [
                    {
                        "url": "http://example.com/image.png",
                        "name": "example image",
                    }
                ],
            }
        ],
    }

    response = client.post(
        "/offers/",
        json=data,
    )
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_put_only_required(client: TestClient):
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [
                {
                    "name": "Foo",
                    "price": 35.4,
                    "images": [
                        {
                            "url": "http://example.com/image.png",
                            "name": "example image",
                        }
                    ],
                }
            ],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Special Offer",
        "description": None,
        "price": 38.6,
        "items": [
            {
                "name": "Foo",
                "description": None,
                "price": 35.4,
                "tax": None,
                "tags": [],
                "images": [
                    {
                        "url": "http://example.com/image.png",
                        "name": "example image",
                    }
                ],
            }
        ],
    }


def test_put_empty_body(client: TestClient):
    response = client.post(
        "/offers/",
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
            {
                "loc": ["body", "items"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_put_missing_required_in_items(client: TestClient):
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [{}],
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "items", 0, "name"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
            {
                "loc": ["body", "items", 0, "price"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_put_missing_required_in_images(client: TestClient):
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [
                {"name": "Foo", "price": 35.4, "images": [{}]},
            ],
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "items", 0, "images", 0, "url"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
            },
            {
                "loc": ["body", "items", 0, "images", 0, "name"],
                "input": {},
                "msg": "Field required",
                "type": "missing",
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
            "/offers/": {
                "post": {
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
                    "summary": "Create Offer",
                    "operationId": "create_offer_offers__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Offer",
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
                "Offer": {
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
                        "items": {
                            "title": "Items",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Item"},
                        },
                    },
                    "required": ["name", "price", "items"],
                    "title": "Offer",
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
