from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def user_exists(user_id: int):
    return True


@app.get("/users/{user_id}", dependencies=[Depends(user_exists)])
async def read_users(user_id: int):
    pass


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/users/{user_id}": {
            "get": {
                "summary": "Read Users",
                "operationId": "read_users_users__user_id__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "User Id", "type": "integer"},
                        "name": "user_id",
                        "in": "path",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_reused_param():
    response = client.get("/openapi.json")
    data = response.json()
    assert data == openapi_schema


def test_read_users():
    response = client.get("/users/42")
    assert response.status_code == 200, response.text
