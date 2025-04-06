import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.post("/old-style", operation_id="old_style")
def route_with_form(form_param: str = Form(alias="aliased-field")):
    return {}


@app.post("/annotated", operation_id="annotated")
def route_with_form_annotated(form_param: Annotated[str, Form(alias="aliased-field")]):
    return {}


client = TestClient(app)


@pytest.mark.parametrize("path", ["/old-style", "/annotated"])
def test_get_route(path: str):
    response = client.post(path, data={"aliased-field": "Hello, World!"})
    assert response.status_code == 200, response.text
    assert response.json() == {}


@pytest.mark.parametrize("schema_obj", ["Body_annotated", "Body_old_style"])
def test_form_alias_is_correct(schema_obj: str):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    form_properties = response.json()["components"]["schemas"][schema_obj]["properties"]
    assert "aliased-field" in form_properties
