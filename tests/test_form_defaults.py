# NOTE: Documentation requirement is not validated by tests; reviewer should check manually.

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/demo/")
def demo_endpoint(field: str = Form("default_value")):
    return {"field": field}

@app.post("/demo_int/")
def demo_int_endpoint(field: int = Form(42)):
    return {"field": field}

@app.post("/demo_float/")
def demo_float_endpoint(field: float = Form(3.14)):
    return {"field": field}

@app.post("/demo_opt/")
def demo_opt_endpoint(field: str = Form(None)):
    return {"field": field}

@app.post("/fileupload/")
def fileupload_endpoint(file: UploadFile = File(None)):
    return {"filename": file.filename if file else None}

@app.post("/other/")
def other_endpoint(foo: str = Form("other")):
    return {"foo": foo}

client = TestClient(app)

def test_blank_field_uses_default():
    response = client.post("/demo/", data={"field": ""})
    assert response.json()["field"] == "default_value"

def test_missing_field_uses_default():
    response = client.post("/demo/", data={})
    assert response.json()["field"] == "default_value"

def test_blank_int_field_uses_default():
    response = client.post("/demo_int/", data={"field": ""})
    assert response.json()["field"] == 42

def test_missing_int_field_uses_default():
    response = client.post("/demo_int/", data={})
    assert response.json()["field"] == 42

def test_blank_float_field_uses_default():
    response = client.post("/demo_float/", data={"field": ""})
    assert response.json()["field"] == 3.14

def test_missing_float_field_uses_default():
    response = client.post("/demo_float/", data={})
    assert response.json()["field"] == 3.14

def test_optional_field_default_none():
    response = client.post("/demo_opt/", data={})
    assert response.json()["field"] is None

def test_blank_optional_field_results_in_none():
    response = client.post("/demo_opt/", data={"field": ""})
    assert response.json()["field"] is None

def test_blank_field_multipart_uses_default():
    response = client.post("/demo/", files={"field": ("", "")})
    assert response.json()["field"] == "default_value"

def test_missing_field_multipart_uses_default():
    response = client.post("/demo/", files={})
    assert response.json()["field"] == "default_value"

def test_multipart_blank_text_field_uses_default():
    response = client.post("/demo/", data={"field": ""}, files={"dummy": ("filename.txt", "dummycontent")})
    assert response.json()["field"] == "default_value"

def test_multipart_blank_int_field_uses_default():
    response = client.post("/demo_int/", data={"field": ""}, files={"dummy": ("file.txt", "dummy")})
    assert response.json()["field"] == 42

def test_multipart_blank_float_field_uses_default():
    response = client.post("/demo_float/", data={"field": ""}, files={"dummy": ("file.txt", "dummy")})
    assert response.json()["field"] == 3.14

def test_blank_uploadfile_defaults_to_none():
    response = client.post("/fileupload/", files={"file": ("", "")})
    assert response.json()["filename"] is None

def test_fileupload_actual_upload_works():
    files = {"file": ("afile.txt", "dummydata")}
    response = client.post("/fileupload/", files=files)
    assert response.json()["filename"] == "afile.txt"

def test_json_request_unaffected():
    response = client.post("/demo/", json={"field": ""})
    assert response.json()["field"] == ""

def test_json_missing_field_uses_default():
    response = client.post("/demo/", json={})
    assert response.json()["field"] == "default_value"

def test_other_request_regression_not_broken():
    response = client.post("/other/", data={})
    assert response.json()["foo"] == "other"

