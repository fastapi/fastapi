from fastapi.testclient import TestClient

from docs_src.security.tutorial010 import app


client = TestClient(app)

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
                "security": [{"APIKeyQuery": []}],
            },
        },
    },
    "components": {
        "securitySchemes": {
            "APIKeyQuery": {
                "type": "apiKey",
                "name": "x-api-key",
                "description": "API Key required to access secure endpoints.",
                "in": "query",
            },
        },
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_api_key():
    response = client.get("/secure-data?x-api-key=mysecretapikey")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "You have access to secure data"}


def test_security_api_key_no_key():
    response = client.get("/secure-data")
    # TODO: this should be 401 in the implementation! discuss with @tiangolo et al
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_security_api_key_invalid_key():
    response = client.get("/secure-data?x-api-key=wrongkey")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid API Key"}
