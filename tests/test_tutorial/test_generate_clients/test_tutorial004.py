import importlib
import json
import pathlib
from unittest.mock import patch

from docs_src.generate_clients import tutorial003_py39


def test_remove_tags(tmp_path: pathlib.Path):
    tmp_file = tmp_path / "openapi.json"
    openapi_json = tutorial003_py39.app.openapi()
    tmp_file.write_text(json.dumps(openapi_json))

    with patch("pathlib.Path", return_value=tmp_file):
        importlib.import_module("docs_src.generate_clients.tutorial004_py39")

    modified_openapi = json.loads(tmp_file.read_text())
    assert modified_openapi == {
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "Item": {
                    "properties": {
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                        "price": {
                            "title": "Price",
                            "type": "number",
                        },
                    },
                    "required": [
                        "name",
                        "price",
                    ],
                    "title": "Item",
                    "type": "object",
                },
                "ResponseMessage": {
                    "properties": {
                        "message": {
                            "title": "Message",
                            "type": "string",
                        },
                    },
                    "required": [
                        "message",
                    ],
                    "title": "ResponseMessage",
                    "type": "object",
                },
                "User": {
                    "properties": {
                        "email": {
                            "title": "Email",
                            "type": "string",
                        },
                        "username": {
                            "title": "Username",
                            "type": "string",
                        },
                    },
                    "required": [
                        "username",
                        "email",
                    ],
                    "title": "User",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/items/": {
                "get": {
                    "operationId": "get_items",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/Item",
                                        },
                                        "title": "Response Items-Get Items",
                                        "type": "array",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Get Items",
                    "tags": [
                        "items",
                    ],
                },
                "post": {
                    "operationId": "create_item",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Item",
                                },
                            },
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ResponseMessage",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Create Item",
                    "tags": [
                        "items",
                    ],
                },
            },
            "/users/": {
                "post": {
                    "operationId": "create_user",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User",
                                },
                            },
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ResponseMessage",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Create User",
                    "tags": [
                        "users",
                    ],
                },
            },
        },
    }
