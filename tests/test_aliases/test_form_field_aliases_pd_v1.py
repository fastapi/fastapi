from typing import List, Optional

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient

from ..utils import needs_pydanticv1

pytestmark = needs_pydanticv1

app = FastAPI()

# =====================================================================================
# Form(alias=...)
# Current situation: Works
# Schema generation for optional field and optional list fails due to issue likely not related to aliases


# ------------------------------
# required field


@app.post("/required-field-alias", operation_id="required_field_alias")
async def required_field_alias(param: str = Form(alias="param_alias")):
    return {"param": param}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_required_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {"title": "Param Alias", "type": "string"}
    }


# ------------------------------
# optional field


@app.post("/optional-field-alias", operation_id="optional_field_alias")
async def optional_field_alias(
    param: Optional[str] = Form(None, alias="param_alias"),
):
    return {"param": param}


def test_optional_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", data={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Alias",
        }
    }
    # Fails with:
    # AssertionError: assert
    # {'param_alias': {'type': 'string', 'title': 'Param Alias'}} ==
    # {'param_alias': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'title': 'Param Alias'}}


# ------------------------------
# list field


@app.post("/list-field-alias", operation_id="list_field_alias")
async def list_field_alias(param: List[str] = Form(alias="param_alias")):
    return {"param": param}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "field required"
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "title": "Param Alias",
            "type": "array",
            "items": {"type": "string"},
        }
    }


# ------------------------------
# optional list field


@app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
async def optional_list_field_alias(
    param: Optional[List[str]] = Form(None, alias="param_alias"),
):
    return {"param": param}


def test_optional_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-list-field-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_list_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Alias",
        },
    }
    # Fails with:
    # AssertionError: assert
    # {'param_alias': {'items': {'type': 'string'}, 'type': 'array', 'title': 'Param Alias'}} ==
    # {'param_alias': {'anyOf': [{'items': {'type': 'string'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Param Alias'}}
