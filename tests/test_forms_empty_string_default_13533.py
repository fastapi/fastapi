"""
Test for issue #13533: Multiple regressions in the handling of forms & form validation

This test verifies that empty strings in form fields are correctly handled:
- For optional fields with None default, empty string should result in None
- For optional fields with int type, empty string should result in None (not parsing error)
- This applies to both x-www-form-urlencoded and multipart/form-data
"""

from typing import Annotated, Optional

from fastapi import FastAPI, File, Form
from fastapi.testclient import TestClient

# Test app for URL-encoded forms with optional string
app_urlencoded_str = FastAPI()


@app_urlencoded_str.post("/test")
def endpoint_urlencoded_str(
    name: Annotated[Optional[str], Form(embed=True)] = None,
):
    return {"name": name}


# Test app for URL-encoded forms with optional int
app_urlencoded_int = FastAPI()


@app_urlencoded_int.post("/test")
def endpoint_urlencoded_int(
    age: Annotated[Optional[int], Form()] = None,
):
    return {"age": age}


# Test app for multipart forms
app_multipart = FastAPI()


@app_multipart.post("/test")
def endpoint_multipart(
    file: Annotated[Optional[bytes], File()] = None,
    name: Annotated[Optional[str], Form(embed=True)] = None,
):
    return {"file_size": len(file) if file else None, "name": name}


def test_urlencoded_empty_string_optional_str():
    """
    Regression test for #13533: Empty string in URL-encoded form
    with optional str field should use default value (None)
    """
    client = TestClient(app_urlencoded_str)
    response = client.post("/test", data={"name": ""})
    assert response.status_code == 200
    assert response.json() == {"name": None}


def test_urlencoded_empty_string_optional_int():
    """
    Regression test for #13533: Empty string in URL-encoded form
    with optional int field should use default value (None), not cause parsing error
    """
    client = TestClient(app_urlencoded_int)
    response = client.post("/test", data={"age": ""})
    assert response.status_code == 200
    assert response.json() == {"age": None}


def test_multipart_empty_string_optional_str():
    """
    Regression test for #13533: Empty string in multipart form
    with optional str field should use default value (None)
    """
    client = TestClient(app_multipart)
    response = client.post("/test", data={"name": ""})
    assert response.status_code == 200
    assert response.json() == {"file_size": None, "name": None}


def test_urlencoded_with_actual_value():
    """Verify that actual values still work correctly"""
    client = TestClient(app_urlencoded_str)
    response = client.post("/test", data={"name": "John"})
    assert response.status_code == 200
    assert response.json() == {"name": "John"}


def test_urlencoded_int_with_actual_value():
    """Verify that actual int values still work correctly"""
    client = TestClient(app_urlencoded_int)
    response = client.post("/test", data={"age": "25"})
    assert response.status_code == 200
    assert response.json() == {"age": 25}


def test_multipart_with_actual_value():
    """Verify that actual values in multipart forms still work correctly"""
    client = TestClient(app_multipart)
    response = client.post("/test", data={"name": "John"})
    assert response.status_code == 200
    assert response.json() == {"file_size": None, "name": "John"}
