"""
Tests for Form fields preserving model_fields_set metadata.
Related to issue #13399: https://github.com/fastapi/fastapi/issues/13399

This test validates that Form models correctly track which fields were
explicitly provided vs. which fields use defaults.
"""

import pydantic
from fastapi import FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing_extensions import Annotated  # noqa: UP035

PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2


class FormModelFieldsSet(BaseModel):
    """Model for testing fields_set metadata preservation."""

    field_1: bool = True
    field_2: str = "default"
    field_3: int = 42


app = FastAPI()


@app.post("/form-fields-set")
async def form_fields_set_endpoint(
    model: Annotated[FormModelFieldsSet, Form()],
) -> None:
    # Works for both Pydantic v1 (__fields_set__) and v2 (model_fields_set)
    fields_set = list(
        model.model_fields_set
        if hasattr(model, "model_fields_set")
        else model.__fields_set__  # type: ignore[attr-defined]
    )
    return {
        "fields_set": fields_set,
        "data": model.model_dump() if PYDANTIC_V2 else model.dict(),
    }


@app.post("/body-fields-set")
async def body_fields_set_endpoint(model: FormModelFieldsSet) -> None:
    # Works for both Pydantic v1 (__fields_set__) and v2 (model_fields_set)
    fields_set = list(
        model.model_fields_set
        if hasattr(model, "model_fields_set")
        else model.__fields_set__  # type: ignore[attr-defined]
    )
    return {"fields_set": fields_set}


@app.get("/query/default")
def query_model(
    name: Annotated[str, Query()] = "query_default",
    age: Annotated[int, Query()] = 10,
) -> None:
    return {"name": name, "age": age}


@app.get("/header/default")
def header_model(
    x_token: Annotated[str, Header()] = "header_default",
) -> None:
    return {"x_token": x_token}


client = TestClient(app)


class TestFormFieldsSetMetadata:
    """Test that Form models correctly preserve fields_set metadata."""

    def test_form_empty_data_has_empty_fields_set(self) -> None:
        """Form with no data should have empty fields_set (matching JSON behavior)."""
        resp = client.post("/form-fields-set", data={})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == []

    def test_body_empty_data_has_empty_fields_set(self) -> None:
        """JSON body with no data should have empty fields_set."""
        resp = client.post("/body-fields-set", json={})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == []

    def test_form_partial_data_tracks_provided_fields(self) -> None:
        """Form with partial data should only show provided fields in fields_set."""
        resp = client.post("/form-fields-set", data={"field_1": "False"})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_body_partial_data_tracks_provided_fields(self) -> None:
        """JSON body with partial data should only show provided fields."""
        resp = client.post("/body-fields-set", json={"field_1": False})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_form_all_fields_provided(self) -> None:
        """Form with all fields should show all fields in fields_set."""
        resp = client.post(
            "/form-fields-set",
            data={"field_1": "False", "field_2": "test", "field_3": "100"},
        )
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert set(fields_set) == {"field_1", "field_2", "field_3"}

    def test_body_all_fields_provided(self) -> None:
        """JSON body with all fields should show all fields in fields_set."""
        resp = client.post(
            "/body-fields-set",
            json={"field_1": False, "field_2": "test", "field_3": 100},
        )
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert set(fields_set) == {"field_1", "field_2", "field_3"}

    def test_form_field_set_to_default_value_is_tracked(self) -> None:
        """Form field explicitly set to default value should appear in fields_set."""
        # Same as default=True, but explicitly provided
        resp = client.post("/form-fields-set", data={"field_1": "True"})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_body_field_set_to_default_value_is_tracked(self) -> None:
        """JSON body field explicitly set to default value should appear in fields_set."""
        resp = client.post("/body-fields-set", json={"field_1": True})
        assert resp.status_code == 200, resp.text
        fields_set = resp.json()["fields_set"]
        assert fields_set == ["field_1"]

    def test_form_body_consistency(self) -> None:
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


class TestNonFormCoverage:
    """
    Test that non-Form parameters (Query, Header) continue to use defaults.
    This ensures line 762 of utils.py is covered and legacy behavior is preserved.
    """

    def test_query_params_missing_uses_defaults(self) -> None:
        """Test Query input where fields are missing -> returns default."""
        response = client.get("/query/default")
        assert response.status_code == 200
        data = response.json()
        assert data == {"name": "query_default", "age": 10}

    def test_header_params_missing_uses_defaults(self) -> None:
        """Test Header input where fields are missing -> returns default."""
        response = client.get("/header/default")
        assert response.status_code == 200
        data = response.json()
        assert data == {"x_token": "header_default"}

    def test_query_params_provided(self) -> None:
        """Test Query input where fields are provided -> returns value."""
        response = client.get("/query/default?name=overridden&age=99")
        assert response.status_code == 200
        data = response.json()
        assert data == {"name": "overridden", "age": 99}
