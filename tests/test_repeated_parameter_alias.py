from fastapi import FastAPI, Path, Query, status
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/{repeated_alias}")
def get_parameters_with_repeated_aliases(
    path: str = Path(..., alias="repeated_alias"),
    query: str = Query(..., alias="repeated_alias"),
):
    return {"path": path, "query": query}


client = TestClient(app)


def test_get_parameters():
    response = client.get("/test_path", params={"repeated_alias": "test_query"})
    assert response.status_code == 200, response.text
    assert response.json() == {"path": "test_path", "query": "test_query"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    actual_schema = response.json()
    assert actual_schema == {
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "title": "Detail",
                            "type": "array",
                        }
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
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
            }
        },
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "openapi": "3.1.0",
        "paths": {
            "/{repeated_alias}": {
                "get": {
                    "operationId": "get_parameters_with_repeated_aliases__repeated_alias__get",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "repeated_alias",
                            "required": True,
                            "schema": {"title": "Repeated Alias", "type": "string"},
                        },
                        {
                            "in": "query",
                            "name": "repeated_alias",
                            "required": True,
                            "schema": {"title": "Repeated Alias", "type": "string"},
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
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Get Parameters With Repeated Aliases",
                }
            }
        },
    }
