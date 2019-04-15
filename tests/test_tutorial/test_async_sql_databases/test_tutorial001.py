from starlette.testclient import TestClient

from async_sql_databases.tutorial001 import app

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/notes/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response_Read_Notes",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Note"},
                                }
                            }
                        },
                    }
                },
                "summary": "Read Notes",
                "operationId": "read_notes_notes__get",
            },
            "post": {
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
            },
        }
    },
    "components": {
        "schemas": {
            "NoteIn": {
                "title": "NoteIn",
                "required": ["text", "completed"],
                "type": "object",
                "properties": {
                    "text": {"title": "Text", "type": "string"},
                    "completed": {"title": "Completed", "type": "boolean"},
                },
            },
            "Note": {
                "title": "Note",
                "required": ["id", "text", "completed"],
                "type": "object",
                "properties": {
                    "id": {"title": "Id", "type": "integer"},
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


def test_openapi_schema():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json() == openapi_schema


def test_create_read():
    with TestClient(app) as client:
        note = {"text": "Foo bar", "completed": False}
        response = client.post("/notes/", json=note)
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == note["text"]
        assert data["completed"] == note["completed"]
        assert "id" in data
        response = client.get(f"/notes/")
        assert response.status_code == 200
        assert data in response.json()
