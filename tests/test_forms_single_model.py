from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class FormModel(BaseModel):
    username: str
    lastname: str
    age: int | None = None
    tags: list[str] = ["foo", "bar"]
    alias_with: str = Field(alias="with", default="nothing")


class FormModelExtraAllow(BaseModel):
    param: str

    model_config = {"extra": "allow"}


@app.post("/form/")
def post_form(user: Annotated[FormModel, Form()]):
    return user


@app.post("/form-extra-allow/")
def post_form_extra_allow(params: Annotated[FormModelExtraAllow, Form()]):
    return params


class FormModelFieldsSet(BaseModel):
    field_1: bool = True


@app.post("/form-model-fields-set/")
def post_form_model_fields_set(model: Annotated[FormModelFieldsSet, Form()]):
    return {"fields_set": sorted(model.model_fields_set)}


@app.post("/body-model-fields-set/")
def post_body_model_fields_set(model: FormModelFieldsSet):
    return {"fields_set": sorted(model.model_fields_set)}


client = TestClient(app)


def test_send_all_data():
    response = client.post(
        "/form/",
        data={
            "username": "Rick",
            "lastname": "Sanchez",
            "age": "70",
            "tags": ["plumbus", "citadel"],
            "with": "something",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "Rick",
        "lastname": "Sanchez",
        "age": 70,
        "tags": ["plumbus", "citadel"],
        "with": "something",
    }


def test_defaults():
    response = client.post("/form/", data={"username": "Rick", "lastname": "Sanchez"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "Rick",
        "lastname": "Sanchez",
        "age": None,
        "tags": ["foo", "bar"],
        "with": "nothing",
    }


def test_invalid_data():
    response = client.post(
        "/form/",
        data={
            "username": "Rick",
            "lastname": "Sanchez",
            "age": "seventy",
            "tags": ["plumbus", "citadel"],
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "age"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "seventy",
            }
        ]
    }


def test_no_data():
    response = client.post("/form/")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": {"tags": ["foo", "bar"], "with": "nothing"},
            },
            {
                "type": "missing",
                "loc": ["body", "lastname"],
                "msg": "Field required",
                "input": {"tags": ["foo", "bar"], "with": "nothing"},
            },
        ]
    }


def test_extra_param_single():
    response = client.post(
        "/form-extra-allow/",
        data={
            "param": "123",
            "extra_param": "456",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "param": "123",
        "extra_param": "456",
    }


def test_extra_param_list():
    response = client.post(
        "/form-extra-allow/",
        data={
            "param": "123",
            "extra_params": ["456", "789"],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "param": "123",
        "extra_params": ["456", "789"],
    }


def test_default_field_not_marked_as_set_for_form_model():
    body_response = client.post("/body-model-fields-set/", json={})
    form_response = client.post("/form-model-fields-set/", data={})

    assert body_response.status_code == 200, body_response.text
    assert form_response.status_code == 200, form_response.text

    assert body_response.json() == {"fields_set": []}
    assert form_response.json() == {"fields_set": []}
