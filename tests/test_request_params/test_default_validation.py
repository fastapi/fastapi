from typing import Annotated

import pytest
from fastapi import Body, Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, BeforeValidator, Field


def double(value):
    return 0 if value is None else int(value) * 2


ValidatedInt = Annotated[int | None, BeforeValidator(double)]


def make_client(parameter, default=10):
    app = FastAPI()
    field = parameter(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, field] = default):
        return value

    class Model(BaseModel):
        value: ValidatedInt = default

    @app.post("/model")
    def read_model(value: Annotated[Model, parameter()]):
        return value.value

    return TestClient(app)


@pytest.mark.parametrize(
    "parameter",
    [
        pytest.param(
            parameter,
            marks=pytest.mark.xfail(
                reason="Missing values are validated as explicitly supplied defaults"
            ),
        )
        for parameter in (Query, Header, Cookie, Form)
    ]
    + [Body],
)
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_missing_value_uses_default_without_validation(parameter, path):
    client = make_client(parameter)
    response = client.post(path, **({"json": {}} if parameter is Body else {}))
    assert response.status_code == 200
    assert response.json() == 10


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_missing_value_uses_none_default_without_validation(parameter, path):
    client = make_client(parameter, default=None)
    response = client.post(path, **({"json": {}} if parameter is Body else {}))
    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_explicit_value_equal_to_default_is_validated(parameter, path):
    client = make_client(parameter)
    kwargs = {
        Query: {"params": {"value": "10"}},
        Header: {"headers": {"value": "10"}},
        Cookie: {"headers": {"cookie": "value=10"}},
        Form: {"data": {"value": "10"}},
        Body: {"json": {"value": 10}},
    }[parameter]
    response = client.post(path, **kwargs)
    assert response.status_code == 200
    assert response.json() == 20


@pytest.mark.parametrize("default", [None, 10])
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/parameter",
            marks=pytest.mark.xfail(
                reason="Explicit null is treated as missing for individual Body parameters"
            ),
        ),
        "/model",
    ],
)
def test_explicit_null_is_validated(default, path):
    client = make_client(Body, default=default)
    response = client.post(path, json={"value": None})
    assert response.status_code == 200
    assert response.json() == 0


@pytest.mark.parametrize("default", [None, 10])
@pytest.mark.xfail(reason="Explicit null-body is treated as missing")
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


def test_model_can_validate_default():
    app = FastAPI()

    class Model(BaseModel):
        value: ValidatedInt = Field(10, validate_default=True)

    @app.post("/")
    def read_model(value: Model):
        return value.value

    client = TestClient(app)
    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == 20
