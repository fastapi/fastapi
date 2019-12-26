from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class Detail(BaseModel):
    detail: str


class User(BaseModel):
    id: int
    name: str


class GetUser:
    __responses__ = {401: {"model": Detail}}

    async def __call__(self, user_id: int) -> User:
        raise HTTPException(401, detail="user_id doesn't exists")


get_user = GetUser()


@app.get("/", response_model=User)
def get_user(user: User = Depends(get_user)):
    return user  # pragma: nocover


client = TestClient(app)

openapi_schema = {
    "components": {
        "schemas": {
            "Detail": {
                "properties": {"detail": {"title": "Detail", "type": "string"}},
                "required": ["detail"],
                "title": "Detail",
                "type": "object",
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "title": "Detail",
                        "type": "array",
                    }
                },
                "title": "HTTPValidationError",
                "type": "object",
            },
            "User": {
                "properties": {
                    "id": {"title": "Id", "type": "integer"},
                    "name": {"title": "Name", "type": "string"},
                },
                "required": ["id", "name"],
                "title": "User",
                "type": "object",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"type": "string"},
                        "title": "Location",
                        "type": "array",
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error " "Type", "type": "string"},
                },
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
                "type": "object",
            },
        }
    },
    "info": {"title": "Fast API", "version": "0.1.0"},
    "openapi": "3.0.2",
    "paths": {
        "/": {
            "get": {
                "operationId": "get_user__get",
                "parameters": [
                    {
                        "in": "query",
                        "name": "user_id",
                        "required": True,
                        "schema": {"title": "User Id", "type": "integer"},
                    }
                ],
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        },
                        "description": "Successful " "Response",
                    },
                    "401": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Detail"}
                            }
                        },
                        "description": "Unauthorized",
                    },
                    "422": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                        "description": "Validation " "Error",
                    },
                },
                "summary": "Get User",
            }
        }
    },
}


def test_additional_properties_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_additional_properties_post():
    response = client.get("/", params={"user_id": 1})
    assert response.status_code == 401
    assert response.json() == {"detail": "user_id doesn't exists"}
