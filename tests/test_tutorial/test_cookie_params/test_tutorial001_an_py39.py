import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py39


@needs_py39
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
def test(path, cookies, expected_status, expected_response):
    from docs_src.cookie_params.tutorial001_an_py39 import app

    client = TestClient(app, cookies=cookies)
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@needs_py39
def test_openapi_schema():
    from docs_src.cookie_params.tutorial001_an_py39 import app

    client = TestClient(app)
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
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Ads Id",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {"title": "Ads Id", "type": "string"}
                            ),
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
