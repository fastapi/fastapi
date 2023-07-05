from fastapi import Depends, FastAPI, Security
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

oid = OpenIdConnect(openIdConnectUrl="/openid")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(oid)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


client = TestClient(app)


def test_security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "Bearer footokenbar"}


def test_security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "Other footokenbar"}


def test_security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not authenticated"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users/me": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read Current User",
                    "operationId": "read_current_user_users_me_get",
                    "security": [{"OpenIdConnect": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {
                "OpenIdConnect": {
                    "type": "openIdConnect",
                    "openIdConnectUrl": "/openid",
                }
            }
        },
    }
