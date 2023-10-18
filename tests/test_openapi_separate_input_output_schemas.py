from typing import List, Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .utils import PYDANTIC_V2, needs_pydanticv2


class SubItem(BaseModel):
    subname: str
    sub_description: Optional[str] = None
    tags: List[str] = []
    if PYDANTIC_V2:
        model_config = {"json_schema_serialization_defaults_required": True}


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    sub: Optional[SubItem] = None
    if PYDANTIC_V2:
        model_config = {"json_schema_serialization_defaults_required": True}


def get_app_client(separate_input_output_schemas: bool = True) -> TestClient:
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

    @app.post("/items/")
    def create_item(item: Item):
        return item

    @app.post("/items-list/")
    def create_item_list(item: List[Item]):
        return item

    @app.get("/items/")
    def read_items() -> List[Item]:
        return [
            Item(
                name="Portal Gun",
                description="Device to travel through the multi-rick-verse",
                sub=SubItem(subname="subname"),
            ),
            Item(name="Plumbus"),
        ]

    client = TestClient(app)
    return client


def test_create_item():
    client = get_app_client()
    client_no = get_app_client(separate_input_output_schemas=False)
    response = client.post("/items/", json={"name": "Plumbus"})
    response2 = client_no.post("/items/", json={"name": "Plumbus"})
    assert response.status_code == response2.status_code == 200, response.text
    assert (
        response.json()
        == response2.json()
        == {"name": "Plumbus", "description": None, "sub": None}
    )


def test_create_item_with_sub():
    client = get_app_client()
    client_no = get_app_client(separate_input_output_schemas=False)
    data = {
        "name": "Plumbus",
        "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF"},
    }
    response = client.post("/items/", json=data)
    response2 = client_no.post("/items/", json=data)
    assert response.status_code == response2.status_code == 200, response.text
    assert (
        response.json()
        == response2.json()
        == {
            "name": "Plumbus",
            "description": None,
            "sub": {"subname": "SubPlumbus", "sub_description": "Sub WTF", "tags": []},
        }
    )


def test_create_item_list():
    client = get_app_client()
    client_no = get_app_client(separate_input_output_schemas=False)
    data = [
        {"name": "Plumbus"},
        {
            "name": "Portal Gun",
            "description": "Device to travel through the multi-rick-verse",
        },
    ]
    response = client.post("/items-list/", json=data)
    response2 = client_no.post("/items-list/", json=data)
    assert response.status_code == response2.status_code == 200, response.text
    assert (
        response.json()
        == response2.json()
        == [
            {"name": "Plumbus", "description": None, "sub": None},
            {
                "name": "Portal Gun",
                "description": "Device to travel through the multi-rick-verse",
                "sub": None,
            },
        ]
    )


def test_read_items():
    client = get_app_client()
    client_no = get_app_client(separate_input_output_schemas=False)
    response = client.get("/items/")
    response2 = client_no.get("/items/")
    assert response.status_code == response2.status_code == 200, response.text
    assert (
        response.json()
        == response2.json()
        == [
            {
                "name": "Portal Gun",
                "description": "Device to travel through the multi-rick-verse",
                "sub": {"subname": "subname", "sub_description": None, "tags": []},
            },
            {"name": "Plumbus", "description": None, "sub": None},
        ]
    )


@needs_pydanticv2
def test_openapi_schema():
    client = get_app_client()
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/Item-Output"
                                        },
                                        "type": "array",
                                        "title": "Response Read Items Items  Get",
                                    }
                                }
                            },
                        }
                    },
                },
                "post": {
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item-Input"}
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
            },
            "/items-list/": {
                "post": {
                    "summary": "Create Item List",
                    "operationId": "create_item_list_items_list__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "items": {
                                        "$ref": "#/components/schemas/Item-Input"
                                    },
                                    "type": "array",
                                    "title": "Item",
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
                "Item-Input": {
                    "properties": {
                        "name": {"type": "string", "title": "Name"},
                        "description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Description",
                        },
                        "sub": {
                            "anyOf": [
                                {"$ref": "#/components/schemas/SubItem-Input"},
                                {"type": "null"},
                            ]
                        },
                    },
                    "type": "object",
                    "required": ["name"],
                    "title": "Item",
                },
                "Item-Output": {
                    "properties": {
                        "name": {"type": "string", "title": "Name"},
                        "description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Description",
                        },
                        "sub": {
                            "anyOf": [
                                {"$ref": "#/components/schemas/SubItem-Output"},
                                {"type": "null"},
                            ]
                        },
                    },
                    "type": "object",
                    "required": ["name", "description", "sub"],
                    "title": "Item",
                },
                "SubItem-Input": {
                    "properties": {
                        "subname": {"type": "string", "title": "Subname"},
                        "sub_description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Sub Description",
                        },
                        "tags": {
                            "items": {"type": "string"},
                            "type": "array",
                            "title": "Tags",
                            "default": [],
                        },
                    },
                    "type": "object",
                    "required": ["subname"],
                    "title": "SubItem",
                },
                "SubItem-Output": {
                    "properties": {
                        "subname": {"type": "string", "title": "Subname"},
                        "sub_description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Sub Description",
                        },
                        "tags": {
                            "items": {"type": "string"},
                            "type": "array",
                            "title": "Tags",
                            "default": [],
                        },
                    },
                    "type": "object",
                    "required": ["subname", "sub_description", "tags"],
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


@needs_pydanticv2
def test_openapi_schema_no_separate():
    client = get_app_client(separate_input_output_schemas=False)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {"$ref": "#/components/schemas/Item"},
                                        "type": "array",
                                        "title": "Response Read Items Items  Get",
                                    }
                                }
                            },
                        }
                    },
                },
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
            },
            "/items-list/": {
                "post": {
                    "summary": "Create Item List",
                    "operationId": "create_item_list_items_list__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "items": {"$ref": "#/components/schemas/Item"},
                                    "type": "array",
                                    "title": "Item",
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
                        "sub": {
                            "anyOf": [
                                {"$ref": "#/components/schemas/SubItem"},
                                {"type": "null"},
                            ]
                        },
                    },
                    "type": "object",
                    "required": ["name"],
                    "title": "Item",
                },
                "SubItem": {
                    "properties": {
                        "subname": {"type": "string", "title": "Subname"},
                        "sub_description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "title": "Sub Description",
                        },
                        "tags": {
                            "items": {"type": "string"},
                            "type": "array",
                            "title": "Tags",
                            "default": [],
                        },
                    },
                    "type": "object",
                    "required": ["subname"],
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
