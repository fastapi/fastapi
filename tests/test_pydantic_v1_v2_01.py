import sys
import warnings
from typing import Any, Union

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

from fastapi import FastAPI
from fastapi._compat.v1 import BaseModel
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


class SubItem(BaseModel):
    name: str


class Item(BaseModel):
    title: str
    size: int
    description: Union[str, None] = None
    sub: SubItem
    multi: list[SubItem] = []


app = FastAPI()

with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")

    @app.post("/simple-model")
    def handle_simple_model(data: SubItem) -> SubItem:
        return data

    @app.post("/simple-model-filter", response_model=SubItem)
    def handle_simple_model_filter(data: SubItem) -> Any:
        extended_data = data.dict()
        extended_data.update({"secret_price": 42})
        return extended_data

    @app.post("/item")
    def handle_item(data: Item) -> Item:
        return data

    @app.post("/item-filter", response_model=Item)
    def handle_item_filter(data: Item) -> Any:
        extended_data = data.dict()
        extended_data.update({"secret_data": "classified", "internal_id": 12345})
        extended_data["sub"].update({"internal_id": 67890})
        return extended_data


client = TestClient(app)


def test_old_simple_model():
    response = client.post(
        "/simple-model",
        json={"name": "Foo"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_old_simple_model_validation_error():
    response = client.post(
        "/simple-model",
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
        "/simple-model-filter",
        json={"name": "Foo"},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo"}


def test_item_model():
    response = client.post(
        "/item",
        json={
            "title": "Test Item",
            "size": 100,
            "description": "This is a test item",
            "sub": {"name": "SubItem1"},
            "multi": [{"name": "Multi1"}, {"name": "Multi2"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "Test Item",
        "size": 100,
        "description": "This is a test item",
        "sub": {"name": "SubItem1"},
        "multi": [{"name": "Multi1"}, {"name": "Multi2"}],
    }


def test_item_model_minimal():
    response = client.post(
        "/item",
        json={"title": "Minimal Item", "size": 50, "sub": {"name": "SubMin"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "Minimal Item",
        "size": 50,
        "description": None,
        "sub": {"name": "SubMin"},
        "multi": [],
    }


def test_item_model_validation_errors():
    response = client.post(
        "/item",
        json={"title": "Missing fields"},
    )
    assert response.status_code == 422, response.text
    error_detail = response.json()["detail"]
    assert len(error_detail) == 2
    assert {
        "loc": ["body", "size"],
        "msg": "field required",
        "type": "value_error.missing",
    } in error_detail
    assert {
        "loc": ["body", "sub"],
        "msg": "field required",
        "type": "value_error.missing",
    } in error_detail


def test_item_model_nested_validation_error():
    response = client.post(
        "/item",
        json={"title": "Test Item", "size": 100, "sub": {"wrong_field": "test"}},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "sub", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_item_model_invalid_type():
    response = client.post(
        "/item",
        json={"title": "Test Item", "size": "not_a_number", "sub": {"name": "SubItem"}},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "size"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_item_filter():
    response = client.post(
        "/item-filter",
        json={
            "title": "Filtered Item",
            "size": 200,
            "description": "Test filtering",
            "sub": {"name": "SubFiltered"},
            "multi": [],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == {
        "title": "Filtered Item",
        "size": 200,
        "description": "Test filtering",
        "sub": {"name": "SubFiltered"},
        "multi": [],
    }
    assert "secret_data" not in result
    assert "internal_id" not in result


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/simple-model": {
                    "post": {
                        "summary": "Handle Simple Model",
                        "operationId": "handle_simple_model_simple_model_post",
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
                "/simple-model-filter": {
                    "post": {
                        "summary": "Handle Simple Model Filter",
                        "operationId": "handle_simple_model_filter_simple_model_filter_post",
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
                "/item": {
                    "post": {
                        "summary": "Handle Item",
                        "operationId": "handle_item_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
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
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                "/item-filter": {
                    "post": {
                        "summary": "Handle Item Filter",
                        "operationId": "handle_item_filter_item_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
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
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                    "Item": {
                        "properties": {
                            "title": {"type": "string", "title": "Title"},
                            "size": {"type": "integer", "title": "Size"},
                            "description": {"type": "string", "title": "Description"},
                            "sub": {"$ref": "#/components/schemas/SubItem"},
                            "multi": {
                                "items": {"$ref": "#/components/schemas/SubItem"},
                                "type": "array",
                                "title": "Multi",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "required": ["title", "size", "sub"],
                        "title": "Item",
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
