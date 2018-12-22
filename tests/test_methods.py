from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = None


@app.delete("/items/{item_id}")
def delete_item(item_id: str, item: Item):
    return {"item_id": item_id, "item": item}


@app.head("/items/{item_id}")
def head_item(item_id: str):
    return JSONResponse(headers={"x-fastapi-item-id": item_id})


@app.options("/items/{item_id}")
def options_item(item_id: str):
    return JSONResponse(headers={"x-fastapi-item-id": item_id})


@app.patch("/items/{item_id}")
def patch_item(item_id: str, item: Item):
    return {"item_id": item_id, "item": item}


@app.trace("/items/{item_id}")
def trace_item(item_id: str):
    return JSONResponse(media_type="message/http")


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/items/{item_id}": {
            "delete": {
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
                "summary": "Delete Item Delete",
                "operationId": "delete_item_items__item_id__delete",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Item"}
                        }
                    },
                    "required": True,
                },
            },
            "options": {
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
                "summary": "Options Item Options",
                "operationId": "options_item_items__item_id__options",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            },
            "head": {
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
                "summary": "Head Item Head",
                "operationId": "head_item_items__item_id__head",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            },
            "patch": {
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
                "summary": "Patch Item Patch",
                "operationId": "patch_item_items__item_id__patch",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Item"}
                        }
                    },
                    "required": True,
                },
            },
            "trace": {
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
                "summary": "Trace Item Trace",
                "operationId": "trace_item_items__item_id__trace",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item_Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
            },
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "title": "Item",
                "required": ["name"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {"title": "Price", "type": "number"},
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_delete():
    response = client.delete("/items/foo", json={"name": "Foo"})
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo", "item": {"name": "Foo", "price": None}}


def test_head():
    response = client.head("/items/foo")
    assert response.status_code == 200
    assert response.headers["x-fastapi-item-id"] == "foo"


def test_options():
    response = client.head("/items/foo")
    assert response.status_code == 200
    assert response.headers["x-fastapi-item-id"] == "foo"


def test_patch():
    response = client.patch("/items/foo", json={"name": "Foo"})
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo", "item": {"name": "Foo", "price": None}}


def test_trace():
    response = client.request("trace", "/items/foo")
    assert response.status_code == 200
    assert response.headers["content-type"] == "message/http"
