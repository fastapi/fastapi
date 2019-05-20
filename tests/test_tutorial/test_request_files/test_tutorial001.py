import os

from starlette.testclient import TestClient

from request_files.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/files/": {
            "post": {
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
                "summary": "Create File",
                "operationId": "create_file_files__post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {"$ref": "#/components/schemas/Body_create_file"}
                        }
                    },
                    "required": True,
                },
            }
        },
        "/uploadfile/": {
            "post": {
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
                "summary": "Create Upload File",
                "operationId": "create_upload_file_uploadfile__post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_create_upload_file"
                            }
                        }
                    },
                    "required": True,
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Body_create_file": {
                "title": "Body_create_file",
                "required": ["file"],
                "type": "object",
                "properties": {
                    "file": {"title": "File", "type": "string", "format": "binary"}
                },
            },
            "Body_create_upload_file": {
                "title": "Body_create_upload_file",
                "required": ["file"],
                "type": "object",
                "properties": {
                    "file": {"title": "File", "type": "string", "format": "binary"}
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
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


file_required = {
    "detail": [
        {
            "loc": ["body", "file"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}


def test_post_form_no_body():
    response = client.post("/files/")
    assert response.status_code == 422
    assert response.json() == file_required


def test_post_body_json():
    response = client.post("/files/", json={"file": "Foo"})
    assert response.status_code == 422
    assert response.json() == file_required


def test_post_file(tmpdir):
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "wb") as file:
        file.write(b"<file content>")

    client = TestClient(app)
    response = client.post("/files/", files={"file": open(path, "rb")})
    assert response.status_code == 200
    assert response.json() == {"file_size": 14}


def test_post_large_file(tmpdir):
    default_pydantic_max_size = 2 ** 16
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "wb") as file:
        file.write(b"x" * (default_pydantic_max_size + 1))

    client = TestClient(app)
    response = client.post("/files/", files={"file": open(path, "rb")})
    assert response.status_code == 200
    assert response.json() == {"file_size": default_pydantic_max_size + 1}


def test_post_upload_file(tmpdir):
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "wb") as file:
        file.write(b"<file content>")

    client = TestClient(app)
    response = client.post("/uploadfile/", files={"file": open(path, "rb")})
    assert response.status_code == 200
    assert response.json() == {"filename": "test.txt"}
