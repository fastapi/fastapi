import pytest
from dirty_equals import IsDict, IsOneOf, IsPartialDict
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel

from tests.utils import needs_pydanticv2

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-bytes", operation_id="required_bytes")
async def read_required_bytes(p: bytes = File(...)):
    return {"file_size": len(p)}


@app.post("/required-uploadfile", operation_id="required_uploadfile")
async def read_required_uploadfile(p: UploadFile = File(...)):
    return {"file_size": p.size}


class FormModelRequiredBytes(BaseModel):
    p: bytes = File(...)


@app.post("/model-required-bytes", operation_id="model_required_bytes")
async def read_model_required_bytes(
    p: FormModelRequiredBytes = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": len(p.p)}


class FormModelRequiredUploadFile(BaseModel):
    p: UploadFile = File(...)


@app.post("/model-required-uploadfile", operation_id="model_required_uploadfile")
async def read_model_required_uploadfile(
    p: FormModelRequiredUploadFile = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": p.p.size}


@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes",
        "/model-required-bytes",
        "/required-uploadfile",
        "/model-required-uploadfile",
    ],
)
def test_required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {"title": "P", "type": "string", "format": "binary"},
        },
        "required": ["p"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes",
        "/model-required-bytes",
        "/required-uploadfile",
        "/model-required-uploadfile",
    ],
)
def test_required_missing(path: str):
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
        "/required-bytes",
        "/model-required-bytes",
        "/required-uploadfile",
        "/model-required-uploadfile",
    ],
)
def test_required(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200
    assert response.json() == {"file_size": 5}


# =====================================================================================
# Alias


@app.post("/required-bytes-alias", operation_id="required_bytes_alias")
async def read_required_bytes_alias(p: bytes = File(..., alias="p_alias")):
    return {"file_size": len(p)}


@app.post("/required-uploadfile-alias", operation_id="required_uploadfile_alias")
async def read_required_uploadfile_alias(p: UploadFile = File(..., alias="p_alias")):
    return {"file_size": p.size}


class FormModelRequiredBytesAlias(BaseModel):
    p: bytes = File(..., alias="p_alias")


@app.post("/model-required-bytes-alias", operation_id="model_required_bytes_alias")
async def read_model_required_bytes_alias(
    p: FormModelRequiredBytesAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": len(p.p)}


class FormModelRequiredUploadFileAlias(BaseModel):
    p: UploadFile = File(..., alias="p_alias")


@app.post(
    "/model-required-uploadfile-alias", operation_id="model_required_uploadfile_alias"
)
async def read_model_required_uploadfile_alias(
    p: FormModelRequiredUploadFileAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": p.p.size}


@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias",
        "/model-required-bytes-alias",
        "/required-uploadfile-alias",
        "/model-required-uploadfile-alias",
    ],
)
def test_required_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {"title": "P Alias", "type": "string", "format": "binary"},
        },
        "required": ["p_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias",
        "/model-required-bytes-alias",
        "/required-uploadfile-alias",
        "/model-required-uploadfile-alias",
    ],
)
def test_required_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
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
        "/required-bytes-alias",
        "/model-required-bytes-alias",
        "/required-uploadfile-alias",
        "/model-required-uploadfile-alias",
    ],
)
def test_required_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(
                        None,
                        {"p": IsPartialDict({"size": 5})},
                        {"p": b"hello"},
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
        "/required-bytes-alias",
        "/model-required-bytes-alias",
        "/required-uploadfile-alias",
        "/model-required-uploadfile-alias",
    ],
)
def test_required_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}


# =====================================================================================
# Validation alias


@app.post(
    "/required-bytes-validation-alias", operation_id="required_bytes_validation_alias"
)
def read_required_bytes_validation_alias(
    p: bytes = File(..., validation_alias="p_val_alias"),
):
    return {"file_size": len(p)}


@app.post(
    "/required-uploadfile-validation-alias",
    operation_id="required_uploadfile_validation_alias",
)
def read_required_uploadfile_validation_alias(
    p: UploadFile = File(..., validation_alias="p_val_alias"),
):
    return {"file_size": p.size}


class FormModelRequiredBytesValidationAlias(BaseModel):
    p: bytes = File(..., validation_alias="p_val_alias")


