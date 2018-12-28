from starlette.testclient import TestClient

from response_model.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/user/": {
            "post": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserOut"}
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
                "summary": "Create User Post",
                "operationId": "create_user_user__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserIn"}
                        }
                    },
                    "required": True,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "UserOut": {
                "title": "UserOut",
                "required": ["username", "email"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
                    "email": {"title": "Email", "type": "string", "format": "email"},
                    "full_name": {"title": "Full_Name", "type": "string"},
                },
            },
            "UserIn": {
                "title": "UserIn",
                "required": ["username", "password", "email"],
                "type": "object",
                "properties": {
                    "username": {"title": "Username", "type": "string"},
                    "password": {"title": "Password", "type": "string"},
                    "email": {"title": "Email", "type": "string", "format": "email"},
                    "full_name": {"title": "Full_Name", "type": "string"},
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_post_user():
    response = client.post(
        "/user/",
        json={
            "username": "foo",
            "password": "fighter",
            "email": "foo@example.com",
            "full_name": "Grave Dohl",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "foo",
        "email": "foo@example.com",
        "full_name": "Grave Dohl",
    }
