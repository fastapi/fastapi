import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.bigger_applications.app_an_py39.main import app

    client = TestClient(app)
    return client


@needs_py39
def test_users_token_jessica(client: TestClient):
    response = client.get("/users?token=jessica")
    assert response.status_code == 200
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]


@needs_py39
def test_users_with_no_token(client: TestClient):
    response = client.get("/users")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_users_foo_token_jessica(client: TestClient):
    response = client.get("/users/foo?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"username": "foo"}


@needs_py39
def test_users_foo_with_no_token(client: TestClient):
    response = client.get("/users/foo")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_users_me_token_jessica(client: TestClient):
    response = client.get("/users/me?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"username": "fakecurrentuser"}


@needs_py39
def test_users_me_with_no_token(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_users_token_monica_with_no_jessica(client: TestClient):
    response = client.get("/users?token=monica")
    assert response.status_code == 400
    assert response.json() == {"detail": "No Jessica token provided"}


@needs_py39
def test_items_token_jessica(client: TestClient):
    response = client.get(
        "/items?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "plumbus": {"name": "Plumbus"},
        "gun": {"name": "Portal Gun"},
    }


@needs_py39
def test_items_with_no_token_jessica(client: TestClient):
    response = client.get("/items", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_items_plumbus_token_jessica(client: TestClient):
    response = client.get(
        "/items/plumbus?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Plumbus", "item_id": "plumbus"}


@needs_py39
def test_items_bar_token_jessica(client: TestClient):
    response = client.get(
        "/items/bar?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@needs_py39
def test_items_plumbus_with_no_token(client: TestClient):
    response = client.get(
        "/items/plumbus", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_items_with_invalid_token(client: TestClient):
    response = client.get("/items?token=jessica", headers={"X-Token": "invalid"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


@needs_py39
def test_items_bar_with_invalid_token(client: TestClient):
    response = client.get("/items/bar?token=jessica", headers={"X-Token": "invalid"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


@needs_py39
def test_items_with_missing_x_token_header(client: TestClient):
    response = client.get("/items?token=jessica")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                }
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
                }
            ]
        }
    )


@needs_py39
def test_items_plumbus_with_missing_x_token_header(client: TestClient):
    response = client.get("/items/plumbus?token=jessica")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                }
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
                }
            ]
        }
    )


@needs_py39
def test_root_token_jessica(client: TestClient):
    response = client.get("/?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}


@needs_py39
def test_root_with_no_token(client: TestClient):
    response = client.get("/")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "token"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py39
def test_put_no_header(client: TestClient):
    response = client.put("/items/foo")
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
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
    )


@needs_py39
def test_put_invalid_header(client: TestClient):
    response = client.put("/items/foo", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


@needs_py39
def test_put(client: TestClient):
    response = client.put(
        "/items/plumbus?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "plumbus", "name": "The great Plumbus"}


@needs_py39
def test_put_forbidden(client: TestClient):
    response = client.put(
        "/items/bar?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "You can only update the item: plumbus"}


@needs_py39
def test_admin(client: TestClient):
    response = client.post(
        "/admin/?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Admin getting schwifty"}


@needs_py39
def test_admin_invalid_header(client: TestClient):
    response = client.post("/admin/", headers={"X-Token": "invalid"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "X-Token header invalid"}


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
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
