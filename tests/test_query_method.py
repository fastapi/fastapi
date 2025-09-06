from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class QuerySchema(BaseModel):
    fields: list[str]
    filters: dict[str, str]


@app.query("/items/")
async def query_items(schema: QuerySchema):
    return {"items": [{"name": "Empanada"}, {"name": "Arepa"}], "schema": schema.model_dump()}


client = TestClient(app)


def test_query_method():
    body = {
        "fields": ["name", "description"],
        "filters": {"category": "food"}
    }
    response = client.request("QUERY", "/items/", json=body)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "items": [{"name": "Empanada"}, {"name": "Arepa"}],
        "schema": body
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "query": {
                    "summary": "Query Items",
                    "operationId": "query_items_items__query",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/QuerySchema"}
                            }
                        },
                        "required": True,
                    },
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
                }
            }
        },
        "components": {
            "schemas": {
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
                "QuerySchema": {
                    "title": "QuerySchema",
                    "required": ["fields", "filters"],
                    "type": "object",
                    "properties": {
                        "fields": {
                            "title": "Fields",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "filters": {
                            "title": "Filters",
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                    },
                },
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
            }
        },
    }