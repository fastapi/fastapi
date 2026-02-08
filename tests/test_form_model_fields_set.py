"""
Test that Form-based dependency models preserve model_fields_set correctly.

This test addresses issue https://github.com/fastapi/fastapi/issues/13399
where Form models were pre-filling default values, making it impossible
to distinguish between explicitly set fields and fields using defaults.
"""

from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel


class ModelWithDefaults(BaseModel):
    field_bool: bool = True
    field_str: str = "default_value"
    field_int: int = 42


app = FastAPI()


@app.post("/json")
async def json_endpoint(model: ModelWithDefaults):
    return {
        "fields_set": list(model.model_fields_set),
        "field_bool": model.field_bool,
        "field_str": model.field_str,
        "field_int": model.field_int,
    }


@app.post("/form")
async def form_endpoint(model: Annotated[ModelWithDefaults, Form()]):
    return {
        "fields_set": list(model.model_fields_set),
        "field_bool": model.field_bool,
        "field_str": model.field_str,
        "field_int": model.field_int,
    }


client = TestClient(app)


def test_json_empty_preserves_fields_set():
    """JSON with empty dict should have empty fields_set"""
    response = client.post("/json", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["fields_set"] == []
    assert data["field_bool"] is True
    assert data["field_str"] == "default_value"
    assert data["field_int"] == 42


def test_json_partial_preserves_fields_set():
    """JSON with partial data should only set provided fields"""
    response = client.post("/json", json={"field_str": "custom"})
    assert response.status_code == 200
    data = response.json()
    assert data["fields_set"] == ["field_str"]
    assert data["field_bool"] is True
    assert data["field_str"] == "custom"
    assert data["field_int"] == 42


def test_json_all_fields_preserves_fields_set():
    """JSON with all fields should mark all as set"""
    response = client.post(
        "/json",
        json={"field_bool": False, "field_str": "custom", "field_int": 100},
    )
    assert response.status_code == 200
    data = response.json()
    assert set(data["fields_set"]) == {"field_bool", "field_str", "field_int"}
    assert data["field_bool"] is False
    assert data["field_str"] == "custom"
    assert data["field_int"] == 100


def test_form_empty_preserves_fields_set():
    """Form with empty data should have empty fields_set (matching JSON behavior)"""
    response = client.post("/form", data={})
    assert response.status_code == 200
    data = response.json()
    # This is the key fix: Form should behave like JSON
    assert data["fields_set"] == []
    assert data["field_bool"] is True
    assert data["field_str"] == "default_value"
    assert data["field_int"] == 42


def test_form_partial_preserves_fields_set():
    """Form with partial data should only set provided fields (matching JSON behavior)"""
    response = client.post("/form", data={"field_str": "custom"})
    assert response.status_code == 200
    data = response.json()
    # This is the key fix: only field_str should be in fields_set
    assert data["fields_set"] == ["field_str"]
    assert data["field_bool"] is True
    assert data["field_str"] == "custom"
    assert data["field_int"] == 42


def test_form_all_fields_preserves_fields_set():
    """Form with all fields should mark all as set"""
    response = client.post(
        "/form",
        data={"field_bool": "false", "field_str": "custom", "field_int": "100"},
    )
    assert response.status_code == 200
    data = response.json()
    assert set(data["fields_set"]) == {"field_bool", "field_str", "field_int"}
    assert data["field_bool"] is False
    assert data["field_str"] == "custom"
    assert data["field_int"] == 100
