from typing import Annotated

import pytest
from fastapi import FastAPI, File, Form, UploadFile, params
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

app = FastAPI()


@app.post("/required-bytes")
def read_required_bytes(
    file: Annotated[bytes | None, File()],
    files: Annotated[list[bytes] | None, File()],
):
    assert file is not None
    assert files is not None
    return {"file": len(file), "files": [len(value) for value in files]}


@app.post("/required-uploadfile")
def read_required_uploadfile(
    file: Annotated[UploadFile | None, File()],
    files: Annotated[list[UploadFile] | None, File()],
):
    assert file is not None
    assert files is not None
    return {"file": file.size, "files": [value.size for value in files]}


@app.post("/optional-bytes")
def read_optional_bytes(
    file: Annotated[bytes | None, File()] = None,
    files: Annotated[list[bytes] | None, File()] = None,
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(value) for value in files] if files is not None else None,
    }


@app.post("/optional-uploadfile")
def read_optional_uploadfile(
    file: Annotated[UploadFile | None, File()] = None,
    files: Annotated[list[UploadFile] | None, File()] = None,
):
    return {
        "file": file.size if file is not None else None,
        "files": [value.size for value in files] if files is not None else None,
    }


@app.post("/bytes-defaults")
def read_bytes_defaults(
    *,
    file: Annotated[bytes | None, File()] = b"default",
    files: Annotated[list[bytes] | None, File(default_factory=lambda: [b"default"])],
):
    assert file is not None
    assert files is not None
    return {"file": len(file), "files": [len(value) for value in files]}


client = TestClient(app)

# HTTPX drops empty filenames, so send the browser's multipart representation directly.
EMPTY_FILE_FORM = (
    b"--boundary\r\n"
    b'Content-Disposition: form-data; name="file"; filename=""\r\n'
    b"Content-Type: application/octet-stream\r\n\r\n"
    b"\r\n--boundary\r\n"
    b'Content-Disposition: form-data; name="files"; filename=""\r\n'
    b"Content-Type: application/octet-stream\r\n\r\n"
    b"\r\n--boundary--\r\n"
)


@pytest.mark.parametrize("path", ["/required-bytes", "/required-uploadfile"])
@pytest.mark.parametrize(
    "content",
    [
        pytest.param(b"", id="omitted"),
        pytest.param(EMPTY_FILE_FORM, id="no-selection"),
    ],
)
def test_missing_required_nullable_files(path, content):
    response = client.post(
        path,
        content=content,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "file"]),
        ("missing", ["body", "files"]),
    ]


