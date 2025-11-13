from typing import List, Optional

from dirty_equals import IsDict
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

app = FastAPI()


class FormModel(BaseModel):
    username: str
    lastname: str
    age: Optional[int] = None
    tags: List[str] = ["foo", "bar"]
    alias_with: str = Field(alias="with", default="nothing")


@app.post("/form/")
def post_form(user: Annotated[FormModel, Form()]):
    return user


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
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "age"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "seventy",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "age"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_no_data():
    response = client.post("/form/")
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
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
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "lastname"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )
