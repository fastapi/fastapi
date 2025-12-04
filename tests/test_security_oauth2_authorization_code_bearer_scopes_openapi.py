# Ref: https://github.com/fastapi/fastapi/issues/14454

from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="authorize",
    tokenUrl="token",
    auto_error=True,
    scopes={"read": "Read access", "write": "Write access"},
)

app = FastAPI(dependencies=[Security(oauth2_scheme)])


@app.get("/items/")
async def read_items(token: Optional[str] = Security(oauth2_scheme, scopes=["read"])):
    return {"token": token}


client = TestClient(app)


def test_token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "get": {
                        "summary": "Read Items",
                        "operationId": "read_items_items__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [
                            {"OAuth2AuthorizationCodeBearer": ["read"]},
                        ],
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "OAuth2AuthorizationCodeBearer": {
                        "type": "oauth2",
                        "flows": {
                            "authorizationCode": {
                                "scopes": {
                                    "read": "Read access",
                                    "write": "Write access",
                                },
                                "authorizationUrl": "authorize",
                                "tokenUrl": "token",
                            }
                        },
                    }
                }
            },
        }
    )
