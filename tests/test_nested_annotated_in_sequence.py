from typing import Annotated

from dirty_equals import IsList
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import Field

MaxSizedSet = Annotated[set[str], Field(max_length=3)]

app = FastAPI()


@app.get("/")
def read_root(foo: Annotated[MaxSizedSet | None, Query()] = None):
    return {"foo": foo}


client = TestClient(app)


def test_endpoint_none():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"foo": None}


def test_endpoint_valid():
    response = client.get("/", params={"foo": ["a", "b"]})
    assert response.status_code == 200
    assert response.json() == {"foo": IsList("a", "b", check_order=False)}


def test_endpoint_too_long():
    response = client.get("/", params={"foo": ["a", "b", "c", "d"]})
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "too_long",
                    "loc": ["query", "foo"],
                    "msg": "Set should have at most 3 items after validation, not more",
                    "input": IsList("a", "b", "c", "d", check_order=False),
                    "ctx": {
                        "actual_length": None,
                        "field_type": "Set",
                        "max_length": 3,
                    },
                }
            ]
        }
    )


def test_openapi():
    assert app.openapi() == snapshot(
        {
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "title": "Detail",
                                "type": "array",
                            },
                        },
                        "title": "HTTPValidationError",
                        "type": "object",
                    },
                    "ValidationError": {
                        "properties": {
                            "ctx": {"title": "Context", "type": "object"},
                            "input": {"title": "Input"},
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}],
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
            "info": {
                "title": "FastAPI",
                "version": "0.1.0",
            },
            "openapi": "3.1.0",
            "paths": {
                "/": {
                    "get": {
                        "operationId": "read_root__get",
                        "parameters": [
                            {
                                "in": "query",
                                "name": "foo",
                                "required": False,
                                "schema": {
                                    "anyOf": [
                                        {
                                            "items": {"type": "string"},
                                            "maxItems": 3,
                                            "type": "array",
                                            "uniqueItems": True,
                                        },
                                        {"type": "null"},
                                    ],
                                    "title": "Foo",
                                },
                            },
                        ],
                        "responses": {
                            "200": {
                                "content": {"application/json": {"schema": {}}},
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
                        "summary": "Read Root",
                    },
                },
            },
        }
    )
