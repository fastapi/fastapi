from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from fastapi.security.base import SecurityBase
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.requests import Request

app = FastAPI()


class User(BaseModel):
    username: str


class CustomOauth2(SecurityBase):
    def __init__(self):
        self.scheme_name: str = "My Custom Oauth2 schema"
        self.oauth = OAuth2AuthorizationCodeBearer(
            authorizationUrl="https://some-url.com/authorization",
            tokenUrl="https://some-url.com/token",
            scopes={"read:users": "Read the users", "write:users": "Create users"},
            scheme_name="CustomOauth2",
            auto_error=True,
        )
        self.model = self.oauth.model

    async def __call__(self, request: Request, security_scopes: SecurityScopes) -> User:
        return User(username="test")


reusable_custom_oauth2 = CustomOauth2()


@app.get(
    "/users/me",
    dependencies=[
        Security(reusable_custom_oauth2, scopes=["read:users", "not:valid:scope"])
    ],
)
# Here we use string annotations to test them
def read_current_user(current_user: "User" = Depends(reusable_custom_oauth2)):
    return current_user


client = TestClient(app)

openapi_schema = {
    "components": {
        "securitySchemes": {
            "My Custom Oauth2 schema": {
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": "https://some-url.com/authorization",
                        "scopes": {
                            "read:users": "Read " "the " "users",
                            "write:users": "Create " "users",
                        },
                        "tokenUrl": "https://some-url.com/token",
                    }
                },
                "type": "oauth2",
            }
        }
    },
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.0.2",
    "paths": {
        "/users/me": {
            "get": {
                "operationId": "read_current_user_users_me_get",
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful " "Response",
                    }
                },
                "security": [
                    {"My Custom Oauth2 schema": ["read:users", "not:valid:scope"]}
                ],
                "summary": "Read Current User",
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_user_is_returned_custom_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"username": "test"}
