# Ref: https://github.com/fastapi/fastapi/issues/14454

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="authorize",
    tokenUrl="token",
    auto_error=True,
    scopes={"read": "Read access", "write": "Write access"},
)


async def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


app = FastAPI(dependencies=[Depends(get_token)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/with-oauth2-scheme",
    dependencies=[Security(oauth2_scheme, scopes=["read", "write"])],
)
async def read_with_oauth2_scheme():
    return {"message": "Admin Access"}


@app.get(
    "/with-get-token", dependencies=[Security(get_token, scopes=["read", "write"])]
)
async def read_with_get_token():
    return {"message": "Admin Access"}


router = APIRouter(dependencies=[Security(oauth2_scheme, scopes=["read"])])


@router.get("/items/")
async def read_items(token: Optional[str] = Depends(oauth2_scheme)):
    return {"token": token}


@router.post("/items/")
async def create_item(
    token: Optional[str] = Security(oauth2_scheme, scopes=["read", "write"]),
):
    return {"token": token}


app.include_router(router)

client = TestClient(app)


def test_root():
    response = client.get("/", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World"}


def test_read_with_oauth2_scheme():
    response = client.get(
        "/with-oauth2-scheme", headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Admin Access"}


def test_read_with_get_token():
    response = client.get(
        "/with-get-token", headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Admin Access"}


def test_read_token():
    response = client.get("/items/", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}


def test_create_token():
    response = client.post("/items/", headers={"Authorization": "Bearer testtoken"})
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
                "/": {
                    "get": {
                        "summary": "Root",
                        "operationId": "root__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [{"OAuth2AuthorizationCodeBearer": []}],
                    }
                },
                "/with-oauth2-scheme": {
                    "get": {
                        "summary": "Read With Oauth2 Scheme",
                        "operationId": "read_with_oauth2_scheme_with_oauth2_scheme_get",
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
                },
                "/with-get-token": {
                    "get": {
                        "summary": "Read With Get Token",
                        "operationId": "read_with_get_token_with_get_token_get",
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
                },
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
                    },
                    "post": {
                        "summary": "Create Item",
                        "operationId": "create_item_items__post",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "security": [
                            {"OAuth2AuthorizationCodeBearer": ["read", "write"]},
                        ],
                    },
                },
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
