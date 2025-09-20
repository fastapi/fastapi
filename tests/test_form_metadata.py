from typing import Annotated, Optional

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class ExampleModel(BaseModel):
    field_1: Optional[bool] = None  # Optional, so not set by default


@app.post("/body")
async def body_endpoint(model: ExampleModel):
    return {"fields_set": list(model.model_fields_set)}


@app.post("/form")
async def form_endpoint(model: Annotated[ExampleModel, Form()]):
    return {"fields_set": list(model.model_fields_set)}


client = TestClient(app)


def test_form_fields_set_empty():
    response = client.post("/body", json={})
    assert response.status_code == 200
    assert response.json() == {"fields_set": []}

    response = client.post("/form", data={})
    assert response.status_code == 200
    assert response.json() == {"fields_set": []}
