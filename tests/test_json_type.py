import json
from typing import Annotated

from fastapi import Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import Json

app = FastAPI()


@app.post("/form-json-list")
def form_json_list(items: Annotated[Json[list[str]], Form()]) -> list[str]:
    return items


@app.get("/query-json-list")
def query_json_list(items: Annotated[Json[list[str]], Query()]) -> list[str]:
    return items


@app.get("/header-json-list")
def header_json_list(x_items: Annotated[Json[list[str]], Header()]) -> list[str]:
    return x_items


@app.get("/cookie-json-list")
def cookie_json_list(items: Annotated[Json[list[str]], Cookie()]) -> list[str]:
    return items


client = TestClient(app)


def test_form_json_list():
    response = client.post(
        "/form-json-list", data={"items": json.dumps(["abc", "def"])}
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]


def test_query_json_list():
    response = client.get(
        "/query-json-list", params={"items": json.dumps(["abc", "def"])}
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]


def test_header_json_list():
    response = client.get(
        "/header-json-list", headers={"x-items": json.dumps(["abc", "def"])}
    )
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]


def test_cookie_json_list():
    client.cookies.set("items", json.dumps(["abc", "def"]))
    response = client.get("/cookie-json-list")
    assert response.status_code == 200, response.text
    assert response.json() == ["abc", "def"]
    client.cookies.clear()
