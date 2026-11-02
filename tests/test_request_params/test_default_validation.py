from typing import Annotated
from unittest.mock import Mock

import pytest
from fastapi import Body, Cookie, FastAPI, File, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, BeforeValidator, Field


def double(value):
    return 0 if value is None else int(value) * 2


ValidatedInt = Annotated[int | None, BeforeValidator(double)]


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
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
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_explicit_null_is_validated(default, path):
    app = FastAPI()

    @app.post("/parameter")
    def read_parameter(value: Annotated[ValidatedInt, Body(embed=True)] = default):
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


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("default,expected", [(None, 0), (10, 20)])
def test_parameter_can_validate_default(parameter, default, expected):
    app = FastAPI()
    field = (
        Body(embed=True, validate_default=True)
        if parameter is Body
        else parameter(validate_default=True)
    )

    @app.post("/")
    def read_parameter(value: Annotated[ValidatedInt, field] = default):
        return value

    client = TestClient(app)
    if parameter is Body:
        response = client.post("/", json={})
    else:
        response = client.post("/")
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("default,expected", [(None, 0), (10, 20)])
def test_parameter_validates_default_factory_once(parameter, default, expected):
    app = FastAPI()
    default_factory = Mock(return_value=default)
    field = (
        Body(embed=True, default_factory=default_factory, validate_default=True)
        if parameter is Body
        else parameter(default_factory=default_factory, validate_default=True)
    )

    @app.post("/")
    def read_parameter(value: Annotated[ValidatedInt, field]):
        return value

    default_factory.assert_not_called()
    client = TestClient(app)
    if parameter is Body:
        response = client.post("/", json={})
    else:
        response = client.post("/")
    assert response.status_code == 200
    assert response.json() == expected
    default_factory.assert_called_once_with()


def test_parameter_preserves_pydantic_default_factory():
    app = FastAPI()
    default_factory = Mock(return_value=5)

    @app.get("/")
    def read_parameter(
        value: Annotated[int, Field(default_factory=default_factory), Query()],
    ):
        return value

    default_factory.assert_not_called()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 5
    default_factory.assert_called_once_with()

    response = client.get("/", params={"value": "10"})
    assert response.status_code == 200
    assert response.json() == 10
    default_factory.assert_called_once_with()


@pytest.mark.parametrize(
    "field,expected", [(Query(), 20), (Query(validate_default=False), 10)]
)
def test_parameter_preserves_pydantic_validate_default(field, expected):
    app = FastAPI()

    @app.get("/")
    def read_parameter(
        value: Annotated[ValidatedInt, Field(validate_default=True), field] = 10,
    ):
        return value

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == expected


def test_inferred_parameter_preserves_pydantic_default_factory():
    app = FastAPI()
    default_factory = Mock(return_value=5)

    @app.get("/")
    def read_parameter(value: Annotated[int, Field(default_factory=default_factory)]):
        return value

    default_factory.assert_not_called()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == 5
    default_factory.assert_called_once_with()

    response = client.get("/", params={"value": "10"})
    assert response.status_code == 200
    assert response.json() == 10
    default_factory.assert_called_once_with()


def test_inferred_parameters_validate_defaults():
    app = FastAPI()

    @app.post("/")
    def read_parameters(
        values: Annotated[
            list[int], Field(default_factory=list, min_length=1, validate_default=True)
        ],
        count: Annotated[int, Field(gt=0, validate_default=True)] = -1,
    ):
        return {"count": count, "values": values}

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["query", "count"],
                "msg": "Input should be greater than 0",
                "input": -1,
                "ctx": {"gt": 0},
            },
            {
                "type": "too_short",
                "loc": ["body"],
                "msg": "List should have at least 1 item after validation, not 0",
                "input": [],
                "ctx": {"field_type": "List", "min_length": 1, "actual_length": 0},
            },
        ]
    }

    response = client.post("/", params={"count": "2"}, json=[1, 2])
    assert response.status_code == 200
    assert response.json() == {"count": 2, "values": [1, 2]}


def test_parameter_rejects_invalid_default():
    app = FastAPI()

    @app.get("/")
    def read_parameter(value: Annotated[int, Query(gt=0, validate_default=True)] = -1):
        return value

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["query", "value"],
                "msg": "Input should be greater than 0",
                "input": -1,
                "ctx": {"gt": 0},
            }
        ]
    }
    response = client.get("/", params={"value": "1"})
    assert response.status_code == 200
    assert response.json() == 1


@pytest.mark.parametrize(
    "validate_default,expected_status,expected",
    [
        (False, 200, "x"),
        (
            True,
            422,
            {
                "detail": [
                    {
                        "type": "bytes_too_short",
                        "loc": ["body", "value"],
                        "msg": "Data should have at least 2 bytes",
                        "input": "x",
                        "ctx": {"min_length": 2},
                    }
                ]
            },
        ),
    ],
)
def test_file_parameter_can_validate_default(
    validate_default, expected_status, expected
):
    app = FastAPI()

    @app.post("/")
    def read_file(
        value: Annotated[
            bytes, File(min_length=2, validate_default=validate_default)
        ] = b"x",
    ):
        return value

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == expected_status
    assert response.json() == expected
