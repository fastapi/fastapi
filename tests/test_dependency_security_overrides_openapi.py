from fastapi import Depends, FastAPI, Header
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient

app = FastAPI()


def get_user_id() -> int:
    pass  # pragma: no cover


def get_user(user_id=Depends(get_user_id)):
    pass  # pragma: no cover


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_id_from_auth_override(token: str = Depends(oauth2_scheme)):
    pass  # pragma: no cover


def get_user_id_from_header_override(user_id: int = Header()):
    pass  # pragma: no cover


@app.get("/user")
def read_user(
    user: str = Depends(get_user),
):
    pass  # pragma: no cover


client = TestClient(app)


override_with_security_schema = {
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                "type": "oauth2",
            }
        }
    },
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.1.0",
    "paths": {
        "/user": {
            "get": {
                "operationId": "read_user_user_get",
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful " "Response",
                    }
                },
                "security": [{"OAuth2PasswordBearer": []}],
                "summary": "Read User",
            }
        }
    },
}


def test_override_with_security():
    app.dependency_overrides[get_user_id] = get_user_id_from_auth_override
    app.openapi_schema = None
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == override_with_security_schema


override_with_header_schema = {
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "title": "Detail",
                        "type": "array",
                    }
                },
                "title": "HTTPValidationError",
                "type": "object",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                        "title": "Location",
                        "type": "array",
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error " "Type", "type": "string"},
                },
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
                "type": "object",
            },
        }
    },
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.1.0",
    "paths": {
        "/user": {
            "get": {
                "operationId": "read_user_user_get",
                "parameters": [
                    {
                        "in": "header",
                        "name": "user-id",
                        "required": True,
                        "schema": {"title": "User-Id", "type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful " "Response",
                    },
                    "422": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                        "description": "Validation " "Error",
                    },
                },
                "summary": "Read User",
            }
        }
    },
}


def test_override_with_header():
    app.dependency_overrides[get_user_id] = get_user_id_from_header_override
    app.openapi_schema = None
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == override_with_header_schema
