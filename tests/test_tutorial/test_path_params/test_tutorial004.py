from fastapi.testclient import TestClient

from docs_src.path_params.tutorial004 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/files/{file_path}": {
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
                "summary": "Read File",
                "operationId": "read_file_files__file_path__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "File Path", "type": "string"},
                        "name": "file_path",
                        "in": "path",
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_file_path():
    response = client.get("/files/home/johndoe/myfile.txt")
    print(response.content)
    assert response.status_code == 200, response.text
    assert response.json() == {"file_path": "home/johndoe/myfile.txt"}


def test_root_file_path():
    response = client.get("/files//home/johndoe/myfile.txt")
    print(response.content)
    assert response.status_code == 200, response.text
    assert response.json() == {"file_path": "/home/johndoe/myfile.txt"}
