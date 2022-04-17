from typing import List, Tuple

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class ItemGroup(BaseModel):
    items: List[Tuple[str, str]]


class Coordinate(BaseModel):
    x: float
    y: float


@app.post("/model-with-tuple/")
def post_model_with_tuple(item_group: ItemGroup):
    return item_group


@app.post("/tuple-of-models/")
def post_tuple_of_models(square: Tuple[Coordinate, Coordinate]):
    return square


@app.post("/tuple-form/")
def hello(values: Tuple[int, int] = Form(...)):
    return values


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/model-with-tuple/": {
            "post": {
                "summary": "Post Model With Tuple",
                "operationId": "post_model_with_tuple_model_with_tuple__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ItemGroup"}
                        }
                    },
                    "required": True,
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
        },
        "/tuple-of-models/": {
            "post": {
                "summary": "Post Tuple Of Models",
                "operationId": "post_tuple_of_models_tuple_of_models__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "title": "Square",
                                "maxItems": 2,
                                "minItems": 2,
                                "type": "array",
                                "items": [
                                    {"$ref": "#/components/schemas/Coordinate"},
                                    {"$ref": "#/components/schemas/Coordinate"},
                                ],
                            }
                        }
                    },
                    "required": True,
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
        },
        "/tuple-form/": {
            "post": {
                "summary": "Hello",
                "operationId": "hello_tuple_form__post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_hello_tuple_form__post"
                            }
                        }
                    },
                    "required": True,
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
        },
    },
    "components": {
        "schemas": {
            "Body_hello_tuple_form__post": {
                "title": "Body_hello_tuple_form__post",
                "required": ["values"],
                "type": "object",
                "properties": {
                    "values": {
                        "title": "Values",
                        "maxItems": 2,
                        "minItems": 2,
                        "type": "array",
                        "items": [{"type": "integer"}, {"type": "integer"}],
                    }
                },
            },
            "Coordinate": {
                "title": "Coordinate",
                "required": ["x", "y"],
                "type": "object",
                "properties": {
                    "x": {"title": "X", "type": "number"},
                    "y": {"title": "Y", "type": "number"},
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
            "ItemGroup": {
                "title": "ItemGroup",
                "required": ["items"],
                "type": "object",
                "properties": {
                    "items": {
                        "title": "Items",
                        "type": "array",
                        "items": {
                            "maxItems": 2,
                            "minItems": 2,
                            "type": "array",
                            "items": [{"type": "string"}, {"type": "string"}],
                        },
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_model_with_tuple_valid():
    data = {"items": [["foo", "bar"], ["baz", "whatelse"]]}
    response = client.post("/model-with-tuple/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_model_with_tuple_invalid():
    data = {"items": [["foo", "bar"], ["baz", "whatelse", "too", "much"]]}
    response = client.post("/model-with-tuple/", json=data)
    assert response.status_code == 422, response.text

    data = {"items": [["foo", "bar"], ["baz"]]}
    response = client.post("/model-with-tuple/", json=data)
    assert response.status_code == 422, response.text


def test_tuple_with_model_valid():
    data = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
    response = client.post("/tuple-of-models/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_tuple_with_model_invalid():
    data = [{"x": 1, "y": 2}, {"x": 3, "y": 4}, {"x": 5, "y": 6}]
    response = client.post("/tuple-of-models/", json=data)
    assert response.status_code == 422, response.text

    data = [{"x": 1, "y": 2}]
    response = client.post("/tuple-of-models/", json=data)
    assert response.status_code == 422, response.text


def test_tuple_form_valid():
    response = client.post("/tuple-form/", data=[("values", "1"), ("values", "2")])
    assert response.status_code == 200, response.text
    assert response.json() == [1, 2]


def test_tuple_form_invalid():
    response = client.post(
        "/tuple-form/", data=[("values", "1"), ("values", "2"), ("values", "3")]
    )
    assert response.status_code == 422, response.text

    response = client.post("/tuple-form/", data=[("values", "1")])
    assert response.status_code == 422, response.text
