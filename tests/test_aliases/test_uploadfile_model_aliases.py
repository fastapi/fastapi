from typing import List, Optional

import pytest
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel

from ..utils import needs_pydanticv2

pytestmark = needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Field(alias=...)
# Current situation: doesn't work (neither validation nor schema generation)

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    file: UploadFile = File(alias="file_alias")


@app.post("/required-field-alias-model")
async def required_field_alias_model(data: RequiredFieldAliasModel = Form()):
    return {"file_size": data.file.size}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 422
    # assert 200 == 422

    # Uncomment when the assertion above passes:
    # detail = resp.json()["detail"]
    # assert detail[0]["msg"] == "Field required"
    # assert "file_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"missing","loc":["body","file"],"msg":"Field required","input":{"file_alias":{"filename":"upload","file":{"_file":{},"_max_size":1048576,"_rolled":false,"_TemporaryFileArgs":{"mode":"w+b","buffering":-1,"suffix":null,"prefix":null,"encoding":null,"newline":null,"dir":null,"errors":null}},"size":7,"headers":{"content-disposition":"form-data; name=\"file_alias\"; filename=\"upload\"","content-type":"application/octet-stream"},"_max_mem_size":1048576}}}]}

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_size": 7}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }
    # AssertionError: assert
    # {'file': {'type': 'string', 'format': 'binary', 'title': 'File'}} ==
    # {'file_alias': {'title': 'File Alias', 'type': 'string', 'format': 'binary'}}


# ------------------------------
# optional field


class OptionalFieldAliasModel(BaseModel):
    file: Optional[UploadFile] = File(None, alias="file_alias")


@app.post("/optional-field-alias-model")
async def optional_field_alias_model(data: OptionalFieldAliasModel = Form()):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": data.file.size}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}
    # AssertionError: assert {'file_size': 7} == {'file_size': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}
    # AssertionError: assert {'file_size': None} == {'file_size': 7}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {
            "anyOf": [{"type": "string", "format": "binary"}, {"type": "null"}],
            "title": "File Alias",
        },
    }
    # AssertionError: assert
    # {'file': {'anyOf': [{'type': 'string', 'format': 'binary'}, {'type': 'null'}], 'title': 'File'}} ==
    # {'file_alias': {'anyOf': [{'type': 'string', 'format': 'binary'}, {'type': 'null'}], 'title': 'File Alias'}}


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    files: List[UploadFile] = File(alias="files_alias")


