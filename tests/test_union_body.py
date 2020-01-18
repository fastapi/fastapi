from typing import Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None


class OtherItem(BaseModel):
    price: int


@app.post("/items/")
def save_union_body(item: Union[OtherItem, Item]):
    return {"item": item}


client = TestClient(app)

item_openapi_schema = {
    "openapi": "3.0.2",
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
                "summary": "Save Union Body",
                "operationId": "save_union_body_items__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "title": "Item",
                                "anyOf": [
                                    {"$ref": "#/components/schemas/OtherItem"},
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
            "OtherItem": {
                "title": "OtherItem",
                "required": ["price"],
                "type": "object",
                "properties": {"price": {"title": "Price", "type": "integer"}},
            },
            "Item": {
                "title": "Item",
                "type": "object",
                "properties": {"name": {"title": "Name", "type": "string"}},
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


def test_item_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == item_openapi_schema


def test_post_other_item():
    response = client.post("/items/", json={"price": 100})
    assert response.status_code == 200
    assert response.json() == {"item": {"price": 100}}


def test_post_item():
    response = client.post("/items/", json={"name": "Foo"})
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "Foo"}}
