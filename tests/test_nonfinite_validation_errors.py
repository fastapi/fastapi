import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, FiniteFloat

app = FastAPI()


class Item(BaseModel):
    value: int


class NestedItem(BaseModel):
    payload: dict[str, int]


class FiniteItem(BaseModel):
    value: FiniteFloat


@app.post("/items")
def create_item(item: Item) -> Item:
    return item  # pragma: no cover


@app.post("/nested")
def create_nested(item: NestedItem) -> NestedItem:
    return item  # pragma: no cover


@app.post("/finite")
def create_finite(item: FiniteItem) -> FiniteItem:
    return item  # pragma: no cover


client = TestClient(app, raise_server_exceptions=False)

json_headers = {"Content-Type": "application/json"}


@pytest.mark.parametrize(
    "raw,expected_input",
    [
        ('{"value": NaN}', "nan"),
        ('{"value": Infinity}', "inf"),
        ('{"value": -Infinity}', "-inf"),
    ],
)
def test_non_finite_input_returns_422(raw: str, expected_input: str):
    response = client.post("/items", content=raw, headers=json_headers)
    assert response.status_code == 422, response.text
    data = response.json()
    assert data["detail"][0]["type"] == "finite_number"
    assert data["detail"][0]["input"] == expected_input


def test_non_finite_input_with_finite_float_field_returns_422():
    response = client.post("/finite", content='{"value": NaN}', headers=json_headers)
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["input"] == "nan"


def test_non_finite_input_nested_returns_422():
    response = client.post(
        "/nested",
        content='{"payload": {"a": 1, "b": NaN}}',
        headers=json_headers,
    )
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["input"] == "nan"


def test_finite_input_stays_numeric():
    response = client.post("/items", content='{"value": 1.5}', headers=json_headers)
    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["input"] == 1.5


def test_valid_input_still_works():
    response = client.post("/items", content='{"value": 1}', headers=json_headers)
    assert response.status_code == 200, response.text
    assert response.json() == {"value": 1}
