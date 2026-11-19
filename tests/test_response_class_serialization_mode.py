import datetime
from decimal import Decimal
from typing import Any

import pytest
from fastapi import FastAPI, Response
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel


class PythonReprResponse(Response):
    media_type = "text/plain"
    serialization_mode = "python"

    def render(self, content: Any) -> bytes:
        return repr(content).encode()


class ReprResponse(Response):
    media_type = "text/plain"

    def render(self, content: Any) -> bytes:
        return repr(content).encode()


class Item(BaseModel):
    tags: set[str]
    when: datetime.date
    price: Decimal


app = FastAPI()


@app.get("/python/raw", response_class=PythonReprResponse)
def get_python_raw():
    return {"point": (1, 2), "tags": {"a"}, "when": datetime.date(2026, 11, 19)}


@app.get("/python/model", response_class=PythonReprResponse)
def get_python_model() -> Item:
    return Item(tags={"a"}, when=datetime.date(2026, 11, 19), price=Decimal("1.50"))


@app.get("/python/invalid", response_class=PythonReprResponse, response_model=Item)
def get_python_invalid():
    return {"tags": "a"}


@app.get("/json/raw", response_class=ReprResponse)
def get_json_raw():
    return {"point": (1, 2), "when": datetime.date(2026, 11, 19)}


client = TestClient(app)


def test_python_data_without_response_model():
    response = client.get("/python/raw")
    assert (
        response.text
        == "{'point': (1, 2), 'tags': {'a'}, 'when': datetime.date(2026, 11, 19)}"
    )


def test_python_data_from_response_model():
    response = client.get("/python/model")
    assert (
        response.text
        == "{'tags': {'a'}, 'when': datetime.date(2026, 11, 19), 'price': Decimal('1.50')}"
    )


def test_python_data_is_still_validated():
    with pytest.raises(ResponseValidationError):
        client.get("/python/invalid")


def test_json_compatible_data_by_default():
    response = client.get("/json/raw")
    assert response.text == "{'point': [1, 2], 'when': '2026-11-19'}"
