import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from docs_src.request_forms_and_files.tutorial001 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/files/": {
            "post": {
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
        }
    },
    "components": {
        "schemas": {
            "Address": {
                "title": "Address",
                "required": ["first_line", "postcode"],
                "type": "object",
                "properties": {
                    "first_line": {"title": "First Line", "type": "string"},
                    "postcode": {"title": "Postcode", "type": "string"},
                },
            },
            "Body_create_file_files__post": {
                "title": "Body_create_file_files__post",
                "required": ["file", "fileb", "token", "user"],
                "type": "object",
                "properties": {
                    "file": {"title": "File", "type": "string", "format": "binary"},
                    "fileb": {"title": "Fileb", "type": "string", "format": "binary"},
                    "token": {"title": "Token", "type": "string"},
                    "user": {"$ref": "#/components/schemas/User"},
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
            "User": {
                "title": "User",
                "required": ["first_name", "last_name", "address"],
                "type": "object",
                "properties": {
                    "first_name": {"title": "First Name", "type": "string"},
                    "last_name": {"title": "Last Name", "type": "string"},
                    "address": {
                        "title": "Address",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Address"},
                    },
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


file_required = {
    "loc": ["body", "file"],
    "msg": "field required",
    "type": "value_error.missing",
}
fileb_required = {
    "loc": ["body", "fileb"],
    "msg": "field required",
    "type": "value_error.missing",
}
token_required = {
    "loc": ["body", "token"],
    "msg": "field required",
    "type": "value_error.missing",
}
user_required = {
    "loc": ["body", "user"],
    "msg": "field required",
    "type": "value_error.missing",
}
test_user = {
    "first_name": "Bob",
    "last_name": "England",
    "address": [{"first_line": "1 Buckingham Ave", "postcode": "E1 0RR"}],
}
test_user_string = json.dumps(test_user)
files_required_detail = {"detail": [file_required, fileb_required]}
fileb_token_required_detail = {"detail": [fileb_required, token_required]}
all_required = {
    "detail": [file_required, fileb_required, token_required, user_required]
}


@pytest.mark.parametrize(
    "params,expected",
    [
        ({}, all_required),
        ({"data": {"token": "foo", "user": test_user_string}}, files_required_detail),
        (
            {"json": {"file": "Foo", "token": "Bar", "user": test_user_string}},
            all_required,
        ),
    ],
)
def test_post_form_body(params, expected):
    response = client.post("/files/", **params)
    assert response.status_code == 422, response.text
    assert response.json() == expected


def test_post_file_no_token(tmpdir):
    path = os.path.join(tmpdir, "test.txt")
    with open(path, "wb") as file:
        file.write(b"<file content>")

    client = TestClient(app)
    response = client.post(
        "/files/", files={"file": open(path, "rb")}, data={"user": test_user_string}
    )
    assert response.status_code == 422, response.text
    assert response.json() == fileb_token_required_detail


@pytest.mark.parametrize(
    "user_string,status_code,expected",
    [
        (
            test_user_string,
            200,
            {
                "file_size": 14,
                "token": "foo",
                "user": test_user,
                "fileb_content_type": "text/plain",
            },
        ),
        (
            "{}",
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "user", "first_name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user", "last_name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user", "address"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ],
            },
        ),
        (
            ",",
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "user"],
                        "msg": "Invalid JSON",
                        "type": "value_error.json",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "value is not a valid dict",
                        "type": "type_error.dict",
                    },
                ],
            },
        ),
        (
            "",
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "user"],
                        "msg": "Invalid JSON",
                        "type": "value_error.json",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ],
            },
        ),
    ],
)
def test_post_files_and_token_user(tmpdir, user_string, status_code, expected):
    patha = Path(tmpdir) / "test.txt"
    pathb = Path(tmpdir) / "testb.txt"
    patha.write_text("<file content>")
    pathb.write_text("<file b content>")

    client = TestClient(app)
    response = client.post(
        "/files/",
        data={"token": "foo", "user": user_string},
        files={
            "file": patha.open("rb"),
            "fileb": ("testb.txt", pathb.open("rb"), "text/plain"),
        },
    )
    assert response.status_code == status_code, response.text
    assert response.json() == expected
