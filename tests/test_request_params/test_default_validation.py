from typing import Annotated

import pytest
from fastapi import Body, Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, BeforeValidator, Field


def double(value):
    return 0 if value is None else int(value) * 2


ValidatedInt = Annotated[int | None, BeforeValidator(double)]


@pytest.mark.parametrize(
    "parameter",
    [
        pytest.param(
            parameter,
            marks=pytest.mark.xfail(
                reason="Missing values are validated as explicitly supplied defaults",
                raises=AssertionError,
            ),
        )
        for parameter in (Query, Header, Cookie, Form)
    ]
    + [Body],
)
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_missing_value_uses_default_without_validation(parameter, path):
    app = FastAPI()
    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, field] = 10):
        return value

    class Model(BaseModel):
        value: ValidatedInt = 10

    @app.post("/model")
    def read_model(value: Annotated[Model, parameter()]):
        return value.value

    client = TestClient(app)
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 200
    assert response.json() == 10


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_missing_value_uses_none_default_without_validation(parameter, path):
    app = FastAPI()
    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, field] = None):
        return value

    class Model(BaseModel):
        value: ValidatedInt = None

    @app.post("/model")
    def read_model(value: Annotated[Model, parameter()]):
        return value.value

    client = TestClient(app)
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_explicit_value_equal_to_default_is_validated(parameter, path):
    app = FastAPI()
    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, field] = 10):
        return value

    class Model(BaseModel):
        value: ValidatedInt = 10

    @app.post("/model")
    def read_model(value: Annotated[Model, parameter()]):
        return value.value

    client = TestClient(app)
    if parameter is Query:
        response = client.post(path, params={"value": "10"})
    elif parameter is Header:
        response = client.post(path, headers={"value": "10"})
    elif parameter is Cookie:
        response = client.post(path, headers={"cookie": "value=10"})
    elif parameter is Form:
        response = client.post(path, data={"value": "10"})
    else:
        response = client.post(path, json={"value": 10})
    assert response.status_code == 200
    assert response.json() == 20


@pytest.mark.parametrize("default", [None, 10])
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/parameter",
            marks=pytest.mark.xfail(
                reason="Explicit null is treated as missing for individual Body parameters",
                raises=AssertionError,
            ),
        ),
        "/model",
    ],
)
def test_explicit_null_is_validated(default, path):
    app = FastAPI()
    field = Body(embed=True)

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, field] = default):
        return value

    class Model(BaseModel):
        value: ValidatedInt = default

    @app.post("/model")
    def read_model(value: Annotated[Model, Body()]):
        return value.value

    client = TestClient(app)
    response = client.post(path, json={"value": None})
    assert response.status_code == 200
    assert response.json() == 0


@pytest.mark.parametrize("default", [None, 10])
@pytest.mark.xfail(
    reason="Explicit null-body is treated as missing", raises=AssertionError
)
def test_explicit_null_body_is_validated(default):
    app = FastAPI()

    @app.post("/")
    def read_body(value: Annotated[ValidatedInt, Body()] = default):
        return value

    client = TestClient(app)
    response = client.post(
        "/", content="null", headers={"content-type": "application/json"}
    )
    assert response.status_code == 200
    assert response.json() == 0


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("default,expected", [(None, 0), (10, 20)])
def test_model_can_validate_default(parameter, default, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[ValidatedInt, Field(validate_default=True)] = default

    @app.post("/")
    def read_model(value: Annotated[Model, parameter()]):
        return value.value

    client = TestClient(app)
    if parameter is Body:
        response = client.post("/", json={})
    else:
        response = client.post("/")
    assert response.status_code == 200
    assert response.json() == expected
