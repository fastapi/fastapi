import os
from pathlib import Path

from starlette.testclient import TestClient

from request_forms_and_files.tutorial001 import app

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
                            "schema": {
                                "$ref": "#/components/schemas/Body_create_file_files__post"
                            }
                        }
                    },
                    "required": True,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_create_file_files__post": {
                "title": "Body_create_file_files__post",
                "required": ["file", "fileb", "token"],
                "type": "object",
                "properties": {
                    "file": {"title": "File", "type": "string", "format": "binary"},
                    "fileb": {"title": "Fileb", "type": "string", "format": "binary"},
                    "token": {"title": "Token", "type": "string"},
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
        },
        {
            "loc": ["body", "fileb"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}

token_required = {
    "detail": [
        {
            "loc": ["body", "fileb"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}

# {'detail': [, {'loc': ['body', 'token'], 'msg': 'field required', 'type': 'value_error.missing'}]}

file_and_token_required = {
    "detail": [
        {
            "loc": ["body", "file"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "fileb"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}


def test_post_form_no_body():
    response = client.post("/files/")
    assert response.status_code == 422
    assert response.json() == file_and_token_required


def test_post_form_no_file():
    response = client.post("/files/", data={"token": "foo"})
    assert response.status_code == 422
    assert response.json() == file_required


def test_post_body_json():
    response = client.post("/files/", json={"file": "Foo", "token": "Bar"})
    assert response.status_code == 422
    assert response.json() == file_and_token_required


def test_post_file_no_token(tmpdir):
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "wb") as file:
        file.write(b"<file content>")

    client = TestClient(app)
    response = client.post("/files/", files={"file": open(path, "rb")})
    assert response.status_code == 422
    assert response.json() == token_required


def test_post_files_and_token(tmpdir):
    patha = Path(tmpdir) / "test.txt"
    pathb = Path(tmpdir) / "testb.txt"
    patha.write_text("<file content>")
    pathb.write_text("<file b content>")

    client = TestClient(app)
    response = client.post(
        "/files/",
        data={"token": "foo"},
        files={
            "file": patha.open("rb"),
            "fileb": ("testb.txt", pathb.open("rb"), "text/plain"),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "file_size": 14,
        "token": "foo",
        "fileb_content_type": "text/plain",
    }
