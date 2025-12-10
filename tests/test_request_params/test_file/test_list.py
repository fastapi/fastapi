from typing import List

import pytest
from dirty_equals import IsDict, IsOneOf, IsPartialDict
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


@app.post("/list-bytes", operation_id="list_bytes")
async def read_list_bytes(p: Annotated[List[bytes], File()]):
    return {"file_size": [len(file) for file in p]}


@app.post("/list-uploadfile", operation_id="list_uploadfile")
async def read_list_uploadfile(p: Annotated[List[UploadFile], File()]):
    return {"file_size": [file.size for file in p]}


class FormModelListBytes(BaseModel):
    p: List[bytes] = File()


@app.post("/model-list-bytes", operation_id="model_list_bytes")
async def read_model_list_bytes(
    p: Annotated[
        FormModelListBytes,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [len(file) for file in p.p]}


class FormModelListUploadFile(BaseModel):
    p: List[UploadFile] = File()


@app.post("/model-list-uploadfile", operation_id="model_list_uploadfile")
async def read_model_list_uploadfile(
    p: Annotated[
        FormModelListUploadFile,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [file.size for file in p.p]}


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes",
        "/model-list-bytes",
        "/list-uploadfile",
        "/model-list-uploadfile",
    ],
)
def test_list_schema(path: str):
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
                    },
                )
                | IsDict(
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "title": "P",
                    },
                )
            )
        },
        "required": ["p"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes",
        "/model-list-bytes",
        "/list-uploadfile",
        "/model-list-uploadfile",
    ],
)
def test_list_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "p"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes",
        "/model-list-bytes",
        "/list-uploadfile",
        "/model-list-uploadfile",
    ],
)
def test_list(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200
    assert response.json() == {"file_size": [5, 5]}


# =====================================================================================
# Alias


@app.post("/list-bytes-alias", operation_id="list_bytes_alias")
async def read_list_bytes_alias(p: Annotated[List[bytes], File(alias="p_alias")]):
    return {"file_size": [len(file) for file in p]}


@app.post("/list-uploadfile-alias", operation_id="list_uploadfile_alias")
async def read_list_uploadfile_alias(
    p: Annotated[List[UploadFile], File(alias="p_alias")],
):
    return {"file_size": [file.size for file in p]}


class FormModelListBytesAlias(BaseModel):
    p: List[bytes] = File(alias="p_alias")


@app.post("/model-list-bytes-alias", operation_id="model_list_bytes_alias")
async def read_model_list_bytes_alias(
    p: Annotated[
        FormModelListBytesAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [len(file) for file in p.p]}


class FormModelListUploadFileAlias(BaseModel):
    p: List[UploadFile] = File(alias="p_alias")


@app.post("/model-list-uploadfile-alias", operation_id="model_list_uploadfile_alias")
async def read_model_list_uploadfile_alias(
    p: Annotated[
        FormModelListUploadFileAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [file.size for file in p.p]}


@pytest.mark.xfail(
    raises=AssertionError,
    condition=PYDANTIC_V2,
    reason="Fails only with PDv2",
    strict=False,
)
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias",
        "/model-list-bytes-alias",
        "/list-uploadfile-alias",
        "/model-list-uploadfile-alias",
    ],
)
def test_list_alias_schema(path: str):
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
                    },
                )
                | IsDict(
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "title": "P Alias",
                    },
                )
            )
        },
        "required": ["p_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias",
        pytest.param(
            "/model-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
        "/list-uploadfile-alias",
        pytest.param(
            "/model-list-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
    ],
)
def test_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],  # model-list-*-alias fail here
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias",
        pytest.param(
            "/model-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
        "/list-uploadfile-alias",
        pytest.param(
            "/model-list-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
                strict=False,
            ),
        ),
    ],
)
def test_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 422  # model-list-uploadfile-alias fail here
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(  # model-list-bytes-alias fail here
                        None,
                        {"p": [IsPartialDict({"size": 5}), IsPartialDict({"size": 5})]},
                    ),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias",
        pytest.param(
            "/model-list-bytes-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
        "/list-uploadfile-alias",
        pytest.param(
            "/model-list-uploadfile-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                strict=False,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 model",
            ),
        ),
    ],
)
def test_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 200, (  # model-list-*-alias fail here
        response.text
    )
    assert response.json() == {"file_size": [5, 5]}


# =====================================================================================
# Validation alias


@app.post("/list-bytes-validation-alias", operation_id="list_bytes_validation_alias")
def read_list_bytes_validation_alias(
    p: Annotated[List[bytes], File(validation_alias="p_val_alias")],
):
    return {"file_size": [len(file) for file in p]}


@app.post(
    "/list-uploadfile-validation-alias",
    operation_id="list_uploadfile_validation_alias",
)
def read_list_uploadfile_validation_alias(
    p: Annotated[List[UploadFile], File(validation_alias="p_val_alias")],
):
    return {"file_size": [file.size for file in p]}


class FormModelRequiredBytesValidationAlias(BaseModel):
    p: List[bytes] = File(validation_alias="p_val_alias")


