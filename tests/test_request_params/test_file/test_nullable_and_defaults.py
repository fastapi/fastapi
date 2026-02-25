from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from pydantic import BeforeValidator
from starlette.datastructures import UploadFile as StarletteUploadFile

from .utils import get_body_model_name

app = FastAPI()


def convert(v: Any) -> Any:
    return v


# =====================================================================================
# Nullable required


@app.post("/nullable-required-bytes")
async def read_nullable_required_bytes(
    file: Annotated[
        bytes | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ],
    files: Annotated[
        list[bytes] | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ],
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(f) for f in files] if files is not None else None,
    }


@app.post("/nullable-required-uploadfile")
async def read_nullable_required_uploadfile(
    file: Annotated[
        UploadFile | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ],
    files: Annotated[
        list[UploadFile] | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ],
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
                    "anyOf": [{"type": "string", "contentMediaType": "application/octet-stream"}, {"type": "null"}],
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {"type": "string", "contentMediaType": "application/octet-stream"},
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[("file", b""), ("files", b""), ("files", b"")],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    call_args = [call_args_item.args for call_args_item in mock_convert.call_args_list]
    file_call_arg_1 = call_args[0][0]
    files_call_arg_1 = call_args[1][0]

    assert (
        (file_call_arg_1 == b"")  # file as bytes
        or isinstance(file_call_arg_1, StarletteUploadFile)  # file as UploadFile
    )
    assert (
        (files_call_arg_1 == [b"", b""])  # files as bytes
        or all(  # files as UploadFile
            isinstance(f, StarletteUploadFile) for f in files_call_arg_1
        )
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[
                ("file", b"test 1"),
                ("files", b"test 2"),
                ("files", b"test 3"),
            ],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}


# =====================================================================================
# Nullable with default=None


@app.post("/nullable-non-required-bytes")
async def read_nullable_non_required_bytes(
    file: Annotated[
        bytes | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    files: Annotated[
        list[bytes] | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {
        "file": len(file) if file is not None else None,
        "files": [len(f) for f in files] if files is not None else None,
    }


@app.post("/nullable-non-required-uploadfile")
async def read_nullable_non_required_uploadfile(
    file: Annotated[
        UploadFile | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    files: Annotated[
        list[UploadFile] | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
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
                    "anyOf": [{"type": "string", "contentMediaType": "application/octet-stream"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {"type": "string", "contentMediaType": "application/octet-stream"},
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[("file", b""), ("files", b""), ("files", b"")],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    call_args = [call_args_item.args for call_args_item in mock_convert.call_args_list]
    file_call_arg_1 = call_args[0][0]
    files_call_arg_1 = call_args[1][0]

    assert (
        (file_call_arg_1 == b"")  # file as bytes
        or isinstance(file_call_arg_1, StarletteUploadFile)  # file as UploadFile
    )
    assert (
        (files_call_arg_1 == [b"", b""])  # files as bytes
        or all(  # files as UploadFile
            isinstance(f, StarletteUploadFile) for f in files_call_arg_1
        )
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[("file", b"test 1"), ("files", b"test 2"), ("files", b"test 3")],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}


# =====================================================================================
# Nullable with not-None default


@app.post("/nullable-with-non-null-default-bytes")
async def read_nullable_with_non_null_default_bytes(
    *,
    file: Annotated[
        bytes | None,
        File(),
        BeforeValidator(lambda v: convert(v)),
    ] = b"default",
    files: Annotated[
        list[bytes] | None,
        File(default_factory=lambda: [b"default"]),
        BeforeValidator(lambda v: convert(v)),
    ],
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
                        {"type": "string", "contentMediaType": "application/octet-stream"},
                        {"type": "null"},
                    ],
                    "default": "default",  # <= Default value here looks strange to me
                },
                "files": {
                    "title": "Files",
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {"type": "string", "contentMediaType": "application/octet-stream"},
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (  # pragma: no cover
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200  # pragma: no cover
    assert response.json() == {"file": None, "files": None}  # pragma: no cover
    # TODO: Remove 'no cover' when the issue is fixed


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default-bytes",
    ],
)
def test_nullable_with_non_null_default_pass_empty_file(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[("file", b""), ("files", b""), ("files", b"")],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    call_args = [call_args_item.args for call_args_item in mock_convert.call_args_list]
    file_call_arg_1 = call_args[0][0]
    files_call_arg_1 = call_args[1][0]

    assert (
        (file_call_arg_1 == b"")  # file as bytes
        or isinstance(file_call_arg_1, StarletteUploadFile)  # file as UploadFile
    )
    assert (
        (files_call_arg_1 == [b"", b""])  # files as bytes
        or all(  # files as UploadFile
            isinstance(f, StarletteUploadFile) for f in files_call_arg_1
        )
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

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            files=[("file", b"test 1"), ("files", b"test 2"), ("files", b"test 3")],
        )

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {"file": 6, "files": [6, 6]}
