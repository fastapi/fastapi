from decimal import Decimal

from dirty_equals import IsOneOf
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, condecimal

app = FastAPI()


class Item(BaseModel):
    name: str
    age: condecimal(gt=Decimal(0.0))  # type: ignore


@app.post("/items/")
def save_item_no_body(item: list[Item]):
    return {"item": item}


client = TestClient(app)


def test_put_correct_body():
    response = client.post("/items/", json=[{"name": "Foo", "age": 5}])
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "item": [
                {
                    "name": "Foo",
                    "age": "5",
                }
            ]
        }
    )


def test_jsonable_encoder_requiring_error():
    response = client.post("/items/", json=[{"name": "Foo", "age": -1.0}])
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["body", 0, "age"],
                "msg": "Input should be greater than 0",
                "input": -1.0,
                "ctx": {"gt": 0},
            }
        ]
    }


def test_put_incorrect_body_multiple():
    response = client.post("/items/", json=[{"age": "five"}, {"age": "six"}])
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", 0, "name"],
                "msg": "Field required",
                "input": {"age": "five"},
            },
            {
                "type": "decimal_parsing",
                "loc": ["body", 0, "age"],
                "msg": "Input should be a valid decimal",
                "input": "five",
            },
            {
                "type": "missing",
                "loc": ["body", 1, "name"],
                "msg": "Field required",
                "input": {"age": "six"},
            },
            {
                "type": "decimal_parsing",
                "loc": ["body", 1, "age"],
                "msg": "Input should be a valid decimal",
                "input": "six",
            },
        ]
    }


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
                    "summary": "Save Item No Body",
                    "operationId": "save_item_no_body_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Item",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
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
                    "required": ["name", "age"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "age": {
                            "title": "Age",
                            "anyOf": [
                                {"exclusiveMinimum": 0.0, "type": "number"},
                                IsOneOf(
                                    # pydantic < 2.12.0
                                    {"type": "string"},
                                    # pydantic >= 2.12.0
                                    {
                                        "type": "string",
                                        "pattern": r"^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$",
                                    },
                                ),
                            ],
                        },
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
