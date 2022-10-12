import importlib
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/": {
            "post": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
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
                "summary": "Create User",
                "operationId": "create_user_users__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserCreate"}
                        }
                    },
                    "required": True,
                },
            },
        },
        "/users/{user_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
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
                "summary": "Read User",
                "operationId": "read_user_users__user_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "User Id", "type": "integer"},
                        "name": "user_id",
                        "in": "path",
                    }
                ],
            }
        },
    },
    "components": {
        "schemas": {
            "User": {
                "title": "User",
                "required": ["email", "id", "is_active"],
                "type": "object",
                "properties": {
                    "email": {"title": "Email", "type": "string"},
                    "id": {"title": "Id", "type": "integer"},
                    "is_active": {"title": "Is Active", "type": "boolean"},
                },
            },
            "UserCreate": {
                "title": "UserCreate",
                "required": ["email", "password"],
                "type": "object",
                "properties": {
                    "email": {"title": "Email", "type": "string"},
                    "password": {"title": "Password", "type": "string"},
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


@pytest.fixture(scope="module")
def client(tmp_path_factory: pytest.TempPathFactory):
    tmp_path = tmp_path_factory.mktemp("data")
    cwd = os.getcwd()
    os.chdir(tmp_path)
    TEST_DB_NAME = "sql_app.db"
    test_db = Path(f"./{TEST_DB_NAME}")
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    # Import while creating the client to create the DB after starting the test session
    from docs_src.sql_databases.sql_app_contextvar.config import Config

    Config.SQLALCHEMY_DATABASE_URL = f"sqlite:///./{TEST_DB_NAME}"
    from docs_src.sql_databases.sql_app_contextvar import main

    # Ensure import side effects are re-executed
    importlib.reload(main)
    with TestClient(main.app) as c:
        yield c
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    os.chdir(cwd)


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_create_user(client):
    test_user = {"email": "johndoe@example.com", "password": "secret"}
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200, response.text
    data = response.json()
    assert test_user["email"] == data["email"]
    assert "id" in data
    response = client.post("/users/", json=test_user)
    assert response.status_code == 400, response.text


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "email" in data
    assert "id" in data


def test_inexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == 404, response.text
