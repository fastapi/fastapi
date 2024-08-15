from typing import List

from dirty_equals import IsDict
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/")
def read_items(q: List[int] = Query(default=None)):
    return {"q": q}


client = TestClient(app)


def test_multi_query():
    response = client.get("/items/?q=5&q=6")
    assert response.status_code == 200, response.text
    assert response.json() == {"q": [5, 6]}


def test_multi_query_incorrect():
    response = client.get("/items/?q=five&q=six")
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "q", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "five",
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "q", 1],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "six",
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "q", 0],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                },
                {
                    "loc": ["query", "q", 1],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                },
            ]
        }
    )


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
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
                                "title": "Q",
                                "type": "array",
                                "items": {"type": "integer"},
                            },
                            "name": "q",
                            "in": "query",
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
