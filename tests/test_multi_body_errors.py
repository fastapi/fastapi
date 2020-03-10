from decimal import Decimal
from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, condecimal

app = FastAPI()


class Item(BaseModel):
    name: str
    age: condecimal(gt=Decimal(0.0))


@app.post("/items/")
def save_item_no_body(item: List[Item]):
    return {"item": item}


client = TestClient(app)


openapi_schema = {
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
                    "age": {"title": "Age", "exclusiveMinimum": 0.0, "type": "number"},
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

single_error = {
    "detail": [
        {
            "ctx": {"limit_value": 0.0},
            "loc": ["body", "item", 0, "age"],
            "msg": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt",
        }
    ]
}

multiple_errors = {
    "detail": [
        {
            "loc": ["body", "item", 0, "name"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "item", 0, "age"],
            "msg": "value is not a valid decimal",
            "type": "type_error.decimal",
        },
        {
            "loc": ["body", "item", 1, "name"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "item", 1, "age"],
            "msg": "value is not a valid decimal",
            "type": "type_error.decimal",
        },
    ]
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_put_correct_body():
    response = client.post("/items/", json=[{"name": "Foo", "age": 5}])
    assert response.status_code == 200
    assert response.json() == {"item": [{"name": "Foo", "age": 5}]}


def test_jsonable_encoder_requiring_error():
    response = client.post("/items/", json=[{"name": "Foo", "age": -1.0}])
    assert response.status_code == 422
    assert response.json() == single_error


def test_put_incorrect_body_multiple():
    response = client.post("/items/", json=[{"age": "five"}, {"age": "six"}])
    assert response.status_code == 422
    assert response.json() == multiple_errors
