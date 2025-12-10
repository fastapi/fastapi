from typing import List, Optional

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


@app.post("/optional-list-bytes")
async def read_optional_list_bytes(p: Annotated[Optional[List[bytes]], File()] = None):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile")
async def read_optional_list_uploadfile(
    p: Annotated[Optional[List[UploadFile]], File()] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


class FormModelOptionalListBytes(BaseModel):
    p: Optional[List[bytes]] = File(default=None)


@app.post("/model-optional-list-bytes")
async def read_model_optional_list_bytes(
    p: FormModelOptionalListBytes = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [len(file) for file in p.p] if p.p else None}


class FormModelOptionalListUploadFile(BaseModel):
    p: Optional[List[UploadFile]] = File(default=None)


@app.post("/model-optional-list-uploadfile")
async def read_model_optional_list_uploadfile(
    p: FormModelOptionalListUploadFile = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [file.size for file in p.p] if p.p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes",
        "/model-optional-list-bytes",
        "/optional-list-uploadfile",
        "/model-optional-list-uploadfile",
    ],
)
def test_optional_list_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": (
                IsDict(
                    {
                        "anyOf": [
                            {
                                "type": "array",
                                "items": {"type": "string", "format": "binary"},
                            },
                            {"type": "null"},
                        ],
                        "title": "P",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {
                        "title": "P",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes",
        "/model-optional-list-bytes",
        "/optional-list-uploadfile",
        "/model-optional-list-uploadfile",
    ],
)
def test_optional_list_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-list-bytes",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 due to #14297",
                strict=False,
            ),
        ),
        pytest.param(
            "/model-optional-list-bytes",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 due to #14297",
                strict=False,
            ),
        ),
        "/optional-list-uploadfile",
        "/model-optional-list-uploadfile",
    ],
)
def test_optional_list(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200
    assert response.json() == {"file_size": [5, 5]}


# =====================================================================================
# Alias


@app.post("/optional-list-bytes-alias")
async def read_optional_list_bytes_alias(
    p: Annotated[Optional[List[bytes]], File(alias="p_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias")
async def read_optional_list_uploadfile_alias(
    p: Annotated[Optional[List[UploadFile]], File(alias="p_alias")] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


class FormModelOptionalListBytesAlias(BaseModel):
    p: Optional[List[bytes]] = File(default=None, alias="p_alias")


@app.post("/model-optional-list-bytes-alias")
async def read_model_optional_list_bytes_alias(
    p: FormModelOptionalListBytesAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [len(file) for file in p.p] if p.p else None}


class FormModelOptionalListUploadFileAlias(BaseModel):
    p: Optional[List[UploadFile]] = File(default=None, alias="p_alias")


@app.post("/model-optional-list-uploadfile-alias")
async def read_model_optional_list_uploadfile_alias(
    p: FormModelOptionalListUploadFileAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [file.size for file in p.p] if p.p else None}


@pytest.mark.xfail(
    raises=AssertionError,
    condition=PYDANTIC_V2,
    reason="Fails only with PDv2",
    strict=False,
)
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias",
        "/model-optional-list-bytes-alias",
        "/optional-list-uploadfile-alias",
        "/model-optional-list-uploadfile-alias",
    ],
)
def test_optional_list_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": (
                IsDict(
                    {
                        "anyOf": [
                            {
                                "type": "array",
                                "items": {"type": "string", "format": "binary"},
                            },
                            {"type": "null"},
                        ],
                        "title": "P Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {
                        "title": "P Alias",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    }
                )
            ),
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias",
        "/model-optional-list-bytes-alias",
        "/optional-list-uploadfile-alias",
        "/model-optional-list-uploadfile-alias",
    ],
)
def test_optional_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias",
        pytest.param(
            "/model-optional-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
        "/optional-list-uploadfile-alias",
        pytest.param(
            "/model-optional-list-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
    ],
)
def test_optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200, (
        response.text  # model-optional-list-*-alias fail here
    )
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model due to #14297",
            ),
        ),
        pytest.param(
            "/model-optional-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model due to #14297",
            ),
        ),
        "/optional-list-uploadfile-alias",
        pytest.param(
            "/model-optional-list-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
    ],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "file_size": [5, 5]  # /model-optional-list-uploadfile-alias fails here
    }


# =====================================================================================
# Validation alias


