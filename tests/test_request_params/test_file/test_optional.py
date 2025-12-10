from typing import Optional

import pytest
from dirty_equals import IsDict
from fastapi import FastAPI, File, Form, UploadFile
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Annotated

from tests.utils import needs_pydanticv2

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-bytes", operation_id="optional_bytes")
async def read_optional_bytes(p: Annotated[Optional[bytes], File()] = None):
    return {"file_size": len(p) if p else None}


@app.post("/optional-uploadfile", operation_id="optional_uploadfile")
async def read_optional_uploadfile(p: Annotated[Optional[UploadFile], File()] = None):
    return {"file_size": p.size if p else None}


class FormModelOptionalBytes(BaseModel):
    p: Optional[bytes] = File(default=None)


@app.post("/model-optional-bytes", operation_id="model_optional_bytes")
async def read_model_optional_bytes(
    p: Annotated[
        FormModelOptionalBytes,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": len(p.p) if p.p else None}


class FormModelOptionalUploadFile(BaseModel):
    p: Optional[UploadFile] = File(default=None)


@app.post("/model-optional-uploadfile", operation_id="model_optional_uploadfile")
async def read_model_optional_uploadfile(
    p: Annotated[
        FormModelOptionalUploadFile,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": p.p.size if p.p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes",
        "/model-optional-bytes",
        "/optional-uploadfile",
        "/model-optional-uploadfile",
    ],
)
def test_optional_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": (
                IsDict(
                    {
                        "anyOf": [
                            {"type": "string", "format": "binary"},
                            {"type": "null"},
                        ],
                        "title": "P",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {"title": "P", "type": "string", "format": "binary"}
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes",
        "/model-optional-bytes",
        "/optional-uploadfile",
        "/model-optional-uploadfile",
    ],
)
def test_optional_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes",
        "/model-optional-bytes",
        "/optional-uploadfile",
        "/model-optional-uploadfile",
    ],
)
def test_optional(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200
    assert response.json() == {"file_size": 5}


# =====================================================================================
# Alias


@app.post("/optional-bytes-alias", operation_id="optional_bytes_alias")
async def read_optional_bytes_alias(
    p: Annotated[Optional[bytes], File(alias="p_alias")] = None,
):
    return {"file_size": len(p) if p else None}


@app.post("/optional-uploadfile-alias", operation_id="optional_uploadfile_alias")
async def read_optional_uploadfile_alias(
    p: Annotated[Optional[UploadFile], File(alias="p_alias")] = None,
):
    return {"file_size": p.size if p else None}


class FormModelOptionalBytesAlias(BaseModel):
    p: Optional[bytes] = File(default=None, alias="p_alias")


@app.post("/model-optional-bytes-alias", operation_id="model_optional_bytes_alias")
async def read_model_optional_bytes_alias(
    p: Annotated[
        FormModelOptionalBytesAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": len(p.p) if p.p else None}


class FormModelOptionalUploadFileAlias(BaseModel):
    p: Optional[UploadFile] = File(default=None, alias="p_alias")


@app.post(
    "/model-optional-uploadfile-alias", operation_id="model_optional_uploadfile_alias"
)
async def read_model_optional_uploadfile_alias(
    p: Annotated[
        FormModelOptionalUploadFileAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": p.p.size if p.p else None}


@pytest.mark.xfail(
    raises=AssertionError,
    condition=PYDANTIC_V2,
    reason="Fails only with PDv2",
    strict=False,
)
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        "/model-optional-bytes-alias",
        "/optional-uploadfile-alias",
        "/model-optional-uploadfile-alias",
    ],
)
def test_optional_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": (
                IsDict(
                    {
                        "anyOf": [
                            {"type": "string", "format": "binary"},
                            {"type": "null"},
                        ],
                        "title": "P Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {"title": "P Alias", "type": "string", "format": "binary"}
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        "/model-optional-bytes-alias",
        "/optional-uploadfile-alias",
        "/model-optional-uploadfile-alias",
    ],
)
def test_optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        pytest.param(
            "/model-optional-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
        "/optional-uploadfile-alias",
        pytest.param(
            "/model-optional-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
    ],
)
def test_optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200
    assert response.json() == {"file_size": None}  # model-optional-*-alias fail here


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        pytest.param(
            "/model-optional-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
        "/optional-uploadfile-alias",
        pytest.param(
            "/model-optional-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
    ],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}  # model-optional-*-alias fail here


# =====================================================================================
# Validation alias


@app.post(
    "/optional-bytes-validation-alias", operation_id="optional_bytes_validation_alias"
)
def read_optional_bytes_validation_alias(
    p: Annotated[Optional[bytes], File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": len(p) if p else None}


@app.post(
    "/optional-uploadfile-validation-alias",
    operation_id="optional_uploadfile_validation_alias",
)
def read_optional_uploadfile_validation_alias(
    p: Annotated[Optional[UploadFile], File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": p.size if p else None}


class FormModelOptionalBytesValidationAlias(BaseModel):
    p: Optional[bytes] = File(default=None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-bytes-validation-alias",
    operation_id="model_optional_bytes_validation_alias",
)
def read_model_optional_bytes_validation_alias(
    p: Annotated[
        FormModelOptionalBytesValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": len(p.p) if p.p else None}


class FormModelOptionalUploadFileValidationAlias(BaseModel):
    p: Optional[UploadFile] = File(default=None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-uploadfile-validation-alias",
    operation_id="model_optional_uploadfile_validation_alias",
)
def read_model_optional_uploadfile_validation_alias(
    p: Annotated[
        FormModelOptionalUploadFileValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": p.p.size if p.p else None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/model-optional-uploadfile-validation-alias",
        "/optional-uploadfile-validation-alias",
        "/model-optional-bytes-validation-alias",
    ],
)
def test_optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": (
                IsDict(
                    {
                        "anyOf": [
                            {"type": "string", "format": "binary"},
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {"title": "P Val Alias", "type": "string", "format": "binary"}
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/model-optional-bytes-validation-alias",
        "/optional-uploadfile-validation-alias",
        "/model-optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-bytes-validation-alias",
        pytest.param(
            "/optional-uploadfile-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {  # /optional-*-validation-alias fail here
        "file_size": None
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/model-optional-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/optional-uploadfile-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, (
        response.text  # /model-optional-bytes-validation-alias fail here
    )
    assert response.json() == {"file_size": 5}  # /optional-*-validation-alias fail here


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-bytes-alias-and-validation-alias",
    operation_id="optional_bytes_alias_and_validation_alias",
)
def read_optional_bytes_alias_and_validation_alias(
    p: Annotated[
        Optional[bytes], File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": len(p) if p else None}


@app.post(
    "/optional-uploadfile-alias-and-validation-alias",
    operation_id="optional_uploadfile_alias_and_validation_alias",
)
def read_optional_uploadfile_alias_and_validation_alias(
    p: Annotated[
        Optional[UploadFile], File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": p.size if p else None}


class FormModelOptionalBytesAliasAndValidationAlias(BaseModel):
    p: Optional[bytes] = File(
        default=None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post(
    "/model-optional-bytes-alias-and-validation-alias",
    operation_id="model_optional_bytes_alias_and_validation_alias",
)
def read_model_optional_bytes_alias_and_validation_alias(
    p: Annotated[
        FormModelOptionalBytesAliasAndValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": len(p.p) if p.p else None}


class FormModelOptionalUploadFileAliasAndValidationAlias(BaseModel):
    p: Optional[UploadFile] = File(
        default=None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post(
    "/model-optional-uploadfile-alias-and-validation-alias",
    operation_id="model_optional_uploadfile_alias_and_validation_alias",
)
def read_model_optional_uploadfile_alias_and_validation_alias(
    p: Annotated[
        FormModelOptionalUploadFileAliasAndValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": p.p.size if p.p else None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/model-optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
        "/model-optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": (
                IsDict(
                    {
                        "anyOf": [
                            {"type": "string", "format": "binary"},
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {"title": "P Val Alias", "type": "string", "format": "binary"}
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/model-optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
        "/model-optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/model-optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
        "/model-optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-bytes-alias-and-validation-alias",
        pytest.param(
            "/optional-uploadfile-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "file_size": None  # model-optional-*-alias-and-validation-alias fail here
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/model-optional-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/optional-uploadfile-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, (
        response.text  # model-optional-bytes-alias-and-validation-alias fails here
    )
    assert response.json() == {
        "file_size": 5
    }  # /optional-*-alias-and-validation-alias fail here
