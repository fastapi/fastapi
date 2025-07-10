from typing import Optional, Union

from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None


class ExtendedItem(Item):
    age: int


@app.post("/items/")
def save_union_different_body(item: Union[ExtendedItem, Item]):
    return {"item": item}


client = TestClient(app)


def test_post_extended_item():
    response = client.post("/items/", json={"name": "Foo", "age": 5})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"name": "Foo", "age": 5}}


def test_post_item():
    response = client.post("/items/", json={"name": "Foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"name": "Foo"}}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
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
                    "summary": "Save Union Different Body",
                    "operationId": "save_union_different_body_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Item",
                                    "anyOf": [
                                        {"$ref": "#/components/schemas/ExtendedItem"},
                                        {"$ref": "#/components/schemas/Item"},
                                    ],
                                }
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Item": {
                    "title": "Item",
                    "type": "object",
                    "properties": {
                        "name": IsDict(
                            {
                                "title": "Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Name", "type": "string"}
                        )
                    },
                },
                "ExtendedItem": {
                    "title": "ExtendedItem",
                    "required": ["age"],
                    "type": "object",
                    "properties": {
                        "name": IsDict(
                            {
                                "title": "Name",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Name", "type": "string"}
                        ),
                        "age": {"title": "Age", "type": "integer"},
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
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
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
            }
        },
    }
