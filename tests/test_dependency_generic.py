from typing import Generic, List, TypeVar

from fastapi import Body, Depends, FastAPI
from starlette.testclient import TestClient

T = TypeVar("T")
E = TypeVar("E")


# A simple generic class that holds a value of type T
class ValueHolder(Generic[T, E]):
    def __init__(self, x: List[E], y: T, z: int):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return self.x


app = FastAPI()


@app.post("/bar")
async def post_endpoint_bar(
    bar: ValueHolder[int, str] = Depends(), data: str = Body(..., embed=True)
):
    return bar.get()


client = TestClient(app)

open_api_foo = {
    "components": {
        "schemas": {
            "Body_post_endpoint_bar_bar_post": {
                "properties": {
                    "data": {"title": "Data", "type": "string"},
                    "x": {"items": {"type": "string"}, "title": "X", "type": "array"},
                },
                "required": ["data", "x"],
                "title": "Body_post_endpoint_bar_bar_post",
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
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "openapi": "3.0.2",
    "paths": {
        "/bar": {
            "post": {
                "operationId": "post_endpoint_bar_bar_post",
                "parameters": [
                    {
                        "in": "query",
                        "name": "y",
                        "required": True,
                        "schema": {"title": "Y", "type": "integer"},
                    },
                    {
                        "in": "query",
                        "name": "z",
                        "required": True,
                        "schema": {"title": "Z", "type": "integer"},
                    },
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_post_endpoint_bar_bar_post"
                            }
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful " "Response",
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
                "summary": "Post Endpoint Bar",
            }
        }
    },
}


def test_openapi_servers():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == open_api_foo


def test_post_generic_success():
    response = client.post("/bar?y=123&z=456", json={"data": "", "x": ["foo"]})
    assert response.status_code == 200
    assert response.json() == ["foo"]
