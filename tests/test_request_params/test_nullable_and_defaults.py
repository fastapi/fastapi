from typing import Annotated
from unittest.mock import Mock

import pytest
from fastapi import Body, Cookie, FastAPI, Form, Header, Query
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


@pytest.fixture(params=[Query, Header, Cookie, Form, Body])
def parameter(request):
    return request.param


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_nullable_required_schema_and_supplied_value(parameter, path):
    app = FastAPI()

    field = Body(embed=True) if parameter is Body else parameter()

    class Model(BaseModel):
        value: int | None

    @app.post("/parameter")
    def read_required(value: Annotated[int | None, field]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        supplied = client.post(path, params={"value": "0"})
    elif parameter is Header:
        supplied = client.post(path, headers={"value": "0"})
    elif parameter is Cookie:
        supplied = client.post(path, headers={"cookie": "value=0"})
    elif parameter is Form:
        supplied = client.post(path, data={"value": "0"})
    else:
        supplied = client.post(path, json={"value": 0})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 0
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"][path]["post"]
    if parameter in (Query, Header, Cookie):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert schema["anyOf"] == [{"type": "integer"}, {"type": "null"}]
    assert required is True
    assert "default" not in schema


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_nullable_none_default_schema_and_supplied_value(parameter, path):
    app = FastAPI()

    field = Body(embed=True) if parameter is Body else parameter()

    class Model(BaseModel):
        value: int | None = None

    @app.post("/parameter")
    def read_defaulted(value: Annotated[int | None, field] = None):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        supplied = client.post(path, params={"value": "0"})
    elif parameter is Header:
        supplied = client.post(path, headers={"value": "0"})
    elif parameter is Cookie:
        supplied = client.post(path, headers={"cookie": "value=0"})
    elif parameter is Form:
        supplied = client.post(path, data={"value": "0"})
    else:
        supplied = client.post(path, json={"value": 0})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 0
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"][path]["post"]
    if parameter in (Query, Header, Cookie):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert schema["anyOf"] == [{"type": "integer"}, {"type": "null"}]
    assert required is False
    assert "default" not in schema


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_nullable_non_null_default_schema_and_supplied_value(parameter, path):
    app = FastAPI()

    field = Body(embed=True) if parameter is Body else parameter()

    class Model(BaseModel):
        value: int | None = 10

    @app.post("/parameter")
    def read_defaulted(value: Annotated[int | None, field] = 10):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        supplied = client.post(path, params={"value": "0"})
    elif parameter is Header:
        supplied = client.post(path, headers={"value": "0"})
    elif parameter is Cookie:
        supplied = client.post(path, headers={"cookie": "value=0"})
    elif parameter is Form:
        supplied = client.post(path, data={"value": "0"})
    else:
        supplied = client.post(path, json={"value": 0})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 0
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"][path]["post"]
    if parameter in (Query, Header, Cookie):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert schema["anyOf"] == [{"type": "integer"}, {"type": "null"}]
    assert required is False
    assert schema["default"] == 10


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_nullable_scalar_is_required(parameter, path):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None

    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, field]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        supplied = client.post(path, params={"value": "0"})
    elif parameter is Header:
        supplied = client.post(path, headers={"value": "0"})
    elif parameter is Cookie:
        supplied = client.post(path, headers={"cookie": "value=0"})
    elif parameter is Form:
        supplied = client.post(path, data={"value": "0"})
    else:
        supplied = client.post(path, json={"value": 0})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 0
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (
            "missing",
            ["body" if parameter in (Body, Form) else parameter().in_.value, "value"],
        )
    ]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("parameter", [Query, Header, Form, Body])
def test_nullable_list_is_required(parameter, path):
    app = FastAPI()

    class Model(BaseModel):
        value: list[int] | None

    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[list[int] | None, field]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        supplied = client.post(path, params={"value": "0"})
    elif parameter is Header:
        supplied = client.post(path, headers={"value": "0"})
    elif parameter is Form:
        supplied = client.post(path, data={"value": "0"})
    else:
        supplied = client.post(path, json={"value": [0]})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == [0]
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (
            "missing",
            ["body" if parameter in (Body, Form) else parameter().in_.value, "value"],
        )
    ]

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"][path]["post"]
    if parameter in (Query, Header):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert required is True
    assert schema["anyOf"] == [
        {"type": "array", "items": {"type": "integer"}},
        {"type": "null"},
    ]
    assert "default" not in schema


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("default", [None, 10])
def test_missing_value_uses_default(parameter, path, default):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None = default

    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, field] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 200
    assert response.json()["value"] == default


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
def test_missing_none_default_is_unset(parameter):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None = None

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Body:
        response = client.post("/model", json={})
    else:
        response = client.post("/model")
    assert response.status_code == 200
    assert response.json() == {"value": None, "fields_set": []}


