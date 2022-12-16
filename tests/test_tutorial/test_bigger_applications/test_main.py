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
                "tags": ["users"],
                "summary": "Read Users",
                "operationId": "read_users_users__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    }
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
        "/users/me": {
            "get": {
                "tags": ["users"],
                "summary": "Read User Me",
                "operationId": "read_user_me_users_me_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    }
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
        "/users/{username}": {
            "get": {
                "tags": ["users"],
                "summary": "Read User",
                "operationId": "read_user_users__username__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Username", "type": "string"},
                        "name": "username",
                        "in": "path",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
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
        "/items/": {
            "get": {
                "tags": ["items"],
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "404": {"description": "Not found"},
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
        "/items/{item_id}": {
            "get": {
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
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "404": {"description": "Not found"},
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
            "put": {
                "tags": ["items", "custom"],
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
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "404": {"description": "Not found"},
                    "403": {"description": "Operation forbidden"},
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
        "/admin/": {
            "post": {
                "tags": ["admin"],
                "summary": "Update Admin",
                "operationId": "update_admin_admin__post",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "418": {"description": "I'm a teapot"},
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
        "/": {
            "get": {
                "summary": "Root",
                "operationId": "root__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Token", "type": "string"},
                        "name": "token",
                        "in": "query",
                    }
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


no_jessica = {
    "detail": [
        {
            "loc": ["query", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response,headers",
    [
        (
            "/users?token=jessica",
            200,
            [{"username": "Rick"}, {"username": "Morty"}],
            {},
        ),
        ("/users", 422, no_jessica, {}),
        ("/users/foo?token=jessica", 200, {"username": "foo"}, {}),
        ("/users/foo", 422, no_jessica, {}),
        ("/users/me?token=jessica", 200, {"username": "fakecurrentuser"}, {}),
        ("/users/me", 422, no_jessica, {}),
        (
            "/users?token=monica",
            400,
            {"detail": "No Jessica token provided"},
            {},
        ),
        (
            "/items?token=jessica",
            200,
            {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}},
            {"X-Token": "fake-super-secret-token"},
        ),
        ("/items", 422, no_jessica, {"X-Token": "fake-super-secret-token"}),
        (
            "/items/plumbus?token=jessica",
            200,
            {"name": "Plumbus", "item_id": "plumbus"},
            {"X-Token": "fake-super-secret-token"},
        ),
        (
            "/items/bar?token=jessica",
            404,
            {"detail": "Item not found"},
            {"X-Token": "fake-super-secret-token"},
        ),
        ("/items/plumbus", 422, no_jessica, {"X-Token": "fake-super-secret-token"}),
        (
            "/items?token=jessica",
            400,
            {"detail": "X-Token header invalid"},
            {"X-Token": "invalid"},
        ),
        (
            "/items/bar?token=jessica",
            400,
            {"detail": "X-Token header invalid"},
            {"X-Token": "invalid"},
        ),
        (
            "/items?token=jessica",
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
            "/items/plumbus?token=jessica",
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
        ("/?token=jessica", 200, {"message": "Hello Bigger Applications!"}, {}),
        ("/", 422, no_jessica, {}),
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
                "loc": ["query", "token"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["header", "x-token"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_put_invalid_header():
    response = client.put("/items/foo", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


def test_put():
    response = client.put(
        "/items/plumbus?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "plumbus", "name": "The great Plumbus"}


def test_put_forbidden():
    response = client.put(
        "/items/bar?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "You can only update the item: plumbus"}


def test_admin():
    response = client.post(
        "/admin/?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Admin getting schwifty"}


def test_admin_invalid_header():
    response = client.post("/admin/", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}
