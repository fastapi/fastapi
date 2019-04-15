import pytest
from starlette.testclient import TestClient

from bigger_applications.app.main import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                },
                "tags": ["items"],
                "summary": "Read Items",
                "operationId": "read_items_items__get",
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
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
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
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
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
    "path,expected_status,expected_response",
    [
        ("/users", 200, [{"username": "Foo"}, {"username": "Bar"}]),
        ("/users/foo", 200, {"username": "foo"}),
        ("/users/me", 200, {"username": "fakecurrentuser"}),
        ("/items", 200, [{"name": "Item Foo"}, {"name": "item Bar"}]),
        ("/items/bar", 200, {"name": "Fake Specific Item", "item_id": "bar"}),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_put():
    response = client.put("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo", "name": "The Fighters"}


def test_put_forbidden():
    response = client.put("/items/bar")
    assert response.status_code == 403
    assert response.json() == {"detail": "You can only update the item: foo"}
