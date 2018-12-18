import sys

import pytest
from starlette.testclient import TestClient

from cookie_params.tutorial001 import app

client = TestClient(app)


print(sys.path)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
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
                "summary": "Read Items Get",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Ads_Id", "type": "string"},
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
                        "items": {"type": "string"},
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


@pytest.mark.parametrize(
    "path,cookies,expected_status,expected_response",
    [
        ("/openapi.json", None, 200, openapi_schema),
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
    response = client.get(path, cookies=cookies)
    assert response.status_code == expected_status
    assert response.json() == expected_response
