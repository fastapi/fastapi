import json
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Json

app = FastAPI()


class JsonListModel(BaseModel):
    json_list: Json[list[str]]


@app.post("/form-str")
def form_str(json_list: Annotated[str, Form()]) -> list[str]:
    model = JsonListModel(json_list=json_list) # type: ignore[arg-type]
    return model.json_list


@app.post("/form-json-list")
def form_json_list(json_list: Annotated[Json[list[str]], Form()]) -> list[str]:
    return json_list


client = TestClient(app)


def test_form_str():
    response = client.post(
        "/form-str",
        data={"json_list": json.dumps(["abc", "def"])},
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]


def test_form_json_list():
    response = client.post(
        "/form-json-list",
        data={"json_list": json.dumps(["abc", "def"])},
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]
