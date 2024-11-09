import os
import shutil

from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.additional_responses.tutorial004 import app

client = TestClient(app)


def test_path_operation():
    response = client.get("/items/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "foo", "value": "there goes my hero"}


def test_path_operation_img():
    shutil.copy("./docs/en/docs/img/favicon.png", "./image.png")
    response = client.get("/items/foo?img=1")
    assert response.status_code == 200, response.text
    assert response.headers["Content-Type"] == "image/png"
    assert len(response.content)
    os.remove("./image.png")


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "get": {
                    "responses": {
                        "404": {"description": "Item not found"},
                        "302": {"description": "The item was moved"},
                        "403": {"description": "Not enough privileges"},
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "image/png": {},
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Item"}
                                },
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
                    "summary": "Read Item",
                    "operationId": "read_item_items__item_id__get",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "string"},
                            "name": "item_id",
                            "in": "path",
                        },
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "boolean"}, {"type": "null"}],
                                    "title": "Img",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Img", "type": "boolean"}
                            ),
                            "name": "img",
                            "in": "query",
                        },
                    ],
                }
            }
        },
        "components": {
            "schemas": {
                "Item": {
                    "title": "Item",
                    "required": ["id", "value"],
                    "type": "object",
                    "properties": {
                        "id": {"title": "Id", "type": "string"},
                        "value": {"title": "Value", "type": "string"},
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
