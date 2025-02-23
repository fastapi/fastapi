from fastapi.testclient import TestClient

from docs_src.security.tutorial009 import app

# IDENTICAL COPY of tests/test_security_api_key_cookie.py


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Current User",
                "operationId": "read_current_user_users_me_get",
                "security": [{"APIKeyCookie": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "APIKeyCookie": {"type": "apiKey", "name": "key", "in": "cookie"}
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_api_key():
    response = client.get("/users/me", cookies={"key": "secret"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "secret"}


def test_security_api_key_no_key():
    response = client.get("/users/me")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}
