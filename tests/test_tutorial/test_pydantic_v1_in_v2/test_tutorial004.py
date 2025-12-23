import sys
import warnings

import pytest
from inline_snapshot import snapshot

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()


import importlib

from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial004_an_py39"),
        pytest.param("tutorial004_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    with warnings.catch_warnings(record=True):
        warnings.filterwarnings(
            "ignore",
            message=r"pydantic\.v1 is deprecated and will soon stop being supported by FastAPI\..*",
            category=DeprecationWarning,
        )
        mod = importlib.import_module(f"docs_src.pydantic_v1_in_v2.{request.param}")

    c = TestClient(mod.app)
    return c


def test_call(client: TestClient):
    response = client.post("/items/", json={"item": {"name": "Foo", "size": 3.4}})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "description": None,
        "size": 3.4,
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "post": {
                        "summary": "Create Item",
                        "operationId": "create_item_items__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/Body_create_item_items__post"
                                            }
                                        ],
                                        "title": "Body",
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
                }
            },
            "components": {
                "schemas": {
                    "Body_create_item_items__post": {
                        "properties": {
                            "item": {
                                "allOf": [{"$ref": "#/components/schemas/Item"}],
                                "title": "Item",
                            }
                        },
                        "type": "object",
                        "required": ["item"],
                        "title": "Body_create_item_items__post",
                    },
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
                            "name": {"type": "string", "title": "Name"},
                            "description": {"type": "string", "title": "Description"},
                            "size": {"type": "number", "title": "Size"},
                        },
                        "type": "object",
                        "required": ["name", "size"],
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
    )