@app.post("/optional-list-bytes-validation-alias")
def read_optional_list_bytes_validation_alias(
    p: Annotated[Optional[List[bytes]], File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-validation-alias")
def read_optional_list_uploadfile_validation_alias(
    p: Annotated[
        Optional[List[UploadFile]], File(validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


class FormModelOptionalListBytesValidationAlias(BaseModel):
    p: Optional[List[bytes]] = File(default=None, validation_alias="p_val_alias")


@app.post("/model-optional-list-bytes-validation-alias")
def read_model_optional_list_bytes_validation_alias(
    p: FormModelOptionalListBytesValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [len(file) for file in p.p] if p.p else None}


class FormModelOptionalListUploadFileValidationAlias(BaseModel):
    p: Optional[List[UploadFile]] = File(default=None, validation_alias="p_val_alias")


@app.post("/model-optional-list-uploadfile-validation-alias")
def read_model_optional_list_uploadfile_validation_alias(
    p: FormModelOptionalListUploadFileValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [file.size for file in p.p] if p.p else None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-validation-alias",
        "/model-optional-list-uploadfile-validation-alias",
        "/optional-list-uploadfile-validation-alias",
        "/model-optional-list-bytes-validation-alias",
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
                            {
                                "type": "array",
                                "items": {"type": "string", "format": "binary"},
                            },
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {
                        "title": "P Val Alias",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    }
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
        "/optional-list-bytes-validation-alias",
        "/model-optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
        "/model-optional-list-uploadfile-validation-alias",
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
            "/optional-list-bytes-validation-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                reason="Fails due to #14297",
            ),
        ),
        pytest.param(
            "/model-optional-list-bytes-validation-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                reason="Fails due to #14297",
            ),
        ),
        pytest.param(
            "/optional-list-uploadfile-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-list-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {  # /optional-list-uploadfile-validation-alias fails here
        "file_size": None
    }


@pytest.mark.xfail(raises=AssertionError, strict=False)
@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-validation-alias",
        "/model-optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
        "/model-optional-list-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, (
        response.text  # /model-optional-list-*-validation-alias fail here
    )
    assert response.json() == {
        "file_size": [5, 5]  # /optional-list-*-validation-alias fail here
    }


# =====================================================================================
# Alias and validation alias


@app.post("/optional-list-bytes-alias-and-validation-alias")
def read_optional_list_bytes_alias_and_validation_alias(
    p: Annotated[
        Optional[List[bytes]], File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias-and-validation-alias")
def read_optional_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        Optional[List[UploadFile]],
        File(alias="p_alias", validation_alias="p_val_alias"),
    ] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


class FormModelOptionalListBytesAliasAndValidationAlias(BaseModel):
    p: Optional[List[bytes]] = File(
        default=None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post("/model-optional-list-bytes-alias-and-validation-alias")
def read_model_optional_list_bytes_alias_and_validation_alias(
    p: FormModelOptionalListBytesAliasAndValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [len(file) for file in p.p] if p.p else None}


class FormModelOptionalListUploadFileAliasAndValidationAlias(BaseModel):
    p: Optional[List[UploadFile]] = File(
        default=None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post("/model-optional-list-uploadfile-alias-and-validation-alias")
def read_model_optional_list_uploadfile_alias_and_validation_alias(
    p: FormModelOptionalListUploadFileAliasAndValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": [file.size for file in p.p] if p.p else None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/model-optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
        "/model-optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": (
                IsDict(
                    {
                        "anyOf": [
                            {
                                "type": "array",
                                "items": {"type": "string", "format": "binary"},
                            },
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    }
                )
                | IsDict(
                    # TODO: remove when deprecating Pydantic v1
                    {
                        "title": "P Val Alias",
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    }
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
        "/optional-list-bytes-alias-and-validation-alias",
        "/model-optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
        "/model-optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/model-optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
        "/model-optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-list-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                reason="Fails due to #14297",
            ),
        ),
        pytest.param(
            "/model-optional-list-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(
                raises=(TypeError, AssertionError),
                strict=False,
                reason="Fails due to #14297",
            ),
        ),
        pytest.param(
            "/optional-list-uploadfile-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 200, response.text
    assert (  # /optional-list-uploadfile-alias-and-validation-alias fails here
        response.json() == {"file_size": None}
    )


@pytest.mark.xfail(raises=AssertionError, strict=False)
@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/model-optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
        "/model-optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, (
        response.text  # /model-optional-list-*-alias-and-validation-alias fails here
    )
    assert response.json() == {
        "file_size": [5, 5]  # /optional-list-*-alias-and-validation-alias fail here
    }
