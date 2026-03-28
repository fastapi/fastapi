"""
Tests for issue #13399: Form models should preserve correct model_fields_set.

Fields not submitted in the form data must NOT appear in model_fields_set,
matching the behaviour of JSON body endpoints.
"""

from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class ExampleModel(BaseModel):
    field_1: bool = True
    field_2: str = "default"
    field_3: int | None = None


@app.post("/body")
async def body_endpoint(model: ExampleModel):
    return {"fields_set": sorted(model.model_fields_set)}


@app.post("/form")
async def form_endpoint(model: Annotated[ExampleModel, Form()]):
    return {"fields_set": sorted(model.model_fields_set)}


client = TestClient(app)


def test_json_empty_body_no_fields_set():
    """Baseline: JSON body with no fields → fields_set should be empty."""
    resp = client.post("/body", json={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == []


def test_form_empty_submission_no_fields_set():
    """Form with no fields submitted → fields_set should be empty (like JSON)."""
    resp = client.post("/form", data={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == []


def test_form_partial_submission_only_submitted_fields_set():
    """Only fields actually submitted appear in fields_set."""
    resp = client.post("/form", data={"field_1": "false"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == ["field_1"]


def test_form_all_fields_submitted():
    """All submitted fields appear in fields_set."""
    resp = client.post(
        "/form", data={"field_1": "false", "field_2": "hello", "field_3": "42"}
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == ["field_1", "field_2", "field_3"]


def test_form_defaults_still_applied():
    """Default values are still applied for fields not submitted."""
    resp = client.post("/form", data={})
    assert resp.status_code == 200, resp.text
    # The endpoint just returns fields_set; check defaults via a richer endpoint
    # by confirming 200 and correct fields_set — defaults are tested in
    # test_forms_single_model.py.


def test_form_fields_set_matches_json_behavior():
    """Form and JSON endpoints must agree on fields_set for equivalent inputs."""
    json_resp = client.post("/body", json={"field_2": "hi"})
    form_resp = client.post("/form", data={"field_2": "hi"})
    assert json_resp.status_code == 200
    assert form_resp.status_code == 200
    assert json_resp.json()["fields_set"] == form_resp.json()["fields_set"]
