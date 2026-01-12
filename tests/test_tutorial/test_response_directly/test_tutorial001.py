import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.response_directly.{request.param}")

    client = TestClient(mod.app)
    return client


def test_path_operation(client: TestClient):
    response = client.put(
        "/items/1",
        json={
            "title": "Foo",
            "timestamp": "2023-01-01T12:00:00",
            "description": "A test item",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "A test item",
        "timestamp": "2023-01-01T12:00:00",
        "title": "Foo",
    }


def test_openapi_schema_pv2(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/items/{id}": {
                "put": {
                    "operationId": "update_item_items__id__put",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "id",
                            "required": True,
                            "schema": {"title": "Id", "type": "string"},
                        },
                    ],
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
                                "application/json": {"schema": {}},
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
                    "summary": "Update Item",
                },
            },
        },
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
                        "description": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"},
                            ],
                            "title": "Description",
                        },
                        "timestamp": {
                            "format": "date-time",
                            "title": "Timestamp",
                            "type": "string",
                        },
                        "title": {"title": "Title", "type": "string"},
                    },
                    "required": [
                        "title",
                        "timestamp",
                    ],
                    "title": "Item",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "integer"},
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
    }
