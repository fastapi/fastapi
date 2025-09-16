"""
Test cases for form default value behavior.

Tests the fix for issue #13533: Restore default value behavior for empty form fields
in both x-www-form-urlencoded and multipart forms.
"""

from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.post("/form-urlencoded/")
def form_urlencoded_endpoint(
    name: Annotated[str, Form()] = "default_name",
    age: Annotated[Optional[int], Form()] = None,
    email: Annotated[Optional[str], Form()] = "default@example.com",
):
    """Test x-www-form-urlencoded form with default values."""
    return {"name": name, "age": age, "email": email}


@app.post("/multipart/")
def multipart_endpoint(
    name: Annotated[str, Form()] = "default_name",
    age: Annotated[Optional[int], Form()] = None,
    email: Annotated[Optional[str], Form()] = "default@example.com",
    file: Annotated[Optional[UploadFile], File()] = None,
):
    """Test multipart form with default values."""
    return {
        "name": name,
        "age": age,
        "email": email,
        "file": file.filename if file else None,
    }


client = TestClient(app)


def test_form_urlencoded_field_missing_uses_default():
    """Test that missing fields use default values in x-www-form-urlencoded forms."""
    response = client.post("/form-urlencoded/", data={})
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,
        "email": "default@example.com",
    }


def test_form_urlencoded_field_empty_uses_default():
    """Test that empty string fields use default values in x-www-form-urlencoded forms."""
    response = client.post(
        "/form-urlencoded/", data={"name": "", "age": "", "email": ""}
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,
        "email": "default@example.com",
    }


def test_form_urlencoded_field_with_value_uses_value():
    """Test that fields with values use the provided values in x-www-form-urlencoded forms."""
    response = client.post(
        "/form-urlencoded/",
        data={"name": "John", "age": "25", "email": "john@example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "John",
        "age": 25,
        "email": "john@example.com",
    }


def test_form_urlencoded_mixed_empty_and_values():
    """Test mixed empty and non-empty fields in x-www-form-urlencoded forms."""
    response = client.post(
        "/form-urlencoded/",
        data={"name": "Jane", "age": "", "email": "jane@example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Jane",
        "age": None,  # Empty string should use default (None)
        "email": "jane@example.com",
    }


def test_multipart_field_missing_uses_default():
    """Test that missing fields use default values in multipart forms."""
    response = client.post("/multipart/", data={})
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,
        "email": "default@example.com",
        "file": None,
    }


def test_multipart_field_empty_uses_default():
    """Test that empty string fields use default values in multipart forms."""
    response = client.post("/multipart/", data={"name": "", "age": "", "email": ""})
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,
        "email": "default@example.com",
        "file": None,
    }


def test_multipart_field_with_value_uses_value():
    """Test that fields with values use the provided values in multipart forms."""
    response = client.post(
        "/multipart/",
        data={"name": "Alice", "age": "30", "email": "alice@example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
        "file": None,
    }


def test_multipart_with_file_and_empty_fields():
    """Test multipart form with file upload and empty fields."""
    files = {"file": ("test.txt", "content", "text/plain")}
    response = client.post(
        "/multipart/",
        data={"name": "", "age": "35", "email": ""},
        files=files,
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",  # Empty string should use default
        "age": 35,
        "email": "default@example.com",  # Empty string should use default
        "file": "test.txt",
    }


def test_multipart_mixed_empty_and_values():
    """Test mixed empty and non-empty fields in multipart forms."""
    response = client.post(
        "/multipart/",
        data={"name": "Bob", "age": "", "email": "bob@example.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Bob",
        "age": None,  # Empty string should use default (None)
        "email": "bob@example.com",
        "file": None,
    }


def test_form_urlencoded_optional_int_with_empty_string():
    """Test that Optional[int] fields with empty strings use default values."""
    response = client.post("/form-urlencoded/", data={"age": ""})
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,  # Empty string should use default (None)
        "email": "default@example.com",
    }


def test_multipart_optional_int_with_empty_string():
    """Test that Optional[int] fields with empty strings use default values in multipart."""
    response = client.post("/multipart/", data={"age": ""})
    assert response.status_code == 200
    assert response.json() == {
        "name": "default_name",
        "age": None,  # Empty string should use default (None)
        "email": "default@example.com",
        "file": None,
    }
