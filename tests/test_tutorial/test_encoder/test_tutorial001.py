import importlib
from types import ModuleType

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
    ],
)
def get_module(request: pytest.FixtureRequest):
    module = importlib.import_module(f"docs_src.encoder.{request.param}")
    return module


@pytest.fixture(name="client")
def get_client(mod: ModuleType):
    client = TestClient(mod.app)
    return client


def test_put(client: TestClient, mod: ModuleType):
    fake_db = mod.fake_db

    response = client.put(
        "/items/123",
        json={
            "title": "Foo",
            "timestamp": "2023-01-01T12:00:00",
            "description": "An optional description",
        },
    )
    assert response.status_code == 200
    assert "123" in fake_db
    assert fake_db["123"] == {
        "title": "Foo",
        "timestamp": "2023-01-01T12:00:00",
        "description": "An optional description",
    }


def test_put_invalid_data(client: TestClient, mod: ModuleType):
    fake_db = mod.fake_db

    response = client.put(
        "/items/345",
        json={
            "title": "Foo",
            "timestamp": "not a date",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "timestamp"],
                "msg": "Input should be a valid datetime or date, invalid character in year",
                "type": "datetime_from_date_parsing",
                "input": "not a date",
                "ctx": {"error": "invalid character in year"},
            }
        ]
    }
    assert "345" not in fake_db


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{id}": {
                "put": {
                    "operationId": "update_item_items__id__put",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "id",
                            "required": True,
                            "schema": {
                                "title": "Id",
                                "type": "string",
                            },
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
                                "application/json": {
                                    "schema": {},
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
                                {
                                    "type": "string",
                                },
                                {
                                    "type": "null",
                                },
                            ],
                            "title": "Description",
                        },
                        "timestamp": {
                            "format": "date-time",
                            "title": "Timestamp",
                            "type": "string",
                        },
                        "title": {
                            "title": "Title",
                            "type": "string",
                        },
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
    }