@app.post(
    "/model-required-bytes-validation-alias",
    operation_id="model_required_bytes_validation_alias",
)
def read_model_required_bytes_validation_alias(
    p: FormModelRequiredBytesValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": len(p.p)}


class FormModelRequiredUploadFileValidationAlias(BaseModel):
    p: UploadFile = File(..., validation_alias="p_val_alias")


@app.post(
    "/model-required-uploadfile-validation-alias",
    operation_id="model_required_uploadfile_validation_alias",
)
def read_model_required_uploadfile_validation_alias(
    p: FormModelRequiredUploadFileValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": p.p.size}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-validation-alias",
        "/model-required-uploadfile-validation-alias",
        "/required-uploadfile-validation-alias",
        "/model-required-bytes-validation-alias",
    ],
)
def test_required_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "title": "P Val Alias",
                "type": "string",
                "format": "binary",
            },
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-validation-alias",
        "/model-required-bytes-validation-alias",
        "/required-uploadfile-validation-alias",
        "/model-required-uploadfile-validation-alias",
    ],
)
def test_required_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
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
        "/required-bytes-validation-alias",
        "/model-required-bytes-validation-alias",
        "/required-uploadfile-validation-alias",
        "/model-required-uploadfile-validation-alias",
    ],
)
def test_required_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": IsPartialDict({"size": 5})}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-validation-alias",
        "/model-required-bytes-validation-alias",
        "/required-uploadfile-validation-alias",
        "/model-required-uploadfile-validation-alias",
    ],
)
def test_required_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-bytes-alias-and-validation-alias",
    operation_id="required_bytes_alias_and_validation_alias",
)
def read_required_bytes_alias_and_validation_alias(
    p: bytes = File(..., alias="p_alias", validation_alias="p_val_alias"),
):
    return {"file_size": len(p)}


@app.post(
    "/required-uploadfile-alias-and-validation-alias",
    operation_id="required_uploadfile_alias_and_validation_alias",
)
def read_required_uploadfile_alias_and_validation_alias(
    p: UploadFile = File(..., alias="p_alias", validation_alias="p_val_alias"),
):
    return {"file_size": p.size}


class FormModelRequiredBytesAliasAndValidationAlias(BaseModel):
    p: bytes = File(..., alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-bytes-alias-and-validation-alias",
    operation_id="model_required_bytes_alias_and_validation_alias",
)
def read_model_required_bytes_alias_and_validation_alias(
    p: FormModelRequiredBytesAliasAndValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": len(p.p)}


class FormModelRequiredUploadFileAliasAndValidationAlias(BaseModel):
    p: UploadFile = File(..., alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-uploadfile-alias-and-validation-alias",
    operation_id="model_required_uploadfile_alias_and_validation_alias",
)
def read_model_required_uploadfile_alias_and_validation_alias(
    p: FormModelRequiredUploadFileAliasAndValidationAlias = Form(
        media_type="multipart/form-data"  # Remove media_type when https://github.com/fastapi/fastapi/pull/14343 is fixed
    ),
):
    return {"file_size": p.p.size}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias-and-validation-alias",
        "/model-required-bytes-alias-and-validation-alias",
        "/required-uploadfile-alias-and-validation-alias",
        "/model-required-uploadfile-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "title": "P Val Alias",
                "type": "string",
                "format": "binary",
            },
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias-and-validation-alias",
        "/model-required-bytes-alias-and-validation-alias",
        "/required-uploadfile-alias-and-validation-alias",
        "/model-required-uploadfile-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias-and-validation-alias",
        "/model-required-bytes-alias-and-validation-alias",
        "/required-uploadfile-alias-and-validation-alias",
        "/model-required-uploadfile-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": IsPartialDict({"size": 5})}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias-and-validation-alias",
        "/model-required-bytes-alias-and-validation-alias",
        "/required-uploadfile-alias-and-validation-alias",
        "/model-required-uploadfile-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p_alias": IsPartialDict({"size": 5})}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-bytes-alias-and-validation-alias",
        "/model-required-bytes-alias-and-validation-alias",
        "/required-uploadfile-alias-and-validation-alias",
        "/model-required-uploadfile-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}
