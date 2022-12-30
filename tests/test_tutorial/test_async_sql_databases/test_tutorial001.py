from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from docs_src.async_sql_databases.tutorial001 import app

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/notes/": {
            "get": {
                "summary": "Read Notes",
                "operationId": "read_notes_notes__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Read Notes Notes  Get",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Note"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "summary": "Create Note",
                "operationId": "create_note_notes__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NoteIn"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Note"}
                            }
                        },
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
            },
        },
        "/notes/{note_id}/": {
            "get": {
                "summary": "Read One Note",
                "operationId": "read_one_note_notes__note_id___get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Note Id", "type": "integer"},
                        "name": "note_id",
                        "in": "path",
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Note"}
                            }
                        },
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
            },
            "put": {
                "summary": "Update Note",
                "operationId": "update_note_notes__note_id___put",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Note Id", "type": "integer"},
                        "name": "note_id",
                        "in": "path",
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/NoteIn"}
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
            },
            "delete": {
                "summary": "Delete Note",
                "operationId": "delete_note_notes__note_id___delete",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Note Id", "type": "integer"},
                        "name": "note_id",
                        "in": "path",
                    }
                ],
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
            },
        },
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
            "Note": {
                "title": "Note",
                "required": ["text", "completed", "id"],
                "type": "object",
                "properties": {
                    "text": {"title": "Text", "type": "string"},
                    "completed": {"title": "Completed", "type": "boolean"},
                    "id": {"title": "Id", "type": "integer"},
                },
            },
            "NoteIn": {
                "title": "NoteIn",
                "required": ["text", "completed"],
                "type": "object",
                "properties": {
                    "text": {"title": "Text", "type": "string"},
                    "completed": {"title": "Completed", "type": "boolean"},
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


note = {"text": "Foo bar", "completed": False}
completed_note = {"text": "Foo bar", "completed": True}


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
    db_file = Path("./test.db")
    if db_file.is_file():
        db_file.unlink()


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_create(client):
    response = client.post("/notes/", json=note)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["text"] == note["text"]
    assert data["completed"] == note["completed"]


def test_read(client):
    response = client.get("/notes/1/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["text"] == note["text"]
    assert data["completed"] == note["completed"]
    response = client.get("/notes/")
    assert response.status_code == 200, response.text
    assert data in response.json()


def test_update(client):
    response = client.put("/notes/1/", json=completed_note)
    assert response.status_code == 200, response.text
    data = {"id": 1, **completed_note}
    response = client.get("/notes/")
    assert response.status_code == 200, response.text
    assert data in response.json()


def test_delete(client):
    response = client.delete("/notes/1/")
    assert response.status_code == 200, response.text
    response = client.get("/notes/")
    assert response.status_code == 200, response.text
    data = {"id": 1, **completed_note}
    assert data not in response.json()


def test_error_responses(client):
    def check_response(response):
        assert response.status_code == 404, response.text
        assert response.json() == {"detail": "Note not found"}

    check_response(client.get("/notes/100/"))
    check_response(client.put("/notes/100/", json=completed_note))
    check_response(client.delete("/notes/100/"))
