from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


@app.get("/home", add_auto_options_route=True)
def get_home():
    return {"hello": "world"}


@app.post("/items/", add_auto_options_route=True)
def create_item(item: Item):
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: str, item: Item):
    return {"item_id": item_id, "item": item}


@app.head("/items/{item_id}", add_auto_options_route=True)
def head_item(item_id: str):
    return JSONResponse(None, headers={"x-fastapi-item-id": item_id})


@app.patch("/items/{item_id}", add_auto_options_route=True)
def patch_item(item_id: str, item: Item):
    return {"item_id": item_id, "item": item}


@app.trace("/items/{item_id}", add_auto_options_route=True)
def trace_item(item_id: str):
    return JSONResponse(None, media_type="message/http")


client = TestClient(app)


def test_get_api_route():
    response = client.get("/home")
    assert response.status_code == 200, response.text
    assert response.json() == {"hello": "world"}


def test_post_api_route():
    response = client.post("/items/", json={"name": "CoolItem"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "CoolItem"}


def test_delete():
    response = client.request("DELETE", "/items/foo", json={"name": "Foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "item": {"name": "Foo"}}


def test_head():
    response = client.head("/items/foo")
    assert response.status_code == 200, response.text
    assert response.headers["x-fastapi-item-id"] == "foo"


def test_patch():
    response = client.patch("/items/foo", json={"name": "Foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "item": {"name": "Foo"}}


def test_trace():
    response = client.request("trace", "/items/foo")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "message/http"


def test_get_auto_options():
    response = client.options("/home")
    assert response.status_code == 200, response.text
    assert response.headers.raw[0][0].decode("utf-8") == "allow"
    assert response.headers.raw[0][1].decode("utf-8") == "GET"


def test_post_auto_options():
    response = client.options("/items/")
    assert response.status_code == 200, response.text
    assert response.headers.raw[0][0].decode("utf-8") == "allow"
    assert response.headers.raw[0][1].decode("utf-8") == "POST"


def test_head_auto_options():
    response = client.head("/items/foo")
    assert response.status_code == 200, response.text
    assert response.headers["x-fastapi-item-id"] == "foo"


def test_other_auto_options():
    response = client.options("/items/foo")
    assert response.status_code == 200, response.text
    assert response.headers.raw[0][0].decode("utf-8") == "allow"
    assert set(response.headers.raw[0][1].decode("utf-8").split(", ")) == {
        "DELETE",
        "HEAD",
        "PATCH",
        "TRACE",
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/home": {
                "get": {
                    "summary": "Get Home",
                    "operationId": "get_home_home_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                },
                "options": {
                    "summary": "Options Route",
                    "operationId": "options_route_home_options",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                },
            },
            "/items/": {
                "post": {
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
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
                },
                "options": {
                    "summary": "Options Route",
                    "operationId": "options_route_items__options",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                },
            },
            "/items/{item_id}": {
                "delete": {
                    "summary": "Delete Item",
                    "operationId": "delete_item_items__item_id__delete",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "title": "Item Id"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
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
                },
                "head": {
                    "summary": "Head Item",
                    "operationId": "head_item_items__item_id__head",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "title": "Item Id"},
                        }
                    ],
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
                },
                "patch": {
                    "summary": "Patch Item",
                    "operationId": "patch_item_items__item_id__patch",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "title": "Item Id"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
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
                },
                "trace": {
                    "summary": "Trace Item",
                    "operationId": "trace_item_items__item_id__trace",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "title": "Item Id"},
                        }
                    ],
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
                },
                "options": {
                    "summary": "Options Route",
                    "operationId": "options_route_items__item_id__options",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                },
            },
        },
        "components": {
            "schemas": {
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
                "Item": {
                    "properties": {"name": {"type": "string", "title": "Name"}},
                    "type": "object",
                    "required": ["name"],
                    "title": "Item",
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
