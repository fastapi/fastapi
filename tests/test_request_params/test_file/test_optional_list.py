from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-list-bytes")
async def read_optional_list_bytes(p: Annotated[Optional[list[bytes]], File()] = None):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile")
async def read_optional_list_uploadfile(
    p: Annotated[Optional[list[UploadFile]], File()] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes",
        "/optional-list-uploadfile",
    ],
)
def test_optional_list_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
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
        "/optional-list-bytes",
        "/optional-list-uploadfile",
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
        "/optional-list-bytes",
        "/optional-list-uploadfile",
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
    p: Annotated[Optional[list[bytes]], File(alias="p_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias")
async def read_optional_list_uploadfile_alias(
    p: Annotated[Optional[list[UploadFile]], File(alias="p_alias")] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias",
        "/optional-list-uploadfile-alias",
    ],
)
def test_optional_list_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
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
        "/optional-list-bytes-alias",
        "/optional-list-uploadfile-alias",
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
        "/optional-list-uploadfile-alias",
    ],
)
def test_optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias",
        "/optional-list-uploadfile-alias",
    ],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": [5, 5]}


# =====================================================================================
# Validation alias


@app.post("/optional-list-bytes-validation-alias")
def read_optional_list_bytes_validation_alias(
    p: Annotated[Optional[list[bytes]], File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-validation-alias")
def read_optional_list_uploadfile_validation_alias(
    p: Annotated[
        Optional[list[UploadFile]], File(validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
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
        "/optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
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
        "/optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-validation-alias",
        "/optional-list-uploadfile-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": [5, 5]}


# =====================================================================================
# Alias and validation alias


@app.post("/optional-list-bytes-alias-and-validation-alias")
def read_optional_list_bytes_alias_and_validation_alias(
    p: Annotated[
        Optional[list[bytes]], File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias-and-validation-alias")
def read_optional_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        Optional[list[UploadFile]],
        File(alias="p_alias", validation_alias="p_val_alias"),
    ] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
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
        "/optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-bytes-alias-and-validation-alias",
        "/optional-list-uploadfile-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": [5, 5]}
