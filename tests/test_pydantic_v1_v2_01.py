from typing import Any, List, Union

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic.v1 import BaseModel


class SubItem(BaseModel):
    name: str


class Item(BaseModel):
    title: str
    size: int
    description: Union[str, None] = None
    sub: SubItem
    multi: List[SubItem] = []


app = FastAPI()


@app.post("/old-simple-model")
def handle_old_models(data: SubItem) -> SubItem:
    return data


@app.post("/old-simple-model-filter", response_model=SubItem)
def handle_old_models_filter(data: SubItem) -> Any:
    extended_data = data.dict()
    extended_data.update({"secret_price": 42})
    return extended_data


client = TestClient(app)


def test_old_simple_model():
    response = client.post(
        "/old-simple-model",
        json={"name": "Foo"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_old_simple_model_validation_error():
    response = client.post(
        "/old-simple-model",
        json={"wrong_name": "Foo"},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_old_simple_model_filter():
    response = client.post(
        "/old-simple-model-filter",
        json={"name": "Foo"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/old-simple-model": {
                    "post": {
                        "summary": "Handle Old Models",
                        "operationId": "handle_old_models_old_simple_model_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/SubItem"}
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SubItem"
                                        }
                                    }
                                },
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
                "/old-simple-model-filter": {
                    "post": {
                        "summary": "Handle Old Models Filter",
                        "operationId": "handle_old_models_filter_old_simple_model_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/SubItem"}
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/SubItem"
                                        }
                                    }
                                },
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
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "SubItem": {
                        "properties": {"name": {"type": "string", "title": "Name"}},
                        "type": "object",
                        "required": ["name"],
                        "title": "SubItem",
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
    )


# test_openapi_schema()
