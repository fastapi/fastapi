from typing import List, Optional

from fastapi import FastAPI, Form
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from ..utils import needs_pydanticv1

pytestmark = needs_pydanticv1

app = FastAPI()

# =====================================================================================
# Field(alias=...)
# Current situation: works

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    param: str = Field(alias="param_alias")


@app.post("/required-field-alias-model")
async def required_field_alias_model(data: RequiredFieldAliasModel = Form(...)):
    return {"param": data.param}


def test_required_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {"title": "Param Alias", "type": "string"}
    }


# ------------------------------
# optional field

if not PYDANTIC_V2:

    class OptionalFieldAliasModel(BaseModel):
        param: Optional[str] = Field(None, alias="param_alias", nullable=True)

    @app.post("/optional-field-alias-model")
    async def optional_field_alias_model(data: OptionalFieldAliasModel = Form(...)):
        return {"param": data.param}


def test_optional_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", data={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "type": "string",
            "nullable": True,
            "title": "Param Alias",
        },
    }


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    param: List[str] = Field(alias="param_alias")


@app.post("/list-field-alias-model")
async def list_field_alias_model(data: ListFieldAliasModel = Form(...)):
    return {"param": data.param}


def test_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias-model", data={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias-model", data={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "title": "Param Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field

if not PYDANTIC_V2:

    class OptionalListFieldAliasModel(BaseModel):
        param: Optional[List[str]] = Field(None, alias="param_alias", nullable=True)

    @app.post("/optional-list-field-alias-model")
    async def optional_list_field_alias_model(
        data: OptionalListFieldAliasModel = Form(...),
    ):
        return {"param": data.param}


def test_optional_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "type": "array",
            "nullable": True,
            "title": "Param Alias",
        }
    }
