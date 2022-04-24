from fastapi.testclient import TestClient

from docs_src.security.tutorial008 import app

client = TestClient(app)

openapi_schema = {
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/health": {
      "get": {
        "summary": "Endpoint",
        "operationId": "endpoint_health_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                }
              }
            }
          }
        },
        "security": [
          {
            "APIKeyHeader": []
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "APIKeyHeader": {
        "type": "apiKey",
        "description": "Mandatory API Token, required for all endpoints",
        "in": "header",
        "name": "X-API-KEY"
      }
    }
  }
}



def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_security_apikey_header():
    auth = {"X-API-KEY": "randomized-string-1234"}
    response = client.get("/health", headers=auth)
    assert response.status_code == 200, response.text
    assert response.json() == {"Hello": "World"}


def test_security_apikey_header_no_credentials():
    response = client.get("/health", headers={})
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 403, response.text


def test_security_apikey_header_invalid_credentials():
    auth = {"X-API-KEY": "totally-wrong-api-key"}
    response = client.get("/health", headers=auth)
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Invalid API Key"}
