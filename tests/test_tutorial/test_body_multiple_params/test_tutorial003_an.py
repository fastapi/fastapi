import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_multiple_params.tutorial003_an import app

    client = TestClient(app)
    return client


def test_post_body_valid(client: TestClient):
    response = client.put(
        "/items/5",
        json={
            "importance": 2,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 5,
        "importance": 2,
        "item": {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        },
        "user": {"username": "Dave", "full_name": None},
    }


def test_post_body_no_data(client: TestClient):
    response = client.put("/items/5", json=None)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "item"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
                {
                    "type": "missing",
                    "loc": ["body", "user"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
                {
                    "type": "missing",
                    "loc": ["body", "importance"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "item"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "user"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "importance"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_post_body_empty_list(client: TestClient):
    response = client.put("/items/5", json=[])
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "item"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
                {
                    "type": "missing",
                    "loc": ["body", "user"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
                {
                    "type": "missing",
                    "loc": ["body", "importance"],
                    "msg": "Field required",
                    "input": None,
                    "url": match_pydantic_error_url("missing"),
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "item"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "user"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "importance"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "put": {
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
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "integer"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
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
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Description", "type": "string"}
                        ),
                        "price": {"title": "Price", "type": "number"},
                        "tax": IsDict(
                            {
                                "title": "Tax",
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Tax", "type": "number"}
                        ),
                    },
                },
                "User": {
                    "title": "User",
                    "required": ["username"],
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "full_name": IsDict(
                            {
                                "title": "Full Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Full Name", "type": "string"}
                        ),
                    },
                },
                "Body_update_item_items__item_id__put": {
                    "title": "Body_update_item_items__item_id__put",
                    "required": ["item", "user", "importance"],
                    "type": "object",
                    "properties": {
                        "item": {"$ref": "#/components/schemas/Item"},
                        "user": {"$ref": "#/components/schemas/User"},
                        "importance": {"title": "Importance", "type": "integer"},
                    },
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
