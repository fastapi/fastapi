import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial004 import app

client = TestClient(app)


test_data = [
    ("/files/data/monthly-2024.csv", {"file_path": "data/monthly-2024.csv"}),
    ("/files/home/johndoe/myfile.txt", {"file_path": "home/johndoe/myfile.txt"}),
    ("/files//home/johndoe/myfile.txt", {"file_path": "/home/johndoe/myfile.txt"}),
]


@pytest.mark.parametrize("url_path, expected_response", test_data)
def test_file_paths(url_path, expected_response):
    response = client.get(url_path)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
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
