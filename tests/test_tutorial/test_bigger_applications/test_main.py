import pytest
from fastapi.testclient import TestClient

from docs_src.bigger_applications.app.main import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "tags": ["users"],
                "summary": "Read Users",
                "operationId": "read_users_users__get",
            }
        },
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "tags": ["users"],
                "summary": "Read User Me",
                "operationId": "read_user_me_users_me_get",
            }
        },
        "/users/{username}": {
            "get": {
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
                "tags": ["users"],
                "summary": "Read User",
                "operationId": "read_user_users__username__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Username", "type": "string"},
                        "name": "username",
                        "in": "path",
                    }
                ],
            }
        },
        "/items/": {
            "get": {
                "responses": {
                    "404": {"description": "Not found"},
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
                "tags": ["items"],
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    }
                ],
            }
        },
        "/items/{item_id}": {
            "get": {
                "responses": {
                    "404": {"description": "Not found"},
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
                "tags": ["items"],
                "summary": "Read Item",
                "operationId": "read_item_items__item_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
            },
            "put": {
                "responses": {
                    "404": {"description": "Not found"},
                    "403": {"description": "Operation forbidden"},
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
                "tags": ["custom", "items"],
                "summary": "Update Item",
                "operationId": "update_item_items__item_id__put",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
            },
        },
    },
    "components": {
        "schemas": {
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
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


@pytest.mark.parametrize(
    "path,expected_status,expected_response,headers",
    [
        ("/users", 200, [{"username": "Foo"}, {"username": "Bar"}], {}),
        ("/users/foo", 200, {"username": "foo"}, {}),
        ("/users/me", 200, {"username": "fakecurrentuser"}, {}),
        (
            "/items",
            200,
            [{"name": "Item Foo"}, {"name": "item Bar"}],
            {"X-Token": "fake-super-secret-token"},
        ),
        (
            "/items/bar",
            200,
            {"name": "Fake Specific Item", "item_id": "bar"},
            {"X-Token": "fake-super-secret-token"},
        ),
        ("/items", 400, {"detail": "X-Token header invalid"}, {"X-Token": "invalid"}),
        (
            "/items/bar",
            400,
            {"detail": "X-Token header invalid"},
            {"X-Token": "invalid"},
        ),
        (
            "/items",
            422,
            {
                "detail": [
                    {
                        "loc": ["header", "x-token"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
            {},
        ),
        (
            "/items/bar",
            422,
            {
                "detail": [
                    {
                        "loc": ["header", "x-token"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
            {},
        ),
        ("/openapi.json", 200, openapi_schema, {}),
    ],
)
def test_get_path(path, expected_status, expected_response, headers):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_put_no_header():
    response = client.put("/items/foo")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["header", "x-token"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_put_invalid_header():
    response = client.put("/items/foo", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


def test_put():
    response = client.put("/items/foo", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "name": "The Fighters"}


def test_put_forbidden():
    response = client.put("/items/bar", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "You can only update the item: foo"}
