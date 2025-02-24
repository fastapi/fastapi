from fastapi.testclient import TestClient

from docs_src.security.tutorial009 import app


openapi_schema = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/secure-data": {
            "get": {
                "summary": "Secure Endpoint",
                "operationId": "secure_endpoint_secure_data_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "security": [{"APIKeyCookie": []}],
            },
        },
    },
    "components": {
        "securitySchemes": {
            "APIKeyCookie": {
                "type": "apiKey",
                "name": "X-API-KEY",
                "description": "API Key required to access secure endpoints.",
                "in": "cookie",
            },
        },
    },
}


def test_openapi_schema():
    client = TestClient(app, cookies={"X-API-KEY": "mysecretapikey"})
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_apikey_cookie():
    client = TestClient(app, cookies={"X-API-KEY": "mysecretapikey"})
    response = client.get("/secure-data")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "You have access to secure data"}


def test_apikey_cookie_no_key():
    client = TestClient(app)
    response = client.get("/secure-data")
    # TODO: this should be 401 in the implementation! discuss with @tiangolo et al
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}

def test_apikey_cookie_invalid_key():
    client = TestClient(app, cookies={"X-API-KEY": "wrongkey"})
    response = client.get("/secure-data")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid API Key"}
