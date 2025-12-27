"""
Test cases for Form() with Pydantic Json[T] type.
Regression tests for issue #10997.
https://github.com/fastapi/fastapi/issues/10997

Before the fix: Json[list[str]] with Form() would wrap values in extra list
After the fix: _is_pydantic_json_field() ensures correct single value extraction
"""

import json
from pathlib import Path
from typing import Annotated

from dirty_equals import IsDict
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel, Json

app = FastAPI()


# ============================================================================
# Endpoints
# ============================================================================


@app.post("/form-json-list")
def form_json_list(items: Annotated[Json[list[str]], Form()]) -> list[str]:
    """Primary bug case - Json[list[str]] with Form()."""
    return items


@app.post("/form-json-dict")
def form_json_dict(data: Annotated[Json[dict[str, str]], Form()]) -> dict[str, str]:
    """Json[dict] parsing."""
    return data


@app.post("/form-json-optional")
def form_json_optional(
    items: Annotated[Json[list[str]] | None, Form()] = None
) -> dict:
    """Optional Json field."""
    return {"items": items, "received": items is not None}


@app.post("/form-json-with-regular-fields")
def form_json_with_regular_fields(
    username: Annotated[str, Form()],
    tags: Annotated[Json[list[str]], Form()],
    age: Annotated[int, Form()],
) -> dict:
    """Json field mixed with regular Form fields."""
    return {"username": username, "tags": tags, "age": age}


class FormWithJsonModel(BaseModel):
    """Pydantic model with Json field for Form()."""

    username: str
    tags: Json[list[str]]


@app.post("/form-json-model")
def form_json_model(form: Annotated[FormWithJsonModel, Form()]) -> FormWithJsonModel:
    """Json field in Pydantic model with Form()."""
    return form


@app.post("/form-json-with-file")
def form_json_with_file(
    tags: Annotated[Json[list[str]], Form()],
    file: UploadFile = File(...),
) -> dict:
    """Json field with File() parameter."""
    return {"tags": tags, "filename": file.filename}


@app.post("/form-regular-list")
def form_regular_list(items: Annotated[list[str], Form()]) -> list[str]:
    """Regular list Form field (without Json wrapper) - must still work."""
    return items


# ============================================================================
# Test Client
# ============================================================================

client = TestClient(app)


# ============================================================================
# Core Functionality Tests
# ============================================================================


def test_form_json_list_str():
    """Test Form() + Json[list[str]] - primary bug case for issue #10997.

    Before the fix, this would incorrectly wrap the JSON string in a list:
        Input: '["abc", "def"]'
        Bug:   [['["abc", "def"]']]  (wrapped in extra list)
        Fix:   ["abc", "def"]        (correctly parsed)
    """
    response = client.post(
        "/form-json-list",
        data={"items": json.dumps(["abc", "def"])},
    )
    assert response.status_code == 200, response.text
    result = response.json()

    # Verify correct parsing
    assert result == ["abc", "def"]

    # Explicitly verify NOT the buggy wrapped version
    assert result != [['["abc", "def"]']]


def test_form_json_dict():
    """Test Form() + Json[dict] - dictionary parsing."""
    test_data = {"name": "John", "city": "NYC"}
    response = client.post(
        "/form-json-dict",
        data={"data": json.dumps(test_data)},
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


# ============================================================================
# Edge Cases Tests
# ============================================================================


def test_form_json_optional_with_none():
    """Test optional Json field with no value sent."""
    response = client.post("/form-json-optional", data={})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["items"] is None
    assert result["received"] is False


def test_form_json_optional_with_value():
    """Test optional Json field with value provided."""
    response = client.post(
        "/form-json-optional",
        data={"items": json.dumps(["test"])},
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["items"] == ["test"]
    assert result["received"] is True


def test_form_json_empty_values():
    """Test Json fields with empty array and object."""
    # Empty list
    response = client.post(
        "/form-json-list",
        data={"items": json.dumps([])},
    )
    assert response.status_code == 200, response.text
    assert response.json() == []

    # Empty dict
    response = client.post(
        "/form-json-dict",
        data={"data": json.dumps({})},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {}


def test_form_json_with_regular_fields():
    """Test Json field mixed with regular Form fields."""
    response = client.post(
        "/form-json-with-regular-fields",
        data={
            "username": "alice",
            "tags": json.dumps(["python", "fastapi"]),
            "age": "30",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "alice",
        "tags": ["python", "fastapi"],
        "age": 30,
    }


# ============================================================================
# Error Handling Tests
# ============================================================================


def test_form_json_missing_required():
    """Test missing required Json field returns validation error."""
    response = client.post("/form-json-list", data={})
    assert response.status_code == 422, response.text
    error_detail = response.json()
    # Note: input can be None or {} depending on form data processing
    assert error_detail == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "items"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "items"],
                    "msg": "Field required",
                    "input": {},
                }
            ]
        }
    ) | IsDict(
        # Pydantic v1 compatibility
        {
            "detail": [
                {
                    "loc": ["body", "items"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


# ============================================================================
# Integration Tests
# ============================================================================


def test_form_json_with_pydantic_model():
    """Test Json field in Pydantic model with Form()."""
    response = client.post(
        "/form-json-model",
        data={
            "username": "alice",
            "tags": json.dumps(["python", "fastapi"]),
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "alice",
        "tags": ["python", "fastapi"],
    }


def test_form_json_with_file_upload(tmp_path: Path):
    """Test Json field with File() parameter in multipart form."""
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("test content")

    response = client.post(
        "/form-json-with-file",
        data={"tags": json.dumps(["important", "urgent"])},
        files={"file": ("test.txt", temp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["tags"] == ["important", "urgent"]
    assert result["filename"] == "test.txt"


def test_form_json_doesnt_break_regular_sequences():
    """Test that regular list Form fields still work correctly.

    This is critical: the fix for Json[T] must not break existing
    Form list behavior. Regular list fields should still use getlist()
    for multiple form values.
    """
    response = client.post(
        "/form-regular-list",
        data={"items": ["x", "y", "z"]},
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["x", "y", "z"]


# ============================================================================
# OpenAPI Schema Test
# ============================================================================


def test_openapi_schema_json_field():
    """Test that OpenAPI schema correctly represents Json fields as string type.

    In OpenAPI, Json[T] form fields should be represented as string type
    (not the inner type like array or object), because the form data contains
    a JSON string that will be parsed by Pydantic, not the parsed structure.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text

    schema = response.json()
    paths = schema["paths"]

    # Check /form-json-list endpoint
    endpoint_schema = paths["/form-json-list"]["post"]
    assert "application/x-www-form-urlencoded" in endpoint_schema["requestBody"]["content"]

    # Get body schema
    body_schema_ref = endpoint_schema["requestBody"]["content"][
        "application/x-www-form-urlencoded"
    ]["schema"]["$ref"]
    schema_name = body_schema_ref.split("/")[-1]
    body_schema = schema["components"]["schemas"][schema_name]

    # Verify Json[list[str]] is represented as string in OpenAPI
    items_field = body_schema["properties"]["items"]
    assert items_field["type"] == "string", (
        f"Json[list[str]] should be 'string' type in OpenAPI, got {items_field}"
    )
