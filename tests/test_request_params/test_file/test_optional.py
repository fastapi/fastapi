from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient

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


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes",
        "/optional-uploadfile",
    ],
)
def test_optional_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {
                "anyOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "null"},
                ],
                "title": "P",
            }
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes",
        "/optional-uploadfile",
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
        "/optional-uploadfile",
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


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        "/optional-uploadfile-alias",
    ],
)
def test_optional_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {
                "anyOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "null"},
                ],
                "title": "P Alias",
            }
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        "/optional-uploadfile-alias",
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
        "/optional-uploadfile-alias",
    ],
)
def test_optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias",
        "/optional-uploadfile-alias",
    ],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}


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


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            }
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-validation-alias",
        "/optional-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}


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


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {"type": "string", "format": "binary"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            }
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-bytes-alias-and-validation-alias",
        "/optional-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": 5}
