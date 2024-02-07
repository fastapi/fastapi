from dirty_equals import IsDict
from fastapi.testclient import TestClient

from docs_src.request_files.tutorial001_02 import app

client = TestClient(app)


def test_post_form_no_body():
    response = client.post("/files/")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "No file sent"}


def test_post_uploadfile_no_body():
    response = client.post("/uploadfile/")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "No upload file sent"}


def test_post_file(tmp_path):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")

    client = TestClient(app)
    with path.open("rb") as file:
        response = client.post("/files/", files={"file": file})
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 14}


def test_post_upload_file(tmp_path):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")

    client = TestClient(app)
    with path.open("rb") as file:
        response = client.post("/uploadfile/", files={"file": file})
    assert response.status_code == 200, response.text
    assert response.json() == {"filename": "test.txt"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/files/": {
                "post": {
                    "summary": "Create File",
                    "operationId": "create_file_files__post",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": IsDict(
                                    {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/Body_create_file_files__post"
                                            }
                                        ],
                                        "title": "Body",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {
                                        "$ref": "#/components/schemas/Body_create_file_files__post"
                                    }
                                )
                            }
                        }
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
            "/uploadfile/": {
                "post": {
                    "summary": "Create Upload File",
                    "operationId": "create_upload_file_uploadfile__post",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": IsDict(
                                    {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/Body_create_upload_file_uploadfile__post"
                                            }
                                        ],
                                        "title": "Body",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {
                                        "$ref": "#/components/schemas/Body_create_upload_file_uploadfile__post"
                                    }
                                )
                            }
                        }
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
        },
        "components": {
            "schemas": {
                "Body_create_file_files__post": {
                    "title": "Body_create_file_files__post",
                    "type": "object",
                    "properties": {
                        "file": IsDict(
                            {
                                "title": "File",
                                "anyOf": [
                                    {"type": "string", "format": "binary"},
                                    {"type": "null"},
                                ],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "File", "type": "string", "format": "binary"}
                        )
                    },
                },
                "Body_create_upload_file_uploadfile__post": {
                    "title": "Body_create_upload_file_uploadfile__post",
                    "type": "object",
                    "properties": {
                        "file": IsDict(
                            {
                                "title": "File",
                                "anyOf": [
                                    {"type": "string", "format": "binary"},
                                    {"type": "null"},
                                ],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "File", "type": "string", "format": "binary"}
                        )
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