@pytest.mark.parametrize(
    "parameter,annotation,default",
    [
        (Query, int | None, 10),
        (Header, int | None, 10),
        (Cookie, int | None, 10),
        (Form, int | None, 10),
        (Body, int | None, 10),
        (Query, list[int] | None, [10]),
        (Header, list[int] | None, [10]),
        (Form, list[int] | None, [10]),
        (Body, list[int] | None, [10]),
    ],
)
def test_missing_non_null_default_is_unset(parameter, annotation, default):
    app = FastAPI()

    class Model(BaseModel):
        value: annotation = default

    @app.post("/")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Body:
        response = client.post("/", json={})
    else:
        response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"value": default, "fields_set": []}


@pytest.mark.parametrize(
    "parameter,annotation,default",
    [
        (Query, int | None, 10),
        (Header, int | None, 10),
        (Cookie, int | None, 10),
        (Form, int | None, 10),
        (Body, int | None, 10),
        (Query, list[int] | None, [10]),
        (Header, list[int] | None, [10]),
        (Form, list[int] | None, [10]),
        (Body, list[int] | None, [10]),
    ],
)
def test_missing_factory_default_is_unset(parameter, annotation, default):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[annotation, Field(default_factory=lambda: default)]

    @app.post("/")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Body:
        response = client.post("/", json={})
    else:
        response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"value": default, "fields_set": []}


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("default", [None, 10])
def test_missing_value_calls_default_factory_once(parameter, path, default):
    app = FastAPI()
    default_factory = Mock(return_value=default)
    field = (
        Body(embed=True, default_factory=default_factory)
        if parameter is Body
        else parameter(default_factory=default_factory)
    )

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, field]):
        return value

    class Model(BaseModel):
        value: Annotated[int | None, Field(default_factory=default_factory)]

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return params.value

    default_factory.assert_not_called()
    client = TestClient(app)
    if parameter is Body:
        response = client.post(path, json={})
    else:
        response = client.post(path)
    assert response.status_code == 200
    assert response.json() == default
    default_factory.assert_called_once_with()


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 10),
    reason="Default factories receiving validated data require Pydantic 2.10",
)
def test_model_default_factory_receives_validated_data(parameter):
    app = FastAPI()

    class Model(BaseModel):
        value: int
        doubled: Annotated[int, Field(default_factory=lambda data: data["value"] * 2)]

    @app.post("/")
    def read_model(params: Annotated[Model, parameter()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    if parameter is Query:
        response = client.post("/", params={"value": "5"})
    elif parameter is Header:
        response = client.post("/", headers={"value": "5"})
    elif parameter is Cookie:
        response = client.post("/", headers={"cookie": "value=5"})
    elif parameter is Form:
        response = client.post("/", data={"value": "5"})
    else:
        response = client.post("/", json={"value": 5})
    assert response.status_code == 200
    assert response.json() == {
        "values": {"value": 5, "doubled": 10},
        "supplied": {"value": 5},
    }


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_supplied_value_does_not_call_default_factory(parameter, path):
    app = FastAPI()
    default_factory = Mock(return_value=10)
    field = (
        Body(embed=True, default_factory=default_factory)
        if parameter is Body
        else parameter(default_factory=default_factory)
    )

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, field]):
        return value

    class Model(BaseModel):
        value: Annotated[int | None, Field(default_factory=default_factory)]

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return params.value

    client = TestClient(app)
    if parameter is Query:
        response = client.post(path, params={"value": "0"})
    elif parameter is Header:
        response = client.post(path, headers={"value": "0"})
    elif parameter is Cookie:
        response = client.post(path, headers={"cookie": "value=0"})
    elif parameter is Form:
        response = client.post(path, data={"value": "0"})
    else:
        response = client.post(path, json={"value": 0})
    assert response.status_code == 200
    assert response.json() == 0
    default_factory.assert_not_called()


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
def test_value_equal_to_default_is_explicitly_set(parameter):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None = 0

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        response = client.post("/model", params={"value": "0"})
    elif parameter is Header:
        response = client.post("/model", headers={"value": "0"})
    elif parameter is Cookie:
        response = client.post("/model", headers={"cookie": "value=0"})
    elif parameter is Form:
        response = client.post("/model", data={"value": "0"})
    else:
        response = client.post("/model", json={"value": 0})
    assert response.status_code == 200
    assert response.json() == {"value": 0, "fields_set": ["value"]}


