from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import OAuth2ClientCredentials
from fastapi.testclient import TestClient

app = FastAPI()

oauth2_scheme = OAuth2ClientCredentials(
    tokenUrl="token",
    description="OAuth2 Client Credentials Flow",
    auto_error=True,
)


@app.get("/items/")
async def read_items(token: Optional[str] = Security(oauth2_scheme)):
    return {"token": token}


client = TestClient(app)


def test_no_token():
    response = client.get("/items")
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_incorrect_token():
    response = client.get("/items", headers={"Authorization": "Non-existent testtoken"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_openapi_schema():
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
                    "security": [{"OAuth2ClientCredentials": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {
                "OAuth2ClientCredentials": {
                    "type": "oauth2",
                    "flows": {
                        "clientCredentials": {
                            "tokenUrl": "token",
                            "scopes": {},
                        }
                    },
                    "description": "OAuth2 Client Credentials Flow",
                }
            }
        },
    }
