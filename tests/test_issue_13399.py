# tests/test_issue_13399.py
from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel

class ExampleModel(BaseModel):
    field_1: bool = True

app = FastAPI()

@app.post("/body")
async def body_endpoint(model: ExampleModel):
    fields = getattr(model, "model_fields_set", set())
    return {"fields_set": list(fields)}

@app.post("/form")
async def form_endpoint(model: Annotated[ExampleModel, Form()]):
    fields = getattr(model, "model_fields_set", set())
    return {"fields_set": list(fields)}

client = TestClient(app)

def test_body():
    resp = client.post("/body", json={})
    assert resp.status_code == 200, resp.text
    assert resp.json()["fields_set"] == []

def test_form():
    resp = client.post("/form", data={})
    assert resp.status_code == 200, resp.text
    # the bug: this currently returns ['field_1'] instead of []
    assert resp.json()["fields_set"] == []
