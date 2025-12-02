import sys

import pytest
from fastapi._compat import PYDANTIC_V2
from inline_snapshot import snapshot

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

if not PYDANTIC_V2:
    pytest.skip("This test is only for Pydantic v2", allow_module_level=True)


import importlib

from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial003_an",
        pytest.param("tutorial003_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.pydantic_v1_in_v2.{request.param}")

    c = TestClient(mod.app)
    return c


def test_call(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "size": 3.4})
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
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Item",
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
                                            "$ref": "#/components/schemas/ItemV2"
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
                            "name": {"type": "string", "title": "Name"},
                            "description": {"type": "string", "title": "Description"},
                            "size": {"type": "number", "title": "Size"},
                        },
                        "type": "object",
                        "required": ["name", "size"],
                        "title": "Item",
                    },
                    "ItemV2": {
                        "properties": {
                            "name": {"type": "string", "title": "Name"},
                            "description": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Description",
                            },
                            "size": {"type": "number", "title": "Size"},
                        },
                        "type": "object",
                        "required": ["name", "size"],
                        "title": "ItemV2",
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
