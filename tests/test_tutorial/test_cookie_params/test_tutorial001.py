import importlib
from types import ModuleType

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="mod",
    params=[
        "tutorial001_py39",
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an_py39",
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.cookie_params.{request.param}")

    return mod


@pytest.mark.parametrize(
    "path,cookies,expected_status,expected_response",
    [
        ("/items", None, 200, {"ads_id": None}),
        ("/items", {"ads_id": "ads_track"}, 200, {"ads_id": "ads_track"}),
        (
            "/items",
            {"ads_id": "ads_track", "session": "cookiesession"},
            200,
            {"ads_id": "ads_track"},
        ),
        ("/items", {"session": "cookiesession"}, 200, {"ads_id": None}),
    ],
)
def test(path, cookies, expected_status, expected_response, mod: ModuleType):
    client = TestClient(mod.app, cookies=cookies)
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_openapi_schema(mod: ModuleType):
    client = TestClient(mod.app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
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
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Ads Id",
                            },
                            "name": "ads_id",
                            "in": "cookie",
                        }
                    ],
                }
            }
        },
        "components": {
            "schemas": {
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
