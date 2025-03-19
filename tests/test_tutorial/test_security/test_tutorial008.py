from fastapi.testclient import TestClient

from docs_src.security.tutorial008 import app

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
                "security": [{"APIKeyHeader": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "APIKeyHeader": {
                "type": "apiKey",
                "description": "API Key required to access secure endpoints.",
                "in": "header",
                "name": "X-API-Key",
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_apikey_header():
    auth = {"X-API-KEY": "mysecretapikey"}
    response = client.get("/secure-data", headers=auth)
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "You have access to secure data"}


def test_apikey_header_no_credentials():
    response = client.get("/secure-data", headers={})
    # TODO: this should be 401 in the implementation! discuss with @tiangolo et al
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_apikey_header_invalid_credentials():
    auth = {"X-API-KEY": "totally-wrong-api-key"}
    response = client.get("/secure-data", headers=auth)
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid API Key"}
