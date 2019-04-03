from typing import Optional

from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()

api_key = APIKeyHeader(name="key", auto_error=False)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: Optional[str] = Security(api_key)):
    if oauth_header is None:
        return None
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: Optional[User] = Depends(get_current_user)):
    if current_user is None:
        return {"msg": "Create an account first"}
    return current_user


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/users/me": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Current User Get",
                "operationId": "read_current_user_users_me_get",
                "security": [{"APIKeyHeader": []}],
            }
        }
    },
    "components": {
        "securitySchemes": {
            "APIKeyHeader": {"type": "apiKey", "name": "key", "in": "header"}
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_security_api_key():
    response = client.get("/users/me", headers={"key": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "secret"}


def test_security_api_key_no_key():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"msg": "Create an account first"}
