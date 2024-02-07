from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyQuery
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

api_key = APIKeyQuery(name="key", description="API Key Query")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


client = TestClient(app)


def test_security_api_key():
    response = client.get("/users/me?key=secret")
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "secret"}


def test_security_api_key_no_key():
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
                    "security": [{"APIKeyQuery": []}],
                }
            }
        },
        "components": {
            "securitySchemes": {
                "APIKeyQuery": {
                    "type": "apiKey",
                    "name": "key",
                    "in": "query",
                    "description": "API Key Query",
                }
            }
        },
    }
