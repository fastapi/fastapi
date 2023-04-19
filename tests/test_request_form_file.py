from typing import Annotated

from fastapi import FastAPI, File, Form
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/files/")
async def create_file(token: Annotated[str, Form()], file: Annotated[bytes, File()]):
    return {
        "file_size": len(file),
        "token": token,
    }


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
            "Body_create_file_files__post": {
                "title": "Body_create_file_files__post",
                "required": ["token", "file"],
                "type": "object",
                "properties": {
                    "token": {"title": "Token", "type": "string"},
                    "file": {"title": "File", "type": "string", "format": "binary"},
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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
    "detail": [
        {
            "loc": ["body", "file"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}

token_required = {
    "detail": [
        {
            "loc": ["body", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}

file_and_token_required = {
    "detail": [
        {
            "loc": ["body", "token"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "file"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}


def test_post_form_no_body():
    response = client.post("/files/")
    assert response.status_code == 422, response.text
    assert response.json() == file_and_token_required


def test_post_form_no_file():
    response = client.post("/files/", data={"token": "foo"})
    assert response.status_code == 422, response.text
    assert response.json() == file_required


def test_post_body_json():
    response = client.post("/files/", json={"file": "Foo", "token": "Bar"})
    assert response.status_code == 422, response.text
    assert response.json() == file_and_token_required


def test_post_file_no_token(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("<file content>")
    with path.open("rb") as file:
        response = client.post(
            "/files/",
            files={"file": file},
        )
    assert response.status_code == 422, response.text
    assert response.json() == token_required


def test_post_files_and_token(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("<file content>")
    with path.open("rb") as file:
        response = client.post(
            "/files/",
            data={"token": "foo"},
            files={"file": file},
        )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 14, "token": "foo"}
