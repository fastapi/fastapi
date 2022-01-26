import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ...utils import needs_py39

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/files/": {
            "post": {
                "summary": "Create Files",
                "operationId": "create_files_files__post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_create_files_files__post"
                            }
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
        },
        "/uploadfiles/": {
            "post": {
                "summary": "Create Upload Files",
                "operationId": "create_upload_files_uploadfiles__post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_create_upload_files_uploadfiles__post"
                            }
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
        },
        "/": {
            "get": {
                "summary": "Main",
                "operationId": "main__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Body_create_files_files__post": {
                "title": "Body_create_files_files__post",
                "required": ["files"],
                "type": "object",
                "properties": {
                    "files": {
                        "title": "Files",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "description": "Multiple files as bytes",
                    }
                },
            },
            "Body_create_upload_files_uploadfiles__post": {
                "title": "Body_create_upload_files_uploadfiles__post",
                "required": ["files"],
                "type": "object",
                "properties": {
                    "files": {
                        "title": "Files",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "description": "Multiple files as UploadFile",
                    }
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
        }
    },
}


@pytest.fixture(name="app")
def get_app():
    from docs_src.request_files.tutorial003_py39 import app

    return app


@pytest.fixture(name="client")
def get_client(app: FastAPI):

    client = TestClient(app)
    return client


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


file_required = {
    "detail": [
        {
            "loc": ["body", "files"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}


@needs_py39
def test_post_files(tmp_path, app: FastAPI):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")
    path2 = tmp_path / "test2.txt"
    path2.write_bytes(b"<file content2>")

    client = TestClient(app)
    with path.open("rb") as file, path2.open("rb") as file2:
        response = client.post(
            "/files/",
            files=(
                ("files", ("test.txt", file)),
                ("files", ("test2.txt", file2)),
            ),
        )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_sizes": [14, 15]}


@needs_py39
def test_post_upload_file(tmp_path, app: FastAPI):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")
    path2 = tmp_path / "test2.txt"
    path2.write_bytes(b"<file content2>")

    client = TestClient(app)
    with path.open("rb") as file, path2.open("rb") as file2:
        response = client.post(
            "/uploadfiles/",
            files=(
                ("files", ("test.txt", file)),
                ("files", ("test2.txt", file2)),
            ),
        )
    assert response.status_code == 200, response.text
    assert response.json() == {"filenames": ["test.txt", "test2.txt"]}


@needs_py39
def test_get_root(app: FastAPI):
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert b"<form" in response.content
