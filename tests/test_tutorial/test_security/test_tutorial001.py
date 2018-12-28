from starlette.testclient import TestClient

from security.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Items Get",
                "operationId": "read_items_items__get",
                "security": [{"OAuth2PasswordBearer": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {"password": {"scopes": {}, "tokenUrl": "/token"}},
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_no_token():
    response = client.get("/items")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json() == {"token": "testtoken"}


def test_incorrect_token():
    response = client.get("/items", headers={"Authorization": "Notexistent testtoken"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
