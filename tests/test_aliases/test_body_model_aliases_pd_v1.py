from typing import List, Optional

from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from ..utils import needs_pydanticv1

pytestmark = needs_pydanticv1


app = FastAPI()

# =====================================================================================
# Pydantic model with Field(alias=...)

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    param: str = Field(alias="param_alias")


@app.post("/required-field-alias", operation_id="required_field_alias")
async def required_field_alias(body: RequiredFieldAliasModel):
    return {"param": body.param}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", json={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", json={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {"type": "string", "title": "Param Alias"}
    }


# ------------------------------
# optional field

if not PYDANTIC_V2:

    class OptionalFieldAliasModel(BaseModel):
        param: Optional[str] = Field(None, alias="param_alias", nullable=True)

    @app.post("/optional-field-alias", operation_id="optional_field_alias")
    async def optional_field_alias(body: OptionalFieldAliasModel):
        return {"param": body.param}


def test_optional_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", json={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", json={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {"nullable": True, "title": "Param Alias", "type": "string"}
    }


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    param: List[str] = Field(alias="param_alias")


@app.post("/list-field-alias", operation_id="list_field_alias")
async def list_field_alias(body: ListFieldAliasModel):
    return {"param": body.param}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias", json={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias", json={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "type": "array",
            "title": "Param Alias",
        }
    }


# ------------------------------
# optional list field

if not PYDANTIC_V2:

    class OptionalListFieldAliasModel(BaseModel):
        param: Optional[List[str]] = Field(None, alias="param_alias", nullable=True)

    @app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
    async def optional_list_field_alias(body: OptionalListFieldAliasModel):
        return {"param": body.param}


def test_optional_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-list-field-alias", json={"param": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias", json={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "nullable": True,
            "title": "Param Alias",
            "type": "array",
        }
    }
