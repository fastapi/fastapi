import importlib
import os
import shutil

import pytest
from fastapi.testclient import TestClient

from tests.utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.additional_responses.{request.param}")

    client = TestClient(mod.app)
    client.headers.clear()
    return client


def test_path_operation(client: TestClient):
    response = client.get("/items/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "foo", "value": "there goes my hero"}


def test_path_operation_img(client: TestClient):
    shutil.copy("./docs/en/docs/img/favicon.png", "./image.png")
    response = client.get("/items/foo?img=1")
    assert response.status_code == 200, response.text
    assert response.headers["Content-Type"] == "image/png"
    assert len(response.content)
    os.remove("./image.png")


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Return the JSON item or an image.",
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
                            "schema": {
                                "anyOf": [{"type": "boolean"}, {"type": "null"}],
                                "title": "Img",
                            },
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
