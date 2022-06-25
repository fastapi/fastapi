from typing import Optional

from fastapi import FastAPI, Security
from fastapi.security import (
    HTTPBasicClientCredentials,
    OAuth2ClientCredentials,
    OAuth2ClientCredentialsRequestForm,
)
from fastapi.testclient import TestClient

app = FastAPI()

oauth2_scheme = OAuth2ClientCredentials(tokenUrl="token", auto_error=True)

token_scheme = HTTPBasicClientCredentials(
    auto_error=False, scheme_name="oAuth2ClientCredentials"
)


@app.get("/items/")
async def read_items(token: Optional[str] = Security(oauth2_scheme)):
    if token:
        return {"token": token}


# @app.post("/token")
# def create_access_token(
#     form: OAuth2ClientCredentialsRequestForm = Depends(),
#     basic_credentials: Optional[HTTPClientCredentials] = Depends(token_scheme),
# ):
#     if form.client_id and form.client_secret:
#         client_id = form.client_id
#         client_secret = form.client_secret
#     elif basic_credentials:
#         client_id = basic_credentials.client_id
#         client_secret = basic_credentials.client_secret
#     else:
#         HTTPException(status_code=400, detail="Client credentials not provided")
#     return {"token": "jwt_token"}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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
                "security": [{"oAuth2ClientCredentials": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "oAuth2ClientCredentials": {
                "type": "oauth2",
                "flows": {
                    "clientCredentials": {
                        "tokenUrl": "token",
                        "scopes": {},
                    }
                },
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


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


def test_no_return_none():
    oauth2_scheme.auto_error = False
    response = client.get("/items")
    assert response.status_code == 200, response.text
    assert response.json() is None
    oauth2_scheme.auto_error = True


def test_client_credentials_form():
    form = OAuth2ClientCredentialsRequestForm(
        client_id="client_id", client_secret="client_secret", scope="profile"
    )
    assert form.grant_type
    assert form.scopes
    assert form.client_id
    assert form.client_secret
