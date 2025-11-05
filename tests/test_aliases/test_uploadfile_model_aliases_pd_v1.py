from typing import List, Optional

from fastapi import FastAPI, File, UploadFile
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from ..utils import needs_pydanticv1

pytestmark = needs_pydanticv1

app = FastAPI()

# =====================================================================================
# Field(alias=...)
# Current situation: Works

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    file: UploadFile = Field(alias="file_alias")


@app.post("/required-field-alias-model")
async def required_field_alias_model(data: RequiredFieldAliasModel = File(...)):
    return {"file_size": data.file.size}


def test_required_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "file_alias" in detail[0]["loc"]


def test_required_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


def test_required_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {"title": "File Alias", "type": "string", "format": "binary"}
    }


# ------------------------------
# optional field

if not PYDANTIC_V2:

    class OptionalFieldAliasModel(BaseModel):
        file: Optional[UploadFile] = Field(None, alias="file_alias", nullable=True)

    @app.post("/optional-field-alias-model")
    async def optional_field_alias_model(data: OptionalFieldAliasModel = File(...)):
        if data.file is None:
            return {"file_size": None}
        return {"file_size": data.file.size}


def test_optional_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file": b"content"})
    assert resp.status_code == 200
    assert resp.json() == {"file_size": None}


def test_optional_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", files={"file_alias": b"content"})
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_size": 7}


def test_optional_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "file_alias": {
            "format": "binary",
            "nullable": True,
            "title": "File Alias",
            "type": "string",
        },
    }


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    files: List[UploadFile] = Field(alias="files_alias")


@app.post("/list-field-alias-model")
async def list_field_alias_model(data: ListFieldAliasModel = File(...)):
    return {"file_sizes": [file.size for file in data.files]}


def test_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "files_alias" in detail[0]["loc"]


def test_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


def test_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "files_alias": {
            "items": {"format": "binary", "type": "string"},
            "title": "Files Alias",
            "type": "array",
        }
    }


# ------------------------------
# optional list field

if not PYDANTIC_V2:

    class OptionalListFieldAliasModel(BaseModel):
        files: Optional[List[UploadFile]] = Field(None, alias="files_alias", nullable=True)

    @app.post("/optional-list-field-alias-model")
    async def optional_list_field_alias_model(
        data: OptionalListFieldAliasModel = File(),
    ):
        if data.files is None:
            return {"file_sizes": None}
        return {"file_sizes": [file.size for file in data.files]}


def test_optional_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    assert resp.status_code == 200
    assert resp.json() == {"file_sizes": None}


def test_optional_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model",
        files=[("files_alias", b"content1"), ("files_alias", b"content2")],
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"file_sizes": [8, 8]}


def test_optional_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert body_schema["properties"] == {
        "files_alias": {
            "nullable": True,
            "items": {"format": "binary", "type": "string"},
            "title": "Files Alias",
            "type": "array",
        }
    }
