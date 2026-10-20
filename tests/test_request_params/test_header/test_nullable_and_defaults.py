from typing import Annotated

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field, model_validator

app = FastAPI()


@app.get("/parameter")
def read_parameter(int_val: Annotated[int | None, Header()]):
    return int_val


class Model(BaseModel):
    int_val: int | None


@app.get("/model")
def read_model(params: Annotated[Model, Header()]):
    return params.int_val


client = TestClient(app)


@pytest.mark.parametrize(
    "path,title", [("/parameter", "Int-Val"), ("/model", "Int Val")]
)
def test_nullable_header_uses_hyphenated_name(path, title):
    response = client.get(path, headers={"int-val": "0"})
    assert response.status_code == 200
    assert response.json() == 0
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    field = response.json()["paths"][path]["get"]["parameters"][0]
    assert field["name"] == "int-val"
    assert field["in"] == "header"
    assert field["required"] is True
    assert field["schema"]["title"] == title
    assert field["schema"]["anyOf"] == [{"type": "integer"}, {"type": "null"}]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "headers,error_type",
    [({}, "missing"), ({"int-val": "invalid"}, "int_parsing")],
)
def test_nullable_header_error_uses_hyphenated_name(path, headers, error_type):
    response = client.get(path, headers=headers)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["header", "int-val"]),
    ]


@pytest.mark.parametrize(
    "headers,error_type",
    [({}, "missing"), ({"int_val": "invalid"}, "int_parsing")],
)
def test_header_model_without_underscore_conversion(headers, error_type):
    app = FastAPI()

    @app.get("/")
    def read_model(params: Annotated[Model, Header(convert_underscores=False)]):
        return params.int_val

    client = TestClient(app)
    response = client.get("/", headers={"int_val": "1"})
    assert response.status_code == 200
    assert response.json() == 1

    response = client.get("/", headers=headers)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["header", "int_val"]),
    ]


@pytest.mark.parametrize(
    "headers,error_type",
    [
        ({}, "missing"),
        (
            {"int-val": "invalid", "x_count": "invalid", "x_total": "invalid"},
            "int_parsing",
        ),
    ],
)
def test_header_model_preserves_explicit_aliases(headers, error_type):
    app = FastAPI()

    class AliasHeaders(BaseModel):
        int_val: int
        count: Annotated[int, Field(alias="x_count")]
        total: Annotated[int, Field(alias="unused", validation_alias="x_total")]

    @app.get("/")
    def read_model(params: Annotated[AliasHeaders, Header()]):
        return params

    client = TestClient(app)
    response = client.get("/", headers={"int-val": "1", "x_count": "2", "x_total": "3"})
    assert response.status_code == 200
    assert response.json() == {"int_val": 1, "x_count": 2, "unused": 3}

    response = client.get("/", headers=headers)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["header", "int-val"]),
        (error_type, ["header", "x_count"]),
        (error_type, ["header", "x_total"]),
    ]


@pytest.mark.parametrize(
    "headers,error_type",
    [({}, "missing"), ({"int-val": "invalid", "x_count": "invalid"}, "int_parsing")],
)
def test_header_model_can_report_python_field_names(headers, error_type):
    app = FastAPI()

    class NameLocationHeaders(BaseModel):
        model_config = ConfigDict(loc_by_alias=False)
        int_val: int
        item_count: Annotated[int, Field(alias="x_count")]

    @app.get("/")
    def read_model(params: Annotated[NameLocationHeaders, Header()]):
        return params

    client = TestClient(app)
    response = client.get("/", headers={"int-val": "1", "x_count": "2"})
    assert response.status_code == 200
    assert response.json() == {"int_val": 1, "x_count": 2}

    response = client.get("/", headers=headers)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["header", "int_val"]),
        (error_type, ["header", "item_count"]),
    ]


def test_header_model_list_error_preserves_item_index():
    app = FastAPI()

    class ListHeaders(BaseModel):
        item_ids: list[int]

    @app.get("/")
    def read_model(params: Annotated[ListHeaders, Header()]):
        return params.item_ids

    client = TestClient(app)
    response = client.get("/", headers=[("item-ids", "1"), ("item-ids", "2")])
    assert response.status_code == 200
    assert response.json() == [1, 2]

    response = client.get("/", headers=[("item-ids", "1"), ("item-ids", "invalid")])
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["header", "item-ids", 1],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


def test_header_model_validation_error_has_no_field_location():
    app = FastAPI()

    class RangeHeaders(BaseModel):
        range_start: int
        range_end: int

        @model_validator(mode="after")
        def validate_range(self):
            if self.range_start > self.range_end:
                raise ValueError("range_start must not exceed range_end")
            return self

    @app.get("/")
    def read_model(params: Annotated[RangeHeaders, Header()]):
        return params

    client = TestClient(app)
    response = client.get("/", headers={"range-start": "1", "range-end": "2"})
    assert response.status_code == 200
    assert response.json() == {"range_start": 1, "range_end": 2}

    response = client.get("/", headers={"range-start": "2", "range-end": "1"})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("value_error", ["header"]),
    ]


def test_header_model_extra_error_preserves_header_name():
    app = FastAPI()

    class StrictHeaders(BaseModel):
        model_config = ConfigDict(extra="forbid")
        host: str
        int_val: int

    @app.get("/")
    def read_model(params: Annotated[StrictHeaders, Header()]):
        return params.int_val

    client = TestClient(app)
    client.headers.clear()
    response = client.get("/", headers={"int-val": "1"})
    assert response.status_code == 200
    assert response.json() == 1

    response = client.get("/", headers={"int-val": "invalid", "extra_header": "value"})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("int_parsing", ["header", "int-val"]),
        ("extra_forbidden", ["header", "extra_header"]),
    ]
