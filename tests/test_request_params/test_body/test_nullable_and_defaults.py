from typing import Annotated

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class RequiredModel(BaseModel):
    value: int | None


class NoneDefaultModel(BaseModel):
    value: int | None = None


class NonNullDefaultModel(BaseModel):
    value: int | None = 10


class NonNullableDefaultModel(BaseModel):
    value: int = 10


@app.post("/required")
def read_required(value: Annotated[int | None, Body(embed=True)]):
    return {"value": value, "fields_set": None}


@app.post("/required-model")
def read_required_model(params: Annotated[RequiredModel, Body()]):
    return {"value": params.value, "fields_set": sorted(params.model_fields_set)}


@app.post("/none-default")
def read_none_default(value: Annotated[int | None, Body(embed=True)] = None):
    return {"value": value, "fields_set": None}


@app.post("/none-default-model")
def read_none_default_model(params: Annotated[NoneDefaultModel, Body()]):
    return {"value": params.value, "fields_set": sorted(params.model_fields_set)}


@app.post("/non-null-default")
def read_non_null_default(value: Annotated[int | None, Body(embed=True)] = 10):
    return {"value": value, "fields_set": None}


@app.post("/non-null-default-model")
def read_non_null_default_model(params: Annotated[NonNullDefaultModel, Body()]):
    return {"value": params.value, "fields_set": sorted(params.model_fields_set)}


@app.post("/non-nullable-default")
def read_non_nullable_default(value: Annotated[int, Body(embed=True)] = 10):
    return {"value": value, "fields_set": None}


@app.post("/non-nullable-default-model")
def read_non_nullable_default_model(params: Annotated[NonNullableDefaultModel, Body()]):
    return {"value": params.value, "fields_set": sorted(params.model_fields_set)}


@app.post("/bare-required")
def read_bare_required(value: Annotated[int | None, Body()]):
    return value


@app.post("/bare-none-default")
def read_bare_none_default(value: Annotated[int | None, Body()] = None):
    return value


@app.post("/bare-int-default")
def read_bare_int_default(value: Annotated[int | None, Body()] = 10):
    return value


@app.post("/bare-non-nullable-default")
def read_bare_non_nullable_default(value: Annotated[int, Body()] = 10):
    return value


@app.post("/bare-str-default")
def read_bare_str_default(value: Annotated[str | None, Body()] = "default"):
    return value


@app.post("/bare-list-default")
def read_bare_list_default(
    value: Annotated[list[int] | None, Body(default_factory=lambda: [10])],
):
    return value


client = TestClient(app)


@pytest.mark.parametrize(
    "path,fields_set",
    [
        pytest.param(
            "/required",
            None,
            marks=pytest.mark.xfail(
                reason="Explicit null is treated as missing for a required Body parameter",
                raises=AssertionError,
            ),
        ),
        ("/required-model", ["value"]),
        ("/none-default", None),
        ("/none-default-model", ["value"]),
        pytest.param(
            "/non-null-default",
            None,
            marks=pytest.mark.xfail(
                reason="Explicit null is replaced with the Body parameter default",
                raises=AssertionError,
            ),
        ),
        ("/non-null-default-model", ["value"]),
    ],
)
def test_explicit_null(path, fields_set):
    supplied = client.post(path, json={"value": 0})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 0
    response = client.post(path, json={"value": None})
    assert response.status_code == 200
    assert response.json() == {"value": None, "fields_set": fields_set}


@pytest.mark.parametrize(
    "path,location",
    [
        ("/required", ["body", "value"]),
        ("/required-model", ["body"]),
        ("/none-default-model", ["body"]),
        ("/non-null-default-model", ["body"]),
    ],
)
def test_absent_body_for_required_argument(path, location):
    # A model argument is required even when its fields have defaults.
    response = client.post(path)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", location),
    ]


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/none-default", None),
        ("/non-null-default", 10),
        ("/non-nullable-default", 10),
    ],
)
def test_absent_body_uses_parameter_default(path, expected):
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"value": expected, "fields_set": None}


def test_absent_required_bare_body():
    supplied = client.post("/bare-required", json=0)
    assert supplied.status_code == 200
    assert supplied.json() == 0
    response = client.post("/bare-required")
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/bare-none-default", None),
        ("/bare-int-default", 10),
        ("/bare-non-nullable-default", 10),
    ],
)
def test_absent_bare_body_uses_default(path, expected):
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    "path",
    [
        "/bare-none-default",
        pytest.param(
            "/bare-required",
            marks=pytest.mark.xfail(
                reason="Explicit null-body is treated as missing", raises=AssertionError
            ),
        ),
        pytest.param(
            "/bare-int-default",
            marks=pytest.mark.xfail(
                reason="Explicit null-body is replaced with the default",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_explicit_null_bare_body(path):
    response = client.post(
        path, content="null", headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.parametrize(
    "path,value",
    [("/bare-int-default", 0), ("/bare-str-default", ""), ("/bare-list-default", [])],
)
def test_falsey_bare_body_is_not_missing(path, value):
    response = client.post(path, json=value)
    assert response.status_code == 200
    assert response.json() == value


@pytest.mark.parametrize(
    "path,error_type",
    [
        ("/bare-int-default", "int_type"),
        ("/bare-str-default", "string_type"),
        ("/bare-list-default", "list_type"),
    ],
)
def test_object_is_not_a_valid_nullable_scalar_or_list(path, error_type):
    response = client.post(path, json={})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["body"]),
    ]


@pytest.mark.parametrize(
    "path", ["/non-nullable-default", "/non-nullable-default-model"]
)
def test_omitted_non_nullable_field_uses_default(path):
    response = client.post(path, json={})
    assert response.status_code == 200
    assert response.json()["value"] == 10


@pytest.mark.parametrize(
    "path,content,location",
    [
        pytest.param(
            "/non-nullable-default",
            '{"value": null}',
            ["body", "value"],
            marks=pytest.mark.xfail(
                reason="Explicit null is replaced with the Body parameter default",
                raises=AssertionError,
            ),
        ),
        ("/non-nullable-default-model", '{"value": null}', ["body", "value"]),
        pytest.param(
            "/bare-non-nullable-default",
            "null",
            ["body"],
            marks=pytest.mark.xfail(
                reason="Explicit null-body is replaced with the default",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_explicit_null_for_non_nullable_body_with_default(path, content, location):
    response = client.post(
        path, content=content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert [
        (error["type"], error["loc"], error["input"])
        for error in response.json()["detail"]
    ] == [
        ("int_type", location, None),
    ]
