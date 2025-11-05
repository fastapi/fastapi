from typing import List, Optional

import pytest
from fastapi import FastAPI, File
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from ..utils import needs_pydanticv2

pytestmark = needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Field(alias=...)
# Current situation: doesn't work due to validation error

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    file: bytes = Field(alias="file_alias")


@app.post("/required-field-alias-model")
async def required_field_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: RequiredFieldAliasModel = File(...),
):
    return {"file_size": len(data.file)}


def test_required_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_required_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }


# ------------------------------
# optional field


class OptionalFieldAliasModel(BaseModel):
    file: Optional[bytes] = Field(None, alias="file_alias")


@app.post("/optional-field-alias-model")
async def optional_field_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalFieldAliasModel = File(...),
):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": len(data.file)}


def test_optional_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_optional_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Alias",
        },
    }


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    files: List[bytes] = Field(alias="files_alias")


@app.post("/list-field-alias-model")
async def list_field_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: ListFieldAliasModel = File(...),
):
    return {"file_sizes": [len(file) for file in data.files]}


def test_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","files_alias",0],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}},{"type":"bytes_type","loc":["body","files_alias",1],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "files_alias": {
            "items": {"type": "string", "format": "binary"},
            "title": "Files Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasModel(BaseModel):
    files: Optional[List[bytes]] = Field(None, alias="files_alias")


@app.post("/optional-list-field-alias-model")
async def optional_list_field_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalListFieldAliasModel = File(),
):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [len(file) for file in data.files]}


def test_optional_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","files_alias",0],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}},{"type":"bytes_type","loc":["body","files_alias",1],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_optional_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert body_schema["properties"] == {
        "files_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Alias",
        }
    }


# =====================================================================================
# Field(validation_alias=...)
# Current situation: doesn't work due to validation error


# ------------------------------
# required field


class RequiredFieldValidationAliasModel(BaseModel):
    file: bytes = Field(validation_alias="file_val_alias")


@app.post(
    "/required-field-validation-alias-model",
    operation_id="required_field_validation_alias_model",
)
async def required_field_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: RequiredFieldValidationAliasModel = File(...),
):
    return {"file_size": len(data.file)}


def test_required_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias-model", files={"file_val_alias": b"content"}
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_val_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_required_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "title": "File Val Alias",
            "type": "string",
            "format": "binary",
        }
    }


# ------------------------------
# optional field


class OptionalFieldValidationAliasModel(BaseModel):
    file: Optional[bytes] = Field(None, validation_alias="file_val_alias")


@app.post(
    "/optional-field-validation-alias-model",
    operation_id="optional_field_validation_alias_model",
)
async def optional_field_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalFieldValidationAliasModel = File(...),
):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": len(data.file)}


def test_optional_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias-model", files={"file_val_alias": b"content"}
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_val_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_optional_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Val Alias",
        },
    }


# ------------------------------
# list field


class ListFieldValidationAliasModel(BaseModel):
    files: List[bytes] = Field(validation_alias="files_val_alias")


@app.post(
    "/list-field-validation-alias-model",
    operation_id="list_field_validation_alias_model",
)
async def list_field_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: ListFieldValidationAliasModel = File(...),
):
    return {"file_sizes": [len(file) for file in data.files]}


def test_list_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","files_val_alias"],"msg":"Input should be a valid list","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "items": {"type": "string", "format": "binary"},
            "title": "Files Val Alias",
            "type": "array",
        }
    }


# ------------------------------
# optional list field


class OptionalListFieldValidationAliasModel(BaseModel):
    files: Optional[List[bytes]] = Field(None, validation_alias="files_val_alias")


@app.post(
    "/optional-list-field-validation-alias-model",
    operation_id="optional_list_field_validation_alias_model",
)
async def optional_list_field_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalListFieldValidationAliasModel = File(...),
):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [len(file) for file in data.files]}


def test_optional_list_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","files_val_alias"],"msg":"Input should be a valid list","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_optional_list_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalListFieldValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Val Alias",
        },
    }


# =====================================================================================
# Field(alias=..., validation_alias=...)
# Current situation: doesn't work due to validation error

# ------------------------------
# required field


class RequiredFieldAliasAndValidationAliasModel(BaseModel):
    file: bytes = Field(alias="file_alias", validation_alias="file_val_alias")


@app.post(
    "/required-field-alias-and-validation-alias-model",
    operation_id="required_field_alias_and_validation_alias_model",
)
async def required_field_alias_and_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: RequiredFieldAliasAndValidationAliasModel = File(...),
):
    return {"file_size": len(data.file)}


def test_required_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


def test_required_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model",
        files={"file_alias": b"content"},
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_val_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_required_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "RequiredFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "title": "File Val Alias",
            "type": "string",
            "format": "binary",
        }
    }


# ------------------------------
# optional field


class OptionalFieldAliasAndValidationAliasModel(BaseModel):
    file: Optional[bytes] = Field(
        None, alias="file_alias", validation_alias="file_val_alias"
    )


@app.post(
    "/optional-field-alias-and-validation-alias-model",
    operation_id="optional_field_alias_and_validation_alias_model",
)
async def optional_field_alias_and_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalFieldAliasAndValidationAliasModel = File(...),
):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": len(data.file)}


def test_optional_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


def test_optional_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model",
        files={"file_alias": b"content"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"bytes_type","loc":["body","file_val_alias"],"msg":"Input should be a valid bytes","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


def test_optional_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "file_val_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Val Alias",
        }
    }


# ------------------------------
# list field


class ListFieldAliasAndValidationAliasModel(BaseModel):
    files: List[bytes] = Field(alias="files_alias", validation_alias="files_val_alias")


@app.post(
    "/list-field-alias-and-validation-alias-model",
    operation_id="list_field_alias_and_validation_alias_model",
)
async def list_field_alias_and_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: ListFieldAliasAndValidationAliasModel = File(...),
):
    return {"file_sizes": [len(file) for file in data.files]}


def test_list_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]


def test_list_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "files_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","files_val_alias"],"msg":"Input should be a valid list","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "ListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "items": {"type": "string", "format": "binary"},
            "title": "Files Val Alias",
            "type": "array",
        }
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasAndValidationAliasModel(BaseModel):
    files: Optional[List[bytes]] = Field(
        None, alias="files_alias", validation_alias="files_val_alias"
    )


@app.post(
    "/optional-list-field-alias-and-validation-alias-model",
    operation_id="optional_list_field_alias_and_validation_alias_model",
)
async def optional_list_field_alias_and_validation_alias_model(  # pragma: no cover (remove `no cover` when bug fixed)
    data: OptionalListFieldAliasAndValidationAliasModel = File(...),
):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [len(file) for file in data.files]}


def test_optional_list_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": None}


def test_optional_list_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    # Fails with:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","files_val_alias"],"msg":"Input should be a valid list","input":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":8,"headers":{"content-disposition":"form-data; name=\"files_val_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


def test_optional_list_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "files_val_alias": {
            "anyOf": [
                {"items": {"type": "string", "format": "binary"}, "type": "array"},
                {"type": "null"},
            ],
            "title": "Files Val Alias",
        }
    }