@pytest.mark.parametrize("path", ["/optional-bytes", "/optional-uploadfile"])
@pytest.mark.parametrize(
    "content",
    [
        pytest.param(b"", id="omitted"),
        pytest.param(EMPTY_FILE_FORM, id="no-selection"),
    ],
)
def test_missing_optional_nullable_files(path, content):
    response = client.post(
        path,
        content=content,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {"file": None, "files": None}


@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes",
        "/required-uploadfile",
        "/optional-bytes",
        "/optional-uploadfile",
    ],
)
@pytest.mark.parametrize("content", [b"", b"hello"])
def test_named_file_is_supplied_even_when_empty(path, content):
    response = client.post(
        path,
        files=[
            ("file", ("empty.txt", content)),
            ("files", ("first.txt", content)),
            ("files", ("second.txt", content)),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "file": len(content),
        "files": [len(content), len(content)],
    }


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(b"", id="omitted"),
        pytest.param(EMPTY_FILE_FORM, id="no-selection"),
    ],
)
def test_missing_files_use_bytes_defaults(content):
    response = client.post(
        "/bytes-defaults",
        content=content,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {"file": 7, "files": [7]}


@pytest.mark.parametrize("content,expected", [(b"", 0), (b"hello", 5)])
def test_supplied_files_override_bytes_defaults(content, expected):
    response = client.post(
        "/bytes-defaults",
        files=[
            ("file", ("file.txt", content)),
            ("files", ("file.txt", content)),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"file": expected, "files": [expected]}


@pytest.mark.parametrize("path", ["/required-bytes", "/required-uploadfile"])
def test_file_without_a_name_is_supplied_when_it_has_content(path):
    response = client.post(
        path,
        content=(
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="file"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"hello\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="files"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"hello\r\n--boundary--\r\n"
        ),
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {"file": 5, "files": [5]}


@pytest.mark.parametrize("path", ["/required-bytes", "/required-uploadfile"])
def test_file_list_ignores_unselected_inputs(path):
    response = client.post(
        path,
        content=(
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="file"; filename="empty.txt"\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="files"; filename="first.txt"\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="files"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="files"; filename="last.txt"\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"hello\r\n--boundary--\r\n"
        ),
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {"file": 0, "files": [0, 5]}


def test_multipart_text_items_in_bytes_list_are_preserved():
    response = client.post(
        "/required-bytes",
        files=[
            ("file", ("empty.txt", b"")),
            ("files", (None, "")),
            ("files", (None, "text")),
            ("files", ("selected.txt", b"hello")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"file": 0, "files": [0, 4, 5]}


def test_unselected_files_in_form_model_use_defaults_and_remain_unset():
    app = FastAPI()

    class FileModel(BaseModel):
        file: UploadFile | None = None
        files: Annotated[list[UploadFile], Field(default_factory=list)]

    @app.post("/")
    def upload(params: Annotated[FileModel, Form()]):
        assert params.file is None
        assert params.files == []
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(
        "/",
        content=EMPTY_FILE_FORM,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == {}


def test_required_non_nullable_files():
    app = FastAPI()

    @app.post("/")
    def upload(
        file: Annotated[UploadFile, File()], files: Annotated[list[bytes], File()]
    ):
        return {"file": file.size, "files": [len(value) for value in files]}

    client = TestClient(app)
    response = client.post(
        "/",
        content=EMPTY_FILE_FORM,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "file"]),
        ("missing", ["body", "files"]),
    ]

    response = client.post(
        "/",
        files=[("file", ("empty.txt", b"")), ("files", ("empty.txt", b""))],
    )
    assert response.status_code == 200
    assert response.json() == {"file": 0, "files": [0]}


@pytest.mark.parametrize("alias", ["primary", "secondary"])
def test_individual_file_alias_choices(alias: str):
    app = FastAPI()

    @app.post("/")
    def read_file(
        file: Annotated[
            bytes,
            File(alias="legacy", validation_alias=AliasChoices("primary", "secondary")),
        ],
    ):
        return file.decode()

    client = TestClient(app)
    response = client.post("/", files={alias: ("hello.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == "hello"


def test_file_alias_choices_errors_use_selected_aliases():
    app = FastAPI()

    @app.post("/")
    def read_files(
        file: Annotated[
            UploadFile,
            File(alias="legacy", validation_alias=AliasChoices("primary", "secondary")),
        ],
        files: Annotated[
            list[UploadFile],
            File(validation_alias=AliasChoices("primary-files", "secondary-files")),
        ],
    ):
        return {"file": file.filename, "files": [item.filename for item in files]}

    client = TestClient(app)
    response = client.post(
        "/",
        files=[
            ("secondary", ("one.txt", b"one")),
            ("secondary-files", ("two.txt", b"two")),
            ("secondary-files", ("three.txt", b"three")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"file": "one.txt", "files": ["two.txt", "three.txt"]}

    response = client.post(
        "/",
        files=[
            ("secondary", (None, "invalid")),
            ("secondary-files", ("valid.txt", b"valid")),
            ("secondary-files", (None, "invalid")),
            ("legacy", ("ignored.txt", b"ignored")),
        ],
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("value_error", ["body", "secondary"]),
        ("value_error", ["body", "secondary-files", 1]),
    ]

    response = client.post(
        "/",
        files=[
            ("primary", (None, "invalid")),
            ("secondary", ("valid.txt", b"valid")),
            ("primary-files", (None, "invalid")),
            ("secondary-files", ("valid.txt", b"valid")),
        ],
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("value_error", ["body", "primary"]),
        ("value_error", ["body", "primary-files", 0]),
    ]

    response = client.post("/")
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "primary"]),
        ("missing", ["body", "primary-files"]),
    ]


def test_unselected_file_alias_choices_use_the_next_alias():
    app = FastAPI()

    @app.post("/")
    def read_file(
        file: Annotated[
            bytes,
            File(alias="legacy", validation_alias=AliasChoices("file", "selected")),
        ],
    ):
        return file.decode()

    client = TestClient(app)
    response = client.post(
        "/",
        content=(
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="file"; filename=""\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"\r\n--boundary\r\n"
            b'Content-Disposition: form-data; name="selected"; filename="hello.txt"\r\n'
            b"Content-Type: application/octet-stream\r\n\r\n"
            b"hello\r\n--boundary--\r\n"
        ),
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 200
    assert response.json() == "hello"

    response = client.post(
        "/",
        content=EMPTY_FILE_FORM,
        headers={"content-type": "multipart/form-data; boundary=boundary"},
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "file"]),
    ]


@pytest.mark.parametrize(
    "file_alias,files_alias",
    [("primary", "primary-files"), ("secondary", "secondary-files"), ("file", "files")],
)
def test_model_bytes_files_use_validation_aliases(file_alias, files_alias):
    app = FastAPI()

    class FileModel(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        file: Annotated[
            bytes, File(validation_alias=AliasChoices("primary", "secondary"))
        ]
        files: Annotated[
            list[bytes],
            File(validation_alias=AliasChoices("primary-files", "secondary-files")),
        ]

    if not isinstance(FileModel.model_fields["file"], params.File):
        pytest.skip("This Pydantic version does not preserve File metadata in models")

    @app.post("/")
    def read_form(data: Annotated[FileModel, Form()]):
        return data

    client = TestClient(app)
    response = client.post(
        "/",
        files=[
            (file_alias, ("one.txt", b"one")),
            (files_alias, ("two.txt", b"two")),
            (files_alias, ("three.txt", b"three")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"file": "one", "files": ["two", "three"]}


def test_model_files_can_share_an_unused_alias_choice():
    app = FastAPI()

    class FileModel(BaseModel):
        files: Annotated[
            list[UploadFile], Field(validation_alias=AliasChoices("files", "legacy"))
        ]
        file: Annotated[
            UploadFile, Field(validation_alias=AliasChoices("file", "legacy"))
        ]

    @app.post("/")
    def read_form(data: Annotated[FileModel, Form()]):
        return {
            "files": [file.filename for file in data.files],
            "file": data.file.filename,
        }

    client = TestClient(app)
    response = client.post(
        "/",
        files=[
            ("legacy", ("one.txt", b"one")),
            ("legacy", ("two.txt", b"two")),
            ("file", ("hello.txt", b"hello")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"files": ["one.txt", "two.txt"], "file": "hello.txt"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/required-bytes": {
                    "post": {
                        "summary": "Read Required Bytes",
                        "operationId": "read_required_bytes_required_bytes_post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_required_bytes_required_bytes_post"
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
                "/required-uploadfile": {
                    "post": {
                        "summary": "Read Required Uploadfile",
                        "operationId": "read_required_uploadfile_required_uploadfile_post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_required_uploadfile_required_uploadfile_post"
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
                "/optional-bytes": {
                    "post": {
                        "summary": "Read Optional Bytes",
                        "operationId": "read_optional_bytes_optional_bytes_post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_optional_bytes_optional_bytes_post"
                                    }
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
                "/optional-uploadfile": {
                    "post": {
                        "summary": "Read Optional Uploadfile",
                        "operationId": "read_optional_uploadfile_optional_uploadfile_post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_optional_uploadfile_optional_uploadfile_post"
                                    }
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
                "/bytes-defaults": {
                    "post": {
                        "summary": "Read Bytes Defaults",
                        "operationId": "read_bytes_defaults_bytes_defaults_post",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_bytes_defaults_bytes_defaults_post"
                                    }
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
                    "Body_read_bytes_defaults_bytes_defaults_post": {
                        "properties": {
                            "file": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "File",
                                "default": "default",
                            },
                            "files": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        "type": "array",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "Files",
                            },
                        },
                        "type": "object",
                        "title": "Body_read_bytes_defaults_bytes_defaults_post",
                    },
                    "Body_read_optional_bytes_optional_bytes_post": {
                        "properties": {
                            "file": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "File",
                            },
                            "files": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        "type": "array",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "Files",
                            },
                        },
                        "type": "object",
                        "title": "Body_read_optional_bytes_optional_bytes_post",
                    },
                    "Body_read_optional_uploadfile_optional_uploadfile_post": {
                        "properties": {
                            "file": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "File",
                            },
                            "files": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        "type": "array",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "Files",
                            },
                        },
                        "type": "object",
                        "title": "Body_read_optional_uploadfile_optional_uploadfile_post",
                    },
                    "Body_read_required_bytes_required_bytes_post": {
                        "properties": {
                            "file": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "File",
                            },
                            "files": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        "type": "array",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "Files",
                            },
                        },
                        "type": "object",
                        "required": ["file", "files"],
                        "title": "Body_read_required_bytes_required_bytes_post",
                    },
                    "Body_read_required_uploadfile_required_uploadfile_post": {
                        "properties": {
                            "file": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "File",
                            },
                            "files": {
                                "anyOf": [
                                    {
                                        "items": {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        "type": "array",
                                    },
                                    {"type": "null"},
                                ],
                                "title": "Files",
                            },
                        },
                        "type": "object",
                        "required": ["file", "files"],
                        "title": "Body_read_required_uploadfile_required_uploadfile_post",
                    },
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                            "input": {"title": "Input"},
                            "ctx": {"type": "object", "title": "Context"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
