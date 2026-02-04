import warnings

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from pydantic import BaseModel


def custom_generate_unique_id(route: APIRoute):
    return f"foo_{route.name}"


def custom_generate_unique_id2(route: APIRoute):
    return f"bar_{route.name}"


def custom_generate_unique_id3(route: APIRoute):
    return f"baz_{route.name}"


class Item(BaseModel):
    name: str
    price: float


class Message(BaseModel):
    title: str
    description: str


def test_top_level_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter()

    @app.post("/", response_model=list[Item], responses={404: {"model": list[Message]}})
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router", response_model=list[Item], responses={404: {"model": list[Message]}}
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "foo_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_root"
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
                                        "title": "Response Foo Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "foo_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_router"
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
                                        "title": "Response Foo Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_foo_post_root": {
                    "title": "Body_foo_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_router": {
                    "title": "Body_foo_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_router_overrides_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @app.post("/", response_model=list[Item], responses={404: {"model": list[Message]}})
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router", response_model=list[Item], responses={404: {"model": list[Message]}}
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "foo_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_root"
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
                                        "title": "Response Foo Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "bar_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_bar_post_router"
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
                                        "title": "Response Bar Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Bar Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_bar_post_router": {
                    "title": "Body_bar_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_root": {
                    "title": "Body_foo_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_router_include_overrides_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @app.post("/", response_model=list[Item], responses={404: {"model": list[Message]}})
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router", response_model=list[Item], responses={404: {"model": list[Message]}}
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    app.include_router(router, generate_unique_id_function=custom_generate_unique_id3)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "foo_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_root"
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
                                        "title": "Response Foo Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "bar_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_bar_post_router"
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
                                        "title": "Response Bar Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Bar Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_bar_post_router": {
                    "title": "Body_bar_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_root": {
                    "title": "Body_foo_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_subrouter_top_level_include_overrides_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter()
    sub_router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @app.post("/", response_model=list[Item], responses={404: {"model": list[Message]}})
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router", response_model=list[Item], responses={404: {"model": list[Message]}}
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @sub_router.post(
        "/subrouter",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
    )
    def post_subrouter(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    router.include_router(sub_router)
    app.include_router(router, generate_unique_id_function=custom_generate_unique_id3)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "foo_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_root"
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
                                        "title": "Response Foo Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "baz_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_baz_post_router"
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
                                        "title": "Response Baz Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Baz Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/subrouter": {
                "post": {
                    "summary": "Post Subrouter",
                    "operationId": "bar_post_subrouter",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_bar_post_subrouter"
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
                                        "title": "Response Bar Post Subrouter",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Bar Post Subrouter",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_bar_post_subrouter": {
                    "title": "Body_bar_post_subrouter",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_baz_post_router": {
                    "title": "Body_baz_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_root": {
                    "title": "Body_foo_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_router_path_operation_overrides_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @app.post("/", response_model=list[Item], responses={404: {"model": list[Message]}})
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
        generate_unique_id_function=custom_generate_unique_id3,
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "foo_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_root"
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
                                        "title": "Response Foo Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "baz_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_baz_post_router"
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
                                        "title": "Response Baz Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Baz Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_baz_post_router": {
                    "title": "Body_baz_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_root": {
                    "title": "Body_foo_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_app_path_operation_overrides_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @app.post(
        "/",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
        generate_unique_id_function=custom_generate_unique_id3,
    )
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @router.post(
        "/router",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
    )
    def post_router(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "baz_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_baz_post_root"
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
                                        "title": "Response Baz Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Baz Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
            "/router": {
                "post": {
                    "summary": "Post Router",
                    "operationId": "bar_post_router",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_bar_post_router"
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
                                        "title": "Response Bar Post Router",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Bar Post Router",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_bar_post_router": {
                    "title": "Body_bar_post_router",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_baz_post_root": {
                    "title": "Body_baz_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_callback_override_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    callback_router = APIRouter(generate_unique_id_function=custom_generate_unique_id2)

    @callback_router.post(
        "/post-callback",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
        generate_unique_id_function=custom_generate_unique_id3,
    )
    def post_callback(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @app.post(
        "/",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
        generate_unique_id_function=custom_generate_unique_id3,
        callbacks=callback_router.routes,
    )
    def post_root(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    @app.post(
        "/tocallback",
        response_model=list[Item],
        responses={404: {"model": list[Message]}},
    )
    def post_with_callback(item1: Item, item2: Item):
        return item1, item2  # pragma: nocover

    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "post": {
                    "summary": "Post Root",
                    "operationId": "baz_post_root",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_baz_post_root"
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
                                        "title": "Response Baz Post Root",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Baz Post Root",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                    "callbacks": {
                        "post_callback": {
                            "/post-callback": {
                                "post": {
                                    "summary": "Post Callback",
                                    "operationId": "baz_post_callback",
                                    "requestBody": {
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/Body_baz_post_callback"
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
                                                        "title": "Response Baz Post Callback",
                                                        "type": "array",
                                                        "items": {
                                                            "$ref": "#/components/schemas/Item"
                                                        },
                                                    }
                                                }
                                            },
                                        },
                                        "404": {
                                            "description": "Not Found",
                                            "content": {
                                                "application/json": {
                                                    "schema": {
                                                        "title": "Response 404 Baz Post Callback",
                                                        "type": "array",
                                                        "items": {
                                                            "$ref": "#/components/schemas/Message"
                                                        },
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
                            }
                        }
                    },
                }
            },
            "/tocallback": {
                "post": {
                    "summary": "Post With Callback",
                    "operationId": "foo_post_with_callback",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_foo_post_with_callback"
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
                                        "title": "Response Foo Post With Callback",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        },
                        "404": {
                            "description": "Not Found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response 404 Foo Post With Callback",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Message"
                                        },
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
                "Body_baz_post_callback": {
                    "title": "Body_baz_post_callback",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_baz_post_root": {
                    "title": "Body_baz_post_root",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
                    },
                },
                "Body_foo_post_with_callback": {
                    "title": "Body_foo_post_with_callback",
                    "required": ["item1", "item2"],
                    "type": "object",
                    "properties": {
                        "item1": {"$ref": "#/components/schemas/Item"},
                        "item2": {"$ref": "#/components/schemas/Item"},
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
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                },
                "Message": {
                    "title": "Message",
                    "required": ["title", "description"],
                    "type": "object",
                    "properties": {
                        "title": {"title": "Title", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "ctx": {"title": "Context", "type": "object"},
                        "input": {"title": "Input"},
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
            }
        },
    }


def test_warn_duplicate_operation_id():
    def broken_operation_id(route: APIRoute):
        return "foo"

    app = FastAPI(generate_unique_id_function=broken_operation_id)

    @app.post("/")
    def post_root(item1: Item):
        return item1  # pragma: nocover

    @app.post("/second")
    def post_second(item1: Item):
        return item1  # pragma: nocover

    @app.post("/third")
    def post_third(item1: Item):
        return item1  # pragma: nocover

    client = TestClient(app)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        client.get("/openapi.json")
        assert len(w) >= 2
        duplicate_warnings = [
            warning for warning in w if issubclass(warning.category, UserWarning)
        ]
        assert len(duplicate_warnings) > 0
        assert "Duplicate Operation ID" in str(duplicate_warnings[0].message)


def test_multiple_methods_unique_operation_id():
    """
    Test that routes with multiple methods get unique operationIds.

    This was a bug where all methods on the same route would get the same
    operationId (based only on the first method), causing duplicate
    operation ID warnings. See https://github.com/fastapi/fastapi/issues/13175
    """
    app = FastAPI()
    router = APIRouter()

    @router.post("/clear")
    @router.delete("/clear")
    def clear_endpoint():
        return {"message": "cleared"}

    app.include_router(router)
    client = TestClient(app)

    # Call the endpoints to ensure coverage
    post_response = client.post("/clear")
    assert post_response.status_code == 200
    delete_response = client.delete("/clear")
    assert delete_response.status_code == 200

    # Check no warnings are raised when generating OpenAPI
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

        # Should not have any duplicate operation ID warnings
        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(duplicate_warnings) == 0, (
            f"Unexpected duplicate warnings: {duplicate_warnings}"
        )

    data = response.json()
    paths = data["paths"]

    # Verify both methods have unique operationIds
    post_op_id = paths["/clear"]["post"]["operationId"]
    delete_op_id = paths["/clear"]["delete"]["operationId"]

    assert post_op_id != delete_op_id, (
        f"POST and DELETE should have different operationIds, got: {post_op_id}"
    )

    # Verify the operationIds contain the method suffix
    assert post_op_id.endswith("_post"), (
        f"POST operationId should end with '_post', got: {post_op_id}"
    )
    assert delete_op_id.endswith("_delete"), (
        f"DELETE operationId should end with '_delete', got: {delete_op_id}"
    )


def test_three_methods_unique_operation_id():
    """Test with three methods on the same route."""
    app = FastAPI()
    router = APIRouter()

    @router.get("/items")
    @router.put("/items")
    @router.patch("/items")
    def item_handler():
        return {"message": "items"}

    app.include_router(router)
    client = TestClient(app)

    # Call the endpoints to ensure coverage
    get_response = client.get("/items")
    assert get_response.status_code == 200
    put_response = client.put("/items")
    assert put_response.status_code == 200
    patch_response = client.patch("/items")
    assert patch_response.status_code == 200

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        assert len(duplicate_warnings) == 0

    data = response.json()
    paths = data["paths"]

    get_op_id = paths["/items"]["get"]["operationId"]
    put_op_id = paths["/items"]["put"]["operationId"]
    patch_op_id = paths["/items"]["patch"]["operationId"]

    # All should be different
    assert len({get_op_id, put_op_id, patch_op_id}) == 3, (
        f"All three operationIds should be unique: {get_op_id}, {put_op_id}, {patch_op_id}"
    )


def test_explicit_operation_id_multiple_methods():
    """
    When an explicit operation_id is provided with multiple methods,
    it should be used as-is, which will trigger the duplicate warning
    (this is expected behavior - user chose to have duplicates).
    """
    app = FastAPI()
    router = APIRouter()

    @router.post("/clear", operation_id="clear_items")
    @router.delete("/clear", operation_id="clear_items")
    def clear_endpoint():
        return {"message": "cleared"}

    app.include_router(router)
    client = TestClient(app)

    # Call the endpoints to ensure coverage
    post_response = client.post("/clear")
    assert post_response.status_code == 200
    delete_response = client.delete("/clear")
    assert delete_response.status_code == 200

    # This WILL generate a warning because the same explicit operation_id
    # is used for both methods
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        response = client.get("/openapi.json")

        # Should have duplicate warning because explicit operation_id is used
        duplicate_warnings = [
            warning for warning in w if "Duplicate Operation ID" in str(warning.message)
        ]
        # With explicit operation_id, both methods share the same ID
        assert len(duplicate_warnings) == 1

    data = response.json()
    paths = data["paths"]

    # Both should use the explicit operation_id (and cause the warning)
    post_op_id = paths["/clear"]["post"]["operationId"]
    delete_op_id = paths["/clear"]["delete"]["operationId"]

    assert post_op_id == "clear_items"
    assert delete_op_id == "clear_items"


def test_single_method_no_extra_suffix():
    """
    Single method routes should not get the extra method suffix added.
    """
    app = FastAPI()
    router = APIRouter()

    @router.get("/items")
    def get_items():
        return {"items": []}

    app.include_router(router)
    client = TestClient(app)

    # Call the endpoint to ensure coverage
    get_response = client.get("/items")
    assert get_response.status_code == 200
    assert get_response.json() == {"items": []}

    response = client.get("/openapi.json")
    data = response.json()

    op_id = data["paths"]["/items"]["get"]["operationId"]

    # Should be the standard format without extra suffix
    assert op_id == "get_items_items_get"
