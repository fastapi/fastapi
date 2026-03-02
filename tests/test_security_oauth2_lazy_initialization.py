# Ref: https://github.com/fastapi/fastapi/issues/3317

from fastapi import APIRouter, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from fastapi.testclient import TestClient

auth_code_scheme = OAuth2AuthorizationCodeBearer()
auth_code_router = APIRouter()


@auth_code_router.get("/private-route")
async def private_route(
    token: str | None = Security(auth_code_scheme, scopes=["admin"]),
):
    return {"token": token}


def create_auth_code_app() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_code_router)
    auth_code_scheme.initialize(
        authorizationUrl="https://example.com/authorize",
        tokenUrl="https://example.com/oauth/token",
        scopes={"admin": "Admin access"},
    )
    return app


def test_oauth2_authorization_code_bearer_lazy_initialize():
    app = create_auth_code_app()
    client = TestClient(app)

    response = client.get(
        "/private-route", headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200, openapi.text
    authorization_code_flow = openapi.json()["components"]["securitySchemes"][
        "OAuth2AuthorizationCodeBearer"
    ]["flows"]["authorizationCode"]
    assert (
        authorization_code_flow["authorizationUrl"] == "https://example.com/authorize"
    )
    assert authorization_code_flow["tokenUrl"] == "https://example.com/oauth/token"
    assert authorization_code_flow["scopes"] == {"admin": "Admin access"}


password_scheme = OAuth2PasswordBearer()
password_router = APIRouter()


@password_router.get("/password-route")
async def password_route(token: str | None = Security(password_scheme)):
    return {"token": token}


def create_password_app() -> FastAPI:
    app = FastAPI()
    app.include_router(password_router)
    password_scheme.initialize(
        tokenUrl="https://example.com/oauth/token",
        scopes={"read": "Read access"},
    )
    return app


def test_oauth2_password_bearer_lazy_initialize():
    app = create_password_app()
    client = TestClient(app)

    response = client.get(
        "/password-route", headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "testtoken"}

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200, openapi.text
    password_flow = openapi.json()["components"]["securitySchemes"][
        "OAuth2PasswordBearer"
    ]["flows"]["password"]
    assert password_flow["tokenUrl"] == "https://example.com/oauth/token"
    assert password_flow["scopes"] == {"read": "Read access"}
