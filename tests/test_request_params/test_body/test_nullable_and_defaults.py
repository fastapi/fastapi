from typing import Annotated

import pytest
from fastapi import Body, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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
        ("/required", None),
        ("/required-model", ["value"]),
        ("/none-default", None),
        ("/none-default-model", ["value"]),
        ("/non-null-default", None),
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
        "/bare-required",
        "/bare-int-default",
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
        ("/non-nullable-default", '{"value": null}', ["body", "value"]),
        ("/non-nullable-default-model", '{"value": null}', ["body", "value"]),
        ("/bare-non-nullable-default", "null", ["body"]),
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


@pytest.mark.parametrize(
    "path",
    ["/required", "/none-default", "/non-null-default", "/non-nullable-default"],
)
def test_explicit_null_is_not_an_embedded_body_object(path):
    response = client.post(
        path, content="null", headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "value"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


def test_explicit_null_is_not_an_object_for_multiple_body_parameters():
    app = FastAPI()

    @app.post("/")
    def read_values(
        value: Annotated[int | None, Body()] = 10,
        other: Annotated[int | None, Body()] = 20,
    ):
        return {"value": value, "other": other}

    client = TestClient(app)
    response = client.post(
        "/", content="null", headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
        ("missing", ["body", "other"]),
    ]

    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"value": 10, "other": 20}

    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == {"value": 10, "other": 20}

    response = client.post("/", json={"value": None, "other": None})
    assert response.status_code == 200
    assert response.json() == {"value": None, "other": None}


@pytest.mark.parametrize(
    "embed,null_content,missing_content",
    [(False, "null", ""), (True, '{"value": null}', "{}")],
)
def test_explicit_null_does_not_call_default_factory(
    embed, null_content, missing_content
):
    app = FastAPI()
    calls = 0

    def default_factory():
        nonlocal calls
        calls += 1
        return "10"

    @app.post("/")
    def read_value(
        value: Annotated[
            int | None,
            Body(embed=embed, default_factory=default_factory, validate_default=True),
        ],
    ):
        return value

    client = TestClient(app)
    response = client.post(
        "/", content=null_content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() is None
    assert calls == 0

    response = client.post(
        "/", content=missing_content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() == 10
    assert calls == 1


def test_explicit_null_in_body_dependency_uses_alias():
    app = FastAPI()

    def dependency(value: Annotated[int | None, Body(alias="input")] = 10):
        return value

    @app.post("/")
    def read_values(
        value: Annotated[int | None, Depends(dependency)],
        other: Annotated[int, Body()] = 20,
    ):
        return {"value": value, "other": other}

    client = TestClient(app)
    response = client.post("/", json={"input": None})
    assert response.status_code == 200
    assert response.json() == {"value": None, "other": 20}

    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == {"value": 10, "other": 20}


@pytest.mark.parametrize(
    "embed,null_content,missing_content",
    [(False, "null", ""), (True, '{"params": null}', "{}")],
)
def test_explicit_null_for_nullable_model_body(embed, null_content, missing_content):
    app = FastAPI()

    @app.post("/")
    def read_model(
        params: Annotated[RequiredModel | None, Body(embed=embed)] = RequiredModel(
            value=10
        ),
    ):
        return params

    client = TestClient(app)
    response = client.post(
        "/", content=null_content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() is None

    response = client.post(
        "/", content=missing_content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() == {"value": 10}


@pytest.mark.parametrize("content,error_type", [("", "missing"), ("null", "int_type")])
def test_validation_error_body_for_missing_and_null(content, error_type):
    app = FastAPI()

    @app.post("/")
    def read_value(value: Annotated[int, Body()]):
        return value

    @app.exception_handler(RequestValidationError)
    def handle_error(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422, content={"body": exc.body, "detail": exc.errors()}
        )

    client = TestClient(app)
    response = client.post("/", json=1)
    assert response.status_code == 200
    assert response.json() == 1

    response = client.post(
        "/", content=content, headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert response.json()["body"] is None
    assert [
        (error["type"], error["loc"], error["input"])
        for error in response.json()["detail"]
    ] == [(error_type, ["body"], None)]
