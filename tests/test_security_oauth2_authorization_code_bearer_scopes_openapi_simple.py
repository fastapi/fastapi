# Ref: https://github.com/fastapi/fastapi/issues/14454

from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="api/oauth/authorize",
    tokenUrl="/api/oauth/token",
    scopes={"read": "Read access", "write": "Write access"},
)


async def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


app = FastAPI(dependencies=[Depends(get_token)])


@app.get("/admin", dependencies=[Security(get_token, scopes=["read", "write"])])
async def read_admin():
    return {"message": "Admin Access"}


client = TestClient(app)


def test_read_admin():
    response = client.get("/admin", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Admin Access"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/admin": {
                    "get": {
                        "summary": "Read Admin",
                        "operationId": "read_admin_admin_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [
                            {"OAuth2AuthorizationCodeBearer": ["read", "write"]}
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
                                "authorizationUrl": "api/oauth/authorize",
                                "tokenUrl": "/api/oauth/token",
                            }
                        },
                    }
                }
            },
        }
    )
