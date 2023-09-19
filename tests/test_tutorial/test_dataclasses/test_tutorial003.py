from fastapi.testclient import TestClient

from docs_src.dataclasses.tutorial003 import app

from ...utils import needs_pydanticv1, needs_pydanticv2

client = TestClient(app)


def test_post_authors_item():
    response = client.post(
        "/authors/foo/items/",
        json=[{"name": "Bar"}, {"name": "Baz", "description": "Drop the Baz"}],
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "foo",
        "items": [
            {"name": "Bar", "description": None},
            {"name": "Baz", "description": "Drop the Baz"},
        ],
    }


def test_get_authors():
    response = client.get("/authors/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be be playin' and havin' fun",
                },
                {"name": "Holy Buddies", "description": None},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai", "description": None},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]


@needs_pydanticv2
def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/authors/{author_id}/items/": {
                "post": {
                    "summary": "Create Author Items",
                    "operationId": "create_author_items_authors__author_id__items__post",
                    "parameters": [
                        {
                            "name": "author_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "title": "Author Id"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
                                    "title": "Items",
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Author"}
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
            "/authors/": {
                "get": {
                    "summary": "Get Authors",
                    "operationId": "get_authors_authors__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/Author"
                                        },
                                        "type": "array",
                                        "title": "Response Get Authors Authors  Get",
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Author": {
                    "properties": {
                        "name": {"type": "string", "title": "Name"},
                        "items": {
                            "items": {"$ref": "#/components/schemas/Item"},
                            "type": "array",
                            "title": "Items",
                        },
                    },
                    "type": "object",
                    "required": ["name"],
                    "title": "Author",
                },
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
                    "properties": {
                        "name": {"type": "string", "title": "Name"},
                        "description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Description",
                        },
                    },
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


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_openapi_schema_pv1():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/authors/{author_id}/items/": {
                "post": {
                    "summary": "Create Author Items",
                    "operationId": "create_author_items_authors__author_id__items__post",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Author Id", "type": "string"},
                            "name": "author_id",
                            "in": "path",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Items",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
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
                                    "schema": {"$ref": "#/components/schemas/Author"}
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
            "/authors/": {
                "get": {
                    "summary": "Get Authors",
                    "operationId": "get_authors_authors__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response Get Authors Authors  Get",
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Author"
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Author": {
                    "title": "Author",
                    "required": ["name"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "items": {
                            "title": "Items",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Item"},
                        },
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
                    "required": ["name"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
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
            }
        },
    }