@app.post("/list-field-alias-model")
async def list_field_alias_model(data: ListFieldAliasModel = Form()):
    return {"file_sizes": [file.size for file in data.files]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422

    # Uncomment when the assertion above passes:
    # detail = resp.json()["detail"]
    # assert detail[0]["msg"] == "Field required"
    # assert "files_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text

    # Uncomment when the assertion above passes:
    # assert resp.json() == {"file_sizes": [8, 8]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
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
    files: Optional[List[UploadFile]] = File(None, alias="files_alias")


@app.post("/optional-list-field-alias-model")
async def optional_list_field_alias_model(data: OptionalListFieldAliasModel = Form()):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [file.size for file in data.files]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
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
    assert resp.json() == {"file_sizes": [8, 8]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
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
# Current situation: Works (with fix #14303), but there is still an issue with `validation_alias`
# (values are extracted as extra parameters, not as declared parameters)

# ------------------------------
# required field


class RequiredFieldValidationAliasModel(BaseModel):
    file: UploadFile = File(validation_alias="file_val_alias")


@app.post(
    "/required-field-validation-alias-model",
    operation_id="required_field_validation_alias_model",
)
async def required_field_validation_alias_model(
    data: RequiredFieldValidationAliasModel = Form(),
):
    return {"file_size": data.file.size}


def test_required_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "file_val_alias" in detail[0]["loc"]


def test_required_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias-model", files={"file_val_alias": b"content"}
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


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
    file: Optional[UploadFile] = File(None, validation_alias="file_val_alias")


@app.post(
    "/optional-field-validation-alias-model",
    operation_id="optional_field_validation_alias_model",
)
async def optional_field_validation_alias_model(
    data: OptionalFieldValidationAliasModel = Form(),
):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": data.file.size}


def test_optional_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias-model", files={"file": b"content"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


def test_optional_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias-model", files={"file_val_alias": b"content"}
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


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
    files: List[UploadFile] = File(validation_alias="files_val_alias")


@app.post(
    "/list-field-validation-alias-model",
    operation_id="list_field_validation_alias_model",
)
async def list_field_validation_alias_model(
    data: ListFieldValidationAliasModel = Form(),
):
    return {"file_sizes": [file.size for file in data.files]}


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


# This currently passes (with fix #14303), but it works incorrectly internally
# (values are extracted as extra parameters, not as declared parameters)
def test_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


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
    files: Optional[List[UploadFile]] = File(None, validation_alias="files_val_alias")


@app.post(
    "/optional-list-field-validation-alias-model",
    operation_id="optional_list_field_validation_alias_model",
)
async def optional_list_field_validation_alias_model(
    data: OptionalListFieldValidationAliasModel = Form(),
):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [file.size for file in data.files]}


def test_optional_list_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


# This currently passes (with fix #14303), but it works incorrectly internally
# (values are extracted as extra parameters, not as declared parameters)
def test_optional_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


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
# Current situation: Works (with fix #14303), but there is still an issue with `validation_alias`
# (values are extracted as extra parameters, not as declared parameters)


# ------------------------------
# required field


class RequiredFieldAliasAndValidationAliasModel(BaseModel):
    file: UploadFile = File(alias="file_alias", validation_alias="file_val_alias")


@app.post(
    "/required-field-alias-and-validation-alias-model",
    operation_id="required_field_alias_and_validation_alias_model",
)
async def required_field_alias_and_validation_alias_model(
    data: RequiredFieldAliasAndValidationAliasModel = Form(),
):
    return {"file_size": data.file.size}


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


def test_required_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


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
    file: Optional[UploadFile] = File(
        None, alias="file_alias", validation_alias="file_val_alias"
    )


@app.post(
    "/optional-field-alias-and-validation-alias-model",
    operation_id="optional_field_alias_and_validation_alias_model",
)
async def optional_field_alias_and_validation_alias_model(
    data: OptionalFieldAliasAndValidationAliasModel = Form(),
):
    if data.file is None:
        return {"file_size": None}
    return {"file_size": data.file.size}


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


def test_optional_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model",
        files={"file_val_alias": b"content"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


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
    files: List[UploadFile] = File(
        alias="files_alias", validation_alias="files_val_alias"
    )


@app.post(
    "/list-field-alias-and-validation-alias-model",
    operation_id="list_field_alias_and_validation_alias_model",
)
async def list_field_alias_and_validation_alias_model(
    data: ListFieldAliasAndValidationAliasModel = Form(),
):
    return {"file_sizes": [file.size for file in data.files]}


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


# This currently passes (with fix #14303), but it works incorrectly internally
# (values are extracted as extra parameters, not as declared parameters)
def test_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


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
    files: Optional[List[UploadFile]] = File(
        None, alias="files_alias", validation_alias="files_val_alias"
    )


@app.post(
    "/optional-list-field-alias-and-validation-alias-model",
    operation_id="optional_list_field_alias_and_validation_alias_model",
)
async def optional_list_field_alias_and_validation_alias_model(
    data: OptionalListFieldAliasAndValidationAliasModel = Form(),
):
    if data.files is None:
        return {"file_sizes": None}
    return {"file_sizes": [file.size for file in data.files]}


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


# This currently passes (with fix #14303), but it works incorrectly internally
# (values are extracted as extra parameters, not as declared parameters)
def test_optional_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        files=[("files_val_alias", b"content1"), ("files_val_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


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
