import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_py310", marks=needs_py310),
        pytest.param("tutorial005_an_py39"),
        pytest.param("tutorial005_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_multiple_params.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_all(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": "Some Foo",
                "tax": 0.1,
            },
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": "Some Foo",
            "tax": 0.1,
        },
    }


def test_post_required(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "item": {"name": "Foo", "price": 50.5},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        },
    }


def test_post_no_body(client: TestClient):
    response = client.put("/items/5", json=None)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": [
                    "body",
                    "item",
                ],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


def test_post_like_not_embeded(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "price": 50.5,
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": [
                    "body",
                    "item",
                ],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


def test_post_missing_required_field_in_item(client: TestClient):
    response = client.put(
        "/items/5", json={"item": {"name": "Foo"}, "user": {"username": "johndoe"}}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"name": "Foo"},
                "loc": [
                    "body",
                    "item",
                    "price",
                ],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/items/{item_id}": {
                "put": {
                    "operationId": "update_item_items__item_id__put",
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
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_update_item_items__item_id__put",
                                },
                            },
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
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
                    "summary": "Update Item",
                },
            },
        },
        "components": {
            "schemas": {
                "Body_update_item_items__item_id__put": {
                    "properties": {
                        "item": {
                            "$ref": "#/components/schemas/Item",
                        },
                    },
                    "required": ["item"],
                    "title": "Body_update_item_items__item_id__put",
                    "type": "object",
                },
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
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                        "description": {
                            "title": "Description",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "price": {"title": "Price", "type": "number"},
                        "tax": {
                            "title": "Tax",
                            "anyOf": [{"type": "number"}, {"type": "null"}],
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
