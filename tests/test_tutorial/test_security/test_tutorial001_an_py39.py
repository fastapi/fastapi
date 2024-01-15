import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.security.tutorial001_an_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_no_token(client: TestClient):
    response = client.get("/items")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@needs_py39
def test_token(client: TestClient):
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


@needs_py39
def test_incorrect_token(client: TestClient):
    response = client.get("/items", headers={"Authorization": "Notexistent testtoken"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "security": [{"OAuth2PasswordBearer": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "type": "oauth2",
                    "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                }
            }
        },
    }
