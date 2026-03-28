"""
Tests for correct model_fields_set and default handling in Form endpoints.

Covers:
- Absent fields (never sent by the client)
- Blank strings (HTML forms send "" for empty text inputs)
- Required fields still return 422 when absent
- Behaviour matches JSON body endpoints
- Aliases work correctly

Related: https://github.com/fastapi/fastapi/issues/13399
"""

from typing import Annotated

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class BoolModel(BaseModel):
    """Checkbox-style: bool with non-falsy default."""

    checkbox: bool = True


class StringModel(BaseModel):
    """Text input with a non-empty default."""

    text: str = "default"
    alias_field: str = Field(alias="with", default="nothing")


class MixedModel(BaseModel):
    field_bool: bool = True
    field_str: str = "hello"
    field_nullable: str | None = None


class RequiredModel(BaseModel):
    required_field: str
    optional_field: str = "default"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.post("/bool")
async def bool_endpoint(model: Annotated[BoolModel, Form()]):
    return {"fields_set": sorted(model.model_fields_set), "values": model.model_dump()}


@app.post("/string")
async def string_endpoint(model: Annotated[StringModel, Form()]):
    return {"fields_set": sorted(model.model_fields_set), "values": model.model_dump(by_alias=True)}


@app.post("/mixed")
async def mixed_endpoint(model: Annotated[MixedModel, Form()]):
    return {"fields_set": sorted(model.model_fields_set), "values": model.model_dump()}


@app.post("/required")
async def required_endpoint(model: Annotated[RequiredModel, Form()]):
    return {"fields_set": sorted(model.model_fields_set), "values": model.model_dump()}


# JSON body counterpart for parity checks
@app.post("/mixed-json")
async def mixed_json_endpoint(model: MixedModel):
    return {"fields_set": sorted(model.model_fields_set), "values": model.model_dump()}


client = TestClient(app)


# ---------------------------------------------------------------------------
# Absent fields — never sent by the client
# ---------------------------------------------------------------------------


def test_absent_bool_field_not_in_fields_set():
    """Unchecked checkbox (absent from form) must NOT appear in model_fields_set."""
    resp = client.post("/bool", data={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == []


def test_absent_bool_field_default_still_applied():
    """Default value is still present in the response even when field not submitted."""
    resp = client.post("/bool", data={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["values"]["checkbox"] is True


def test_submitted_bool_field_in_fields_set():
    """Submitted checkbox appears in model_fields_set."""
    resp = client.post("/bool", data={"checkbox": "false"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == ["checkbox"]
    assert resp.json()["values"]["checkbox"] is False


# ---------------------------------------------------------------------------
# Blank string fields — HTML forms send "" for empty text inputs
# ---------------------------------------------------------------------------


def test_blank_string_treated_as_unset():
    """Empty text input ('') must NOT appear in model_fields_set; default applied."""
    resp = client.post("/string", data={"text": "", "with": ""})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["fields_set"] == []
    assert body["values"]["text"] == "default"
    assert body["values"]["with"] == "nothing"


def test_non_empty_string_in_fields_set():
    """Non-empty submission must appear in model_fields_set."""
    resp = client.post("/string", data={"text": "hello"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "text" in body["fields_set"]
    assert body["values"]["text"] == "hello"


# ---------------------------------------------------------------------------
# Mixed model — no data submitted at all
# ---------------------------------------------------------------------------


def test_no_data_fields_set_empty():
    """Submitting no form data produces an empty model_fields_set."""
    resp = client.post("/mixed", data={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == []


def test_partial_data_only_submitted_fields_in_set():
    """Only submitted fields appear in model_fields_set."""
    resp = client.post("/mixed", data={"field_bool": "false"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == ["field_bool"]


def test_all_data_all_fields_in_set():
    """All submitted fields appear in model_fields_set."""
    resp = client.post(
        "/mixed",
        data={"field_bool": "true", "field_str": "world", "field_nullable": "x"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == ["field_bool", "field_nullable", "field_str"]


# ---------------------------------------------------------------------------
# Required fields — must still return 422 when absent
# ---------------------------------------------------------------------------


def test_required_field_absent_returns_422():
    """Required field absent from form must still return a 422 validation error."""
    resp = client.post("/required", data={})
    assert resp.status_code == 422, resp.text
    detail = resp.json()["detail"]
    locs = [e["loc"] for e in detail]
    assert ["body", "required_field"] in locs


def test_required_field_present_optional_absent():
    """Required field present, optional absent → only required field in fields_set."""
    resp = client.post("/required", data={"required_field": "value"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["fields_set"] == ["required_field"]
    assert body["values"]["optional_field"] == "default"


# ---------------------------------------------------------------------------
# Parity with JSON body
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "submitted, expected_set",
    [
        ({}, []),
        ({"field_bool": "true"}, ["field_bool"]),
        ({"field_str": "world"}, ["field_str"]),
        (
            {"field_bool": "false", "field_str": "hi", "field_nullable": "x"},
            ["field_bool", "field_nullable", "field_str"],
        ),
    ],
)
def test_form_fields_set_matches_json(submitted, expected_set):
    """Form and JSON endpoints produce the same model_fields_set for equivalent input."""
    form_resp = client.post("/mixed", data=submitted)
    json_payload = {}
    if "field_bool" in submitted:
        json_payload["field_bool"] = submitted["field_bool"].lower() == "true"
    if "field_str" in submitted:
        json_payload["field_str"] = submitted["field_str"]
    if "field_nullable" in submitted:
        json_payload["field_nullable"] = submitted["field_nullable"]

    json_resp = client.post("/mixed-json", json=json_payload)

    assert form_resp.status_code == 200, form_resp.text
    assert json_resp.status_code == 200, json_resp.text
    assert form_resp.json()["fields_set"] == json_resp.json()["fields_set"] == expected_set