@app.post(
    "/model-list-bytes-validation-alias",
    operation_id="model_list_bytes_validation_alias",
)
def read_model_list_bytes_validation_alias(
    p: Annotated[
        FormModelRequiredBytesValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [len(file) for file in p.p]}  # pragma: no cover


class FormModelRequiredUploadFileValidationAlias(BaseModel):
    p: List[UploadFile] = File(validation_alias="p_val_alias")


@app.post(
    "/model-list-uploadfile-validation-alias",
    operation_id="model_list_uploadfile_validation_alias",
)
def read_model_list_uploadfile_validation_alias(
    p: Annotated[
        FormModelRequiredUploadFileValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [file.size for file in p.p]}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-validation-alias",
        "/model-list-uploadfile-validation-alias",
        "/list-uploadfile-validation-alias",
        "/model-list-bytes-validation-alias",
    ],
)
def test_list_validation_alias_schema(path: str):
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
                    },
                )
                | IsDict(
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "title": "P Val Alias",
                    },
                )
            )
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/list-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-bytes-validation-alias",
        pytest.param(
            "/list-uploadfile-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-uploadfile-validation-alias",
    ],
)
def test_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [  # /list-*-validation-alias fail here
                    "body",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/list-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/model-list-bytes-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/list-uploadfile-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-uploadfile-validation-alias",
    ],
)
def test_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 422, (  # /list-*-validation-alias fail here
        response.text
    )

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(  # /model-list-bytes-validation-alias fails here
                    None,
                    {"p": [IsPartialDict({"size": 5}), IsPartialDict({"size": 5})]},
                ),
            }
        ]
    }


@pytest.mark.xfail(raises=AssertionError, strict=False)
@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-validation-alias",
        "/model-list-bytes-validation-alias",
        "/list-uploadfile-validation-alias",
        "/model-list-uploadfile-validation-alias",
    ],
)
def test_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, response.text  # all 4 fail here
    assert response.json() == {"file_size": [5, 5]}  # pragma: no cover


# =====================================================================================
# Alias and validation alias


@app.post(
    "/list-bytes-alias-and-validation-alias",
    operation_id="list_bytes_alias_and_validation_alias",
)
def read_list_bytes_alias_and_validation_alias(
    p: Annotated[List[bytes], File(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"file_size": [len(file) for file in p]}


@app.post(
    "/list-uploadfile-alias-and-validation-alias",
    operation_id="list_uploadfile_alias_and_validation_alias",
)
def read_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        List[UploadFile], File(alias="p_alias", validation_alias="p_val_alias")
    ],
):
    return {"file_size": [file.size for file in p]}


class FormModelRequiredBytesAliasAndValidationAlias(BaseModel):
    p: List[bytes] = File(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-list-bytes-alias-and-validation-alias",
    operation_id="model_list_bytes_alias_and_validation_alias",
)
def read_model_list_bytes_alias_and_validation_alias(
    p: Annotated[
        FormModelRequiredBytesAliasAndValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [len(file) for file in p.p]}  # pragma: no cover


class FormModelRequiredUploadFileAliasAndValidationAlias(BaseModel):
    p: List[UploadFile] = File(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-list-uploadfile-alias-and-validation-alias",
    operation_id="model_list_uploadfile_alias_and_validation_alias",
)
def read_model_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        FormModelRequiredUploadFileAliasAndValidationAlias,
        Form(
            media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
        ),
    ],
):
    return {"file_size": [file.size for file in p.p]}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias-and-validation-alias",
        "/model-list-bytes-alias-and-validation-alias",
        "/list-uploadfile-alias-and-validation-alias",
        "/model-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_list_alias_and_validation_alias_schema(path: str):
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
                    },
                )
                | IsDict(
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                        "title": "P Val Alias",
                    },
                )
            )
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/list-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-bytes-alias-and-validation-alias",
        pytest.param(
            "/list-uploadfile-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "p_val_alias",  # /list-*-alias-and-validation-alias fail here
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.xfail(raises=AssertionError, strict=False)
@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias-and-validation-alias",
        "/model-list-bytes-alias-and-validation-alias",
        "/list-uploadfile-alias-and-validation-alias",
        "/model-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", "hello"), ("p", "world")])
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "p_val_alias",  # /list-*-alias-and-validation-alias fail here
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-list-*-alias-and-validation-alias fail here
                    {"p": [IsPartialDict({"size": 5}), IsPartialDict({"size": 5})]},
                ),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/list-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/model-list-bytes-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        pytest.param(
            "/list-uploadfile-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 422, (
        response.text  # /list-*-alias-and-validation-alias fails here
    )

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-list-bytes-alias-and-validation-alias fails here
                    {
                        "p_alias": [
                            IsPartialDict({"size": 5}),
                            IsPartialDict({"size": 5}),
                        ]
                    },
                ),
            }
        ]
    }


@pytest.mark.xfail(raises=AssertionError, strict=False)
@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/list-bytes-alias-and-validation-alias",
        "/model-list-bytes-alias-and-validation-alias",
        "/list-uploadfile-alias-and-validation-alias",
        "/model-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, (  # all 4 fail here
        response.text
    )
    assert response.json() == {"file_size": [5, 5]}  # pragma: no cover
