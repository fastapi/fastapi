from fastapi import Depends, FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()


def _get_client_key(client_id: str = Query(...)) -> str:
    return f"{client_id}_key"


def _get_client_tag(client_id: str | None = Query(None)) -> str | None:
    if client_id is None:
        return None
    return f"{client_id}_tag"


@app.get("/foo")
def foo_handler(
    client_key: str = Depends(_get_client_key),
    client_tag: str | None = Depends(_get_client_tag),
):
    return {"client_id": client_key, "client_tag": client_tag}


client = TestClient(app)


def test_get_invalid():
    response = client.get("/foo")
    assert response.status_code == 422


def test_get_valid():
    response = client.get("/foo", params={"client_id": "bar"})
    assert response.status_code == 200
    assert response.json() == {"client_id": "bar_key", "client_tag": "bar_tag"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
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
                            }
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
                "/foo": {
                    "get": {
                        "operationId": "foo_handler_foo_get",
                        "parameters": [
                            {
                                "in": "query",
                                "name": "client_id",
                                "required": True,
                                "schema": {"title": "Client Id", "type": "string"},
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
                        "summary": "Foo Handler",
                    }
                }
            },
        }
    )
