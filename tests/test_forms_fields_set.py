"""
Tests for Form fields preserving model_fields_set metadata.
Related to issue #13399: https://github.com/fastapi/fastapi/issues/13399

This test validates that Form models correctly track which fields were
explicitly provided vs. which fields use defaults.
"""

from typing import Annotated

from fastapi import FastAPI, Form
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel


class FormModelFieldsSet(BaseModel):
    """Model for testing fields_set metadata preservation."""

    field_1: bool = True
    field_2: str = "default"
    field_3: int = 42


app = FastAPI()


@app.post("/form-fields-set")
async def form_fields_set_endpoint(model: Annotated[FormModelFieldsSet, Form()]):
    # Use correct attribute name for each Pydantic version
    if PYDANTIC_V2:
        fields_set = list(model.model_fields_set)
    else:
        fields_set = list(model.__fields_set__)
    return {
        "fields_set": fields_set,
        "data": model.dict() if not PYDANTIC_V2 else model.model_dump(),
    }


@app.post("/body-fields-set")
async def body_fields_set_endpoint(model: FormModelFieldsSet):
    # Use correct attribute name for each Pydantic version
    if PYDANTIC_V2:
        fields_set = list(model.model_fields_set)
    else:
        fields_set = list(model.__fields_set__)
    return {"fields_set": fields_set}


client = TestClient(app)


class TestFormFieldsSetMetadata:
    """Test that Form models correctly preserve fields_set metadata."""

    def test_form_empty_data_has_empty_fields_set(self):
        """Form with no data should have empty fields_set (matching JSON behavior)."""
        resp = client.post("/form-fields-set", data={})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == []

    def test_body_empty_data_has_empty_fields_set(self):
        """JSON body with no data should have empty fields_set."""
        resp = client.post("/body-fields-set", json={})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == []

    def test_form_partial_data_tracks_provided_fields(self):
        """Form with partial data should only show provided fields in fields_set."""
        resp = client.post("/form-fields-set", data={"field_1": "False"})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_body_partial_data_tracks_provided_fields(self):
        """JSON body with partial data should only show provided fields."""
        resp = client.post("/body-fields-set", json={"field_1": False})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_form_all_fields_provided(self):
        """Form with all fields should show all fields in fields_set."""
        resp = client.post(
            "/form-fields-set",
            data={"field_1": "False", "field_2": "test", "field_3": "100"},
        )
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert set(fields_set) == {"field_1", "field_2", "field_3"}

    def test_body_all_fields_provided(self):
        """JSON body with all fields should show all fields in fields_set."""
        resp = client.post(
            "/body-fields-set",
            json={"field_1": False, "field_2": "test", "field_3": 100},
        )
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert set(fields_set) == {"field_1", "field_2", "field_3"}

    def test_form_field_set_to_default_value_is_tracked(self):
        """Form field explicitly set to default value should appear in fields_set."""
        # Same as default=True, but explicitly provided
        resp = client.post("/form-fields-set", data={"field_1": "True"})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_body_field_set_to_default_value_is_tracked(self):
        """JSON body field explicitly set to default value should appear in fields_set."""
        resp = client.post("/body-fields-set", json={"field_1": True})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_form_body_consistency(self):
        """
        Verify that body and form behave consistently.
        Form fields_set should match JSON body fields_set for equivalent data.
        """
        # Empty data - both should have empty fields_set
        body_resp = client.post("/body-fields-set", json={})
        form_resp = client.post("/form-fields-set", data={})
        assert body_resp.json()["fields_set"] == []
        assert form_resp.json()["fields_set"] == []

        # Partial data - both should track same fields
        body_resp = client.post(
            "/body-fields-set", json={"field_1": False, "field_3": 99}
        )
        form_resp = client.post(
            "/form-fields-set", data={"field_1": "False", "field_3": "99"}
        )
        assert set(body_resp.json()["fields_set"]) == {"field_1", "field_3"}
        assert set(form_resp.json()["fields_set"]) == {"field_1", "field_3"}
