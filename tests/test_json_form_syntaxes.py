import json
from typing import Annotated, Any

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import Json

app = FastAPI()


@app.post("/form-json-equals-syntax")
def form_json_equals_syntax(data: Json[dict[str, Any]] = Form()) -> dict[str, Any]:
    return data


@app.post("/form-json-annotated-syntax")
def form_json_annotated_syntax(
    data: Annotated[Json[dict[str, Any]], Form()],
) -> dict[str, Any]:
    return data


@app.post("/form-json-list-equals")
def form_json_list_equals(items: Json[list[str]] = Form()) -> list[str]:
    return items


@app.post("/form-json-list-annotated")
def form_json_list_annotated(
    items: Annotated[Json[list[str]], Form()],
) -> list[str]:
    return items


@app.post("/form-json-nested-equals")
def form_json_nested_equals(
    config: Json[dict[str, list[int]]] = Form(),
) -> dict[str, list[int]]:
    return config


@app.post("/form-json-nested-annotated")
def form_json_nested_annotated(
    config: Annotated[Json[dict[str, list[int]]], Form()],
) -> dict[str, list[int]]:
    return config


client = TestClient(app)


def test_form_json_equals_syntax():
    test_data = {"key": "value", "nested": {"inner": 123}}
    response = client.post(
        "/form-json-equals-syntax", data={"data": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_annotated_syntax():
    test_data = {"key": "value", "nested": {"inner": 123}}
    response = client.post(
        "/form-json-annotated-syntax", data={"data": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_list_equals():
    test_data = ["abc", "def", "ghi"]
    response = client.post(
        "/form-json-list-equals", data={"items": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_list_annotated():
    test_data = ["abc", "def", "ghi"]
    response = client.post(
        "/form-json-list-annotated", data={"items": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_nested_equals():
    test_data = {"groups": [1, 2, 3], "ids": [4, 5]}
    response = client.post(
        "/form-json-nested-equals", data={"config": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_nested_annotated():
    test_data = {"groups": [1, 2, 3], "ids": [4, 5]}
    response = client.post(
        "/form-json-nested-annotated", data={"config": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_invalid_json_equals():
    response = client.post("/form-json-equals-syntax", data={"data": "not valid json{"})
    assert response.status_code == 422


def test_form_json_invalid_json_annotated():
    response = client.post(
        "/form-json-annotated-syntax", data={"data": "not valid json{"}
    )
    assert response.status_code == 422


def test_form_json_empty_dict_equals():
    test_data = {}
    response = client.post(
        "/form-json-equals-syntax", data={"data": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_form_json_empty_list_equals():
    test_data = []
    response = client.post(
        "/form-json-list-equals", data={"items": json.dumps(test_data)}
    )
    assert response.status_code == 200, response.text
    assert response.json() == test_data
