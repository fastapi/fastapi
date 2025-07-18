from decimal import Decimal
from typing import List

from dirty_equals import IsDict, IsOneOf
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, condecimal

app = FastAPI()


class Item(BaseModel):
    name: str
    age: condecimal(gt=Decimal(0.0))  # type: ignore


@app.post("/items/")
def save_item_no_body(item: List[Item]):
    return {"item": item}


client = TestClient(app)


def test_put_correct_body():
    response = client.post("/items/", json=[{"name": "Foo", "age": 5}])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "item": [
            {
                "name": "Foo",
                "age": IsOneOf(
                    5,
                    # TODO: remove when deprecating Pydantic v1
                    "5",
                ),
            }
        ]
    }


def test_jsonable_encoder_requiring_error():
    response = client.post("/items/", json=[{"name": "Foo", "age": -1.0}])
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
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
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "ctx": {"limit_value": 0.0},
                    "loc": ["body", 0, "age"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                }
            ]
        }
    )


def test_put_incorrect_body_multiple():
    response = client.post("/items/", json=[{"age": "five"}, {"age": "six"}])
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
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
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", 0, "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", 0, "age"],
                    "msg": "value is not a valid decimal",
                    "type": "type_error.decimal",
                },
                {
                    "loc": ["body", 1, "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", 1, "age"],
                    "msg": "value is not a valid decimal",
                    "type": "type_error.decimal",
                },
            ]
        }
    )


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
                        "age": IsDict(
                            {
                                "title": "Age",
                                "anyOf": [
                                    {"exclusiveMinimum": 0.0, "type": "number"},
                                    {"type": "string"},
                                ],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {
                                "title": "Age",
                                "exclusiveMinimum": 0.0,
                                "type": "number",
                            }
                        ),
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
