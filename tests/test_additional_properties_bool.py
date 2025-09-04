from typing import Union

from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict


class FooBaseModel(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="forbid")
    else:

        class Config:
            extra = "forbid"


class Foo(FooBaseModel):
    pass


app = FastAPI()


@app.post("/")
async def post(
    foo: Union[Foo, None] = None,
):
    return foo


client = TestClient(app)


def test_call_invalid():
    response = client.post("/", json={"foo": {"bar": "baz"}})
    assert response.status_code == 422


def test_call_valid():
    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == {}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post",
                    "operationId": "post__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": IsDict(
                                    {
                                        "anyOf": [
                                            {"$ref": "#/components/schemas/Foo"},
                                            {"type": "null"},
                                        ],
                                        "title": "Foo",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {"$ref": "#/components/schemas/Foo"}
                                )
                            }
                        }
                    },
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
                "Foo": {
                    "properties": {},
                    "additionalProperties": False,
                    "type": "object",
                    "title": "Foo",
                },
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }
