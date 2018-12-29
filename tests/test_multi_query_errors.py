from typing import List

from fastapi import FastAPI, Query
from starlette.testclient import TestClient

app = FastAPI()


@app.get("/items/")
def read_items(q: List[int] = Query(None)):
    return {"q": q}


client = TestClient(app)


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

multiple_errors = {
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_multi_query():
    response = client.get("/items/?q=5&q=6")
    assert response.status_code == 200
    assert response.json() == {"q": [5, 6]}


def test_multi_query_incorrect():
    response = client.get("/items/?q=five&q=six")
    assert response.status_code == 422
    assert response.json() == multiple_errors
