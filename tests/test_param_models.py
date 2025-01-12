from fastapi import FastAPI
from fastapi.params import Body, Cookie, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

app = FastAPI()


class DataModel(BaseModel):
    alias_with: str = Field(alias="with", default="nothing")


@app.post("/param/body")
def post_param_body(data: Annotated[DataModel, Body()]):
    return data


@app.post("/param/form")
def post_param_form(data: Annotated[DataModel, Form()]):
    return data


@app.post("/param/query")
def post_param_query(data: Annotated[DataModel, Query()]):
    return data


@app.post("/param/cookies")
def post_param_cookies(data: Annotated[DataModel, Cookie()]):
    return data


@app.post("/param/headers")
def post_param_headers(data: Annotated[DataModel, Header()]):
    return data


client = TestClient(app)


def test_param_body_with_alias():
    response = client.post("/param/body", json={"with": "something"})
    assert response.status_code == 200, response.text
    assert response.json() == {"with": "something"}


def test_param_form_with_alias():
    response = client.post("/param/form", data={"with": "something"})
    assert response.status_code == 200, response.text
    assert response.json() == {"with": "something"}


def test_param_query_with_alias():
    response = client.post("/param/query", params={"with": "something"})
    assert response.status_code == 200, response.text
    assert response.json() == {"with": "something"}


def test_param_headers_with_alias():
    response = client.post("/param/headers", headers={"with": "something"})
    assert response.status_code == 200, response.text
    assert response.json() == {"with": "something"}


def test_param_cookies_with_alias():
    with client as c:
        c.cookies.set("with", "something")
        response = c.post("/param/cookies")
    assert response.status_code == 200, response.text
    assert response.json() == {"with": "something"}
