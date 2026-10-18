from typing import Annotated

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot

from .utils import get_body_model_name

app = FastAPI()


# =====================================================================================
# Nullable required


@app.post("/nullable-required-bytes")
async def read_nullable_required_bytes(
    file: Annotated[bytes | None, File()],
    files: Annotated[list[bytes] | None, File()],
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(f) for f in files] if files is not None else None,
    }


@app.post("/nullable-required-uploadfile")
async def read_nullable_required_uploadfile(
    file: Annotated[UploadFile | None, File()],
    files: Annotated[list[UploadFile] | None, File()],
):
    return {
        "file": file.size if file is not None else None,
        "files": [f.size for f in files] if files is not None else None,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-bytes",
        "/nullable-required-uploadfile",
    ],
)
def test_nullable_required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert openapi["components"]["schemas"][body_model_name] == snapshot(
        {
            "properties": {
                "file": {
                    "title": "File",
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
                        },
                        {"type": "null"},
                    ],
                },
            },
            "required": ["file", "files"],
            "title": Is(body_model_name),
            "type": "object",
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-bytes",
        "/nullable-required-uploadfile",
    ],
)
def test_nullable_required_missing(path: str):
    client = TestClient(app)

    response = client.post(path)

    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "file"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
                {
                    "type": "missing",
                    "loc": ["body", "files"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-bytes",
        "/nullable-required-uploadfile",
    ],
)
def test_nullable_required_pass_empty_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[("file", b""), ("files", b""), ("files", b"")],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "file": 0,
        "files": [0, 0],
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-bytes",
        "/nullable-required-uploadfile",
    ],
)
def test_nullable_required_pass_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[
            ("file", b"test 1"),
            ("files", b"test 2"),
            ("files", b"test 3"),
        ],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}


# =====================================================================================
# Nullable with default=None


@app.post("/nullable-non-required-bytes")
async def read_nullable_non_required_bytes(
    file: Annotated[bytes | None, File()] = None,
    files: Annotated[list[bytes] | None, File()] = None,
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(f) for f in files] if files is not None else None,
    }


@app.post("/nullable-non-required-uploadfile")
async def read_nullable_non_required_uploadfile(
    file: Annotated[UploadFile | None, File()] = None,
    files: Annotated[list[UploadFile] | None, File()] = None,
):
    return {
        "file": file.size if file is not None else None,
        "files": [f.size for f in files] if files is not None else None,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-bytes",
        "/nullable-non-required-uploadfile",
    ],
)
def test_nullable_non_required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert openapi["components"]["schemas"][body_model_name] == snapshot(
        {
            "properties": {
                "file": {
                    "title": "File",
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
                        },
                        {"type": "null"},
                    ],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
            },
            "title": Is(body_model_name),
            "type": "object",
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-bytes",
        "/nullable-non-required-uploadfile",
    ],
)
def test_nullable_non_required_missing(path: str):
    client = TestClient(app)

    response = client.post(path)

    assert response.status_code == 200
    assert response.json() == {
        "file": None,
        "files": None,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-bytes",
        "/nullable-non-required-uploadfile",
    ],
)
def test_nullable_non_required_pass_empty_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[("file", b""), ("files", b""), ("files", b"")],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"file": 0, "files": [0, 0]}


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-bytes",
        "/nullable-non-required-uploadfile",
    ],
)
def test_nullable_non_required_pass_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[("file", b"test 1"), ("files", b"test 2"), ("files", b"test 3")],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}


# =====================================================================================
# Nullable with not-None default


@app.post("/nullable-with-non-null-default-bytes")
async def read_nullable_with_non_null_default_bytes(
    *,
    file: Annotated[bytes | None, File()] = b"default",
    files: Annotated[list[bytes] | None, File(default_factory=lambda: [b"default"])],
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(f) for f in files] if files is not None else None,
    }


# Note: It seems to be not possible to create endpoint with UploadFile and non-None default


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default-bytes",
    ],
)
def test_nullable_with_non_null_default_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert openapi["components"]["schemas"][body_model_name] == snapshot(
        {
            "properties": {
                "file": {
                    "title": "File",
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    "default": "default",  # <= Default value here looks strange to me
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
                        },
                        {"type": "null"},
                    ],
                },
            },
            "title": Is(body_model_name),
            "type": "object",
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-with-non-null-default-bytes",
            marks=pytest.mark.xfail(
                reason="AttributeError: 'bytes' object has no attribute 'read'",
            ),
        ),
    ],
)
def test_nullable_with_non_null_default_missing(path: str):
    client = TestClient(app)

    response = client.post(path)

    assert response.status_code == 200  # pragma: no cover
    assert response.json() == {"file": 7, "files": [7]}  # pragma: no cover
    # TODO: Remove 'no cover' when the issue is fixed


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default-bytes",
    ],
)
def test_nullable_with_non_null_default_pass_empty_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[("file", b""), ("files", b""), ("files", b"")],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"file": 0, "files": [0, 0]}


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default-bytes",
    ],
)
def test_nullable_with_non_null_default_pass_file(path: str):
    client = TestClient(app)

    response = client.post(
        path,
        files=[("file", b"test 1"), ("files", b"test 2"), ("files", b"test 3")],
    )

    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}