@pytest.mark.parametrize("parameter", [Query, Header, Cookie, Form, Body])
def test_partial_model_submission(parameter):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None = None
        omitted: int | None = 10

    @app.post("/")
    def read_model(params: Annotated[Model, parameter()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    if parameter is Query:
        response = client.post("/", params={"value": "0"})
    elif parameter is Header:
        response = client.post("/", headers={"value": "0"})
    elif parameter is Cookie:
        response = client.post("/", headers={"cookie": "value=0"})
    elif parameter is Form:
        response = client.post("/", data={"value": "0"})
    else:
        response = client.post("/", json={"value": 0})
    assert response.status_code == 200
    assert response.json() == {"value": 0}


@pytest.mark.parametrize("parameter", [Query, Header, Form, Body])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "default,expected_schema",
    [
        pytest.param(
            None,
            {
                "title": "Value",
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
            },
            id="none-default",
        ),
        pytest.param(
            [10],
            {
                "title": "Value",
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "default": [10],
            },
            id="non-null-default",
        ),
    ],
)
def test_nullable_list_default_and_repeated_values(
    parameter, path, default, expected_schema
):
    app = FastAPI()

    class Model(BaseModel):
        value: list[int] | None = default

    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/parameter")
    def read_parameter(value: Annotated[list[int] | None, field] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Body:
        missing = client.post(path, json={})
    else:
        missing = client.post(path)
    assert missing.status_code == 200
    assert missing.json()["value"] == default
    if parameter is Query:
        supplied = client.post(path, params={"value": ["0", "1"]})
    elif parameter is Header:
        supplied = client.post(path, headers=[("value", "0"), ("value", "1")])
    elif parameter is Form:
        supplied = client.post(path, data={"value": ["0", "1"]})
    else:
        supplied = client.post(path, json={"value": [0, 1]})
    assert supplied.status_code == 200
    assert supplied.json() == {
        "value": [0, 1],
        "fields_set": ["value"] if path == "/model" else None,
    }

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"][path]["post"]
    if parameter in (Query, Header):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert required is False
    assert schema == expected_schema


@pytest.mark.parametrize("parameter", [Query, Header, Cookie])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "default,expected_schema",
    [
        (
            None,
            {"title": "Value", "anyOf": [{"type": "string"}, {"type": "null"}]},
        ),
        (
            "default",
            {
                "title": "Value",
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "default": "default",
            },
        ),
    ],
)
def test_empty_non_form_string_is_supplied(parameter, path, default, expected_schema):
    app = FastAPI()

    class Model(BaseModel):
        value: str | None = default

    @app.post("/parameter")
    def read_parameter(value: Annotated[str | None, parameter()] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    if parameter is Query:
        response = client.post(path, params={"value": ""})
    elif parameter is Header:
        response = client.post(path, headers={"value": ""})
    else:
        response = client.post(path, headers={"cookie": "value="})
    assert response.status_code == 200
    assert response.json() == {
        "value": "",
        "fields_set": ["value"] if path == "/model" else None,
    }

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    field = response.json()["paths"][path]["post"]["parameters"][0]
    assert field["required"] is False
    assert field["schema"] == expected_schema


@pytest.mark.parametrize("parameter", [Query, Header, Cookie])
@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_empty_required_non_form_string_is_supplied(parameter, path):
    app = FastAPI()

    class Model(BaseModel):
        value: str | None

    @app.post("/parameter")
    def read_parameter(value: Annotated[str | None, parameter()]):
        return value

    @app.post("/model")
    def read_model(params: Annotated[Model, parameter()]):
        return params.value

    client = TestClient(app)
    if parameter is Query:
        response = client.post(path, params={"value": ""})
    elif parameter is Header:
        response = client.post(path, headers={"value": ""})
    else:
        response = client.post(path, headers={"cookie": "value="})
    assert response.status_code == 200
    assert response.json() == ""
    missing = client.post(path)
    assert missing.status_code == 422
    assert [(error["type"], error["loc"]) for error in missing.json()["detail"]] == [
        ("missing", [parameter().in_.value, "value"]),
    ]
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    field = response.json()["paths"][path]["post"]["parameters"][0]
    assert field["required"] is True
    assert field["schema"] == {
        "title": "Value",
        "anyOf": [{"type": "string"}, {"type": "null"}],
    }


@pytest.mark.parametrize("parameter", [Query, Header, Form, Body])
def test_nullable_list_parameter_default_factory(parameter):
    app = FastAPI()
    field = (
        Body(embed=True, default_factory=lambda: [10])
        if parameter is Body
        else parameter(default_factory=lambda: [10])
    )

    @app.post("/")
    def read_parameter(value: Annotated[list[int] | None, field]):
        return value

    client = TestClient(app)
    missing = client.post("/")
    assert missing.status_code == 200
    assert missing.json() == [10]
    if parameter is Query:
        supplied = client.post("/", params={"value": ["0", "1"]})
    elif parameter is Header:
        supplied = client.post("/", headers=[("value", "0"), ("value", "1")])
    elif parameter is Form:
        supplied = client.post("/", data={"value": ["0", "1"]})
    else:
        supplied = client.post("/", json={"value": [0, 1]})
    assert supplied.status_code == 200
    assert supplied.json() == [0, 1]

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    openapi = response.json()
    operation = openapi["paths"]["/"]["post"]
    if parameter in (Query, Header):
        field = operation["parameters"][0]
        schema = field["schema"]
        required = field["required"]
    else:
        media_type = (
            "application/json"
            if parameter is Body
            else "application/x-www-form-urlencoded"
        )
        reference = operation["requestBody"]["content"][media_type]["schema"]["$ref"]
        model = openapi["components"]["schemas"][reference.rsplit("/", 1)[1]]
        schema = model["properties"]["value"]
        required = "value" in model.get("required", [])
    assert required is False
    assert schema["anyOf"] == [
        {"type": "array", "items": {"type": "integer"}},
        {"type": "null"},
    ]
    assert "default" not in schema
