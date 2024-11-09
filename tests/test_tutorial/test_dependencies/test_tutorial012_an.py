from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial012_an import app

client = TestClient(app)


def test_get_no_headers_items():
    response = client.get("/items/")
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-key"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["header", "x-token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["header", "x-key"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_get_no_headers_users():
    response = client.get("/users/")
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-key"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["header", "x-token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["header", "x-key"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_get_invalid_one_header_items():
    response = client.get("/items/", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


def test_get_invalid_one_users():
    response = client.get("/users/", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


def test_get_invalid_second_header_items():
    response = client.get(
        "/items/", headers={"X-Token": "fake-super-secret-token", "X-Key": "invalid"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Key header invalid"}


def test_get_invalid_second_header_users():
    response = client.get(
        "/users/", headers={"X-Token": "fake-super-secret-token", "X-Key": "invalid"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Key header invalid"}


def test_get_valid_headers_items():
    response = client.get(
        "/items/",
        headers={
            "X-Token": "fake-super-secret-token",
            "X-Key": "fake-super-secret-key",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"item": "Portal Gun"}, {"item": "Plumbus"}]


def test_get_valid_headers_users():
    response = client.get(
        "/users/",
        headers={
            "X-Token": "fake-super-secret-token",
            "X-Key": "fake-super-secret-key",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "X-Token", "type": "string"},
                            "name": "x-token",
                            "in": "header",
                        },
                        {
                            "required": True,
                            "schema": {"title": "X-Key", "type": "string"},
                            "name": "x-key",
                            "in": "header",
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
                }
            },
            "/users/": {
                "get": {
                    "summary": "Read Users",
                    "operationId": "read_users_users__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "X-Token", "type": "string"},
                            "name": "x-token",
                            "in": "header",
                        },
                        {
                            "required": True,
                            "schema": {"title": "X-Key", "type": "string"},
                            "name": "x-key",
                            "in": "header",
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
                }
            },
        },
        "components": {
            "schemas": {
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
            }
        },
    }
