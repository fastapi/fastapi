"""Mixed `Form`/`File` and JSON `Body` parameters in one operation.

When an operation mixes form parameters with plain JSON body parameters,
FastAPI builds a single form-typed body field, so `get_request_handler()`
always reads the request with `request.form()`. A JSON request then never
reaches the body fields: every body field is reported missing, even when
the JSON payload carries all of them. Form requests can only satisfy the
JSON body fields when their values happen to be form-compatible scalars,
so an object-typed JSON body field (e.g. `dict`) can never be satisfied
at all.

The handler now dispatches on the request content type for mixed bodies:
JSON requests are parsed as JSON, form requests are parsed as a form.
Pure form and pure JSON operations are untouched.
"""

from typing import Annotated

from fastapi import Body, Depends, FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient


def test_mixed_form_and_body_json_request():
    app = FastAPI()

    @app.post("/mixed")
    def mixed(data: Annotated[dict, Body()], name: Annotated[str, Form()]):
        return {"data": data, "name": name}

    client = TestClient(app)
    response = client.post("/mixed", json={"data": {"a": 1}, "name": "bob"})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": {"a": 1}, "name": "bob"}


def test_mixed_form_and_body_form_request_with_scalar_body():
    app = FastAPI()

    @app.post("/mixed")
    def mixed(count: Annotated[int, Body()], name: Annotated[str, Form()]):
        return {"count": count, "name": name}

    client = TestClient(app)
    response = client.post("/mixed", data={"count": "3", "name": "bob"})
    assert response.status_code == 200, response.text
    assert response.json() == {"count": 3, "name": "bob"}


def test_mixed_form_and_body_dependency_json_request():
    def get_name(name: Annotated[str, Form()]):
        return name

    app = FastAPI()

    @app.post("/mixed")
    def mixed(data: Annotated[dict, Body()], name=Depends(get_name)):
        return {"data": data, "name": name}

    client = TestClient(app)
    response = client.post("/mixed", json={"data": {"a": 1}, "name": "bob"})
    assert response.status_code == 200, response.text
    assert response.json() == {"data": {"a": 1}, "name": "bob"}


def test_mixed_form_and_body_form_request_cannot_carry_object_body():
    app = FastAPI()

    @app.post("/mixed")
    def mixed(data: Annotated[dict, Body()], name: Annotated[str, Form()]):
        return {"data": data, "name": name}

    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/mixed", data={"name": "bob", "data": '{"a": 1}'})
    assert response.status_code == 422, response.text


def test_pure_form_endpoint_json_request_still_rejected():
    app = FastAPI()

    @app.post("/form-only")
    def form_only(name: Annotated[str, Form()]):
        return {"name": name}

    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/form-only", json={"name": "bob"})
    assert response.status_code == 422, response.text


def test_mixed_file_and_body_json_request_reports_file_missing():
    app = FastAPI()

    @app.post("/mixed-file")
    def mixed_file(data: Annotated[dict, Body()], file: Annotated[UploadFile, File()]):
        return {"data": data, "filename": file.filename}

    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/mixed-file", json={"data": {"a": 1}})
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["loc"] == ["body", "file"]
