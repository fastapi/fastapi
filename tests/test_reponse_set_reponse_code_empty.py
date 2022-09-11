from typing import Any

from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


@app.delete(
    "/{id}",
    status_code=204,
)
async def delete_deployment(
    id: int,
    response: Response,
) -> Any:
    response.status_code = 400
    return {"msg": "Status overwritten", "id": id}


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/{id}": {
            "delete": {
                "summary": "Delete Deployment",
                "operationId": "delete_deployment__id__delete",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Id", "type": "integer"},
                        "name": "id",
                        "in": "path",
                    }
                ],
                "responses": {
                    "204": {"description": "Successful Response"},
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
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_dependency_set_status_code():
    response = client.delete("/1")
    assert response.status_code == 400 and response.content
    assert response.json() == {"msg": "Status overwritten", "id": 1}
