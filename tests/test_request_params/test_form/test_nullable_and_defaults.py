from typing import Annotated

import pytest
from fastapi import Body, FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError


@pytest.mark.parametrize(
    "path",
    [
        "/parameter",
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="Empty scalar form strings are not treated as missing in models",
                raises=AssertionError,
            ),
        ),
    ],
)
@pytest.mark.parametrize("default", [None, "default"])
@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_empty_string_uses_default(path, default, encoding):
    app = FastAPI()

    class Model(BaseModel):
        value: str | None = default

    @app.post("/parameter")
    def read_parameter(value: Annotated[str | None, Form()] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": "hello"})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == "hello"
    if encoding == "urlencoded":
        response = client.post(path, data={"value": ""})
    else:
        response = client.post(path, files={"value": (None, "")})
    assert response.status_code == 200
    assert response.json() == {
        "value": default,
        "fields_set": [] if path == "/model" else None,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/parameter",
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="Empty scalar form strings are not treated as missing in models",
                raises=AssertionError,
            ),
        ),
    ],
)
@pytest.mark.parametrize("default", [None, 10])
@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_empty_integer_uses_default(path, default, encoding):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None = default

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, Form()] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": "1"})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 1
    if encoding == "urlencoded":
        response = client.post(path, data={"value": ""})
    else:
        response = client.post(path, files={"value": (None, "")})
    assert response.status_code == 200
    assert response.json() == {
        "value": default,
        "fields_set": [] if path == "/model" else None,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/parameter",
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="Empty required scalar form strings are not treated as missing in models",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_empty_required_string_is_missing(path):
    app = FastAPI()

    class Model(BaseModel):
        value: str | None

    @app.post("/parameter")
    def read_parameter(value: Annotated[str | None, Form()]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": "hello"})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == "hello"
    response = client.post(path, data={"value": ""})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
    ]


@pytest.mark.parametrize(
    "path",
    [
        "/parameter",
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="Empty required scalar form strings are not treated as missing in models",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_empty_required_integer_is_missing(path):
    app = FastAPI()

    class Model(BaseModel):
        value: int | None

    @app.post("/parameter")
    def read_parameter(value: Annotated[int | None, Form()]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": "1"})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == 1
    response = client.post(path, data={"value": ""})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
    ]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("values", [[""], ["", "hello"]])
def test_empty_required_string_list_item_is_preserved(path, values):
    app = FastAPI()

    class Model(BaseModel):
        value: list[str] | None

    @app.post("/parameter")
    def read_required(value: Annotated[list[str] | None, Form()]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    response = client.post(path, data={"value": values})
    assert response.status_code == 200
    assert response.json() == {
        "value": values,
        "fields_set": ["value"] if path == "/model" else None,
    }


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("default", [None, ["default"]])
@pytest.mark.parametrize("values", [[""], ["", "hello"]])
def test_empty_defaulted_string_list_item_is_preserved(path, default, values):
    app = FastAPI()

    class Model(BaseModel):
        value: list[str] | None = default

    @app.post("/parameter")
    def read_defaulted(value: Annotated[list[str] | None, Form()] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    response = client.post(path, data={"value": values})
    assert response.status_code == 200
    assert response.json() == {
        "value": values,
        "fields_set": ["value"] if path == "/model" else None,
    }


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_empty_required_integer_list_item_fails_validation(path):
    app = FastAPI()

    class Model(BaseModel):
        value: list[int] | None

    @app.post("/parameter")
    def read_required(value: Annotated[list[int] | None, Form()]):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": ["1", "2"]})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == [1, 2]
    response = client.post(path, data={"value": ""})
    assert response.status_code == 422
    assert [
        (error["type"], error["loc"], error["input"])
        for error in response.json()["detail"]
    ] == [
        ("int_parsing", ["body", "value", 0], ""),
    ]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("default", [None, [10]])
def test_empty_defaulted_integer_list_item_fails_validation(path, default):
    app = FastAPI()

    class Model(BaseModel):
        value: list[int] | None = default

    @app.post("/parameter")
    def read_defaulted(value: Annotated[list[int] | None, Form()] = default):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    supplied = client.post(path, data={"value": ["1", "2"]})
    assert supplied.status_code == 200
    assert supplied.json()["value"] == [1, 2]
    response = client.post(path, data={"value": ""})
    assert response.status_code == 422
    assert [
        (error["type"], error["loc"], error["input"])
        for error in response.json()["detail"]
    ] == [
        ("int_parsing", ["body", "value", 0], ""),
    ]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_checked_checkbox_is_true(path):
    app = FastAPI()

    class Model(BaseModel):
        value: bool

    @app.post("/parameter")
    def read_parameter(value: Annotated[bool, Form()]):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data={"value": "on"})
    assert response.status_code == 200
    assert response.json() == {"value": True}


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/parameter",
            marks=pytest.mark.xfail(
                reason="An omitted boolean form field is treated as missing instead of False",
                raises=AssertionError,
            ),
        ),
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="An omitted boolean form field is treated as missing instead of False",
                raises=AssertionError,
            ),
        ),
        "/parameter-default",
        "/model-default",
    ],
)
def test_unchecked_checkbox_is_false(path):
    app = FastAPI()

    class Model(BaseModel):
        value: bool

    @app.post("/parameter")
    def read_parameter(value: Annotated[bool, Form()]):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    class ModelWithDefault(BaseModel):
        value: bool = False

    @app.post("/parameter-default")
    def read_parameter_default(value: Annotated[bool, Form()] = False):
        return {"value": value}

    @app.post("/model-default")
    def read_model_default(params: Annotated[ModelWithDefault, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    checked = client.post(path, data={"value": "on"})
    assert checked.status_code == 200
    assert checked.json() == {"value": True}
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"value": False}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        pytest.param({"value": "on"}, True, id="checked"),
        pytest.param(
            {},
            False,
            id="unchecked",
            marks=pytest.mark.xfail(
                reason="An omitted boolean form field uses its True default instead of False",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_checkbox_with_true_default(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: bool = True

    @app.post("/parameter")
    def read_parameter(value: Annotated[bool, Form()] = True):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        pytest.param({"value": "on"}, True, id="checked"),
        pytest.param(
            {},
            False,
            id="unchecked",
            marks=pytest.mark.xfail(
                reason="An omitted nullable boolean form field is treated as missing instead of False",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_required_nullable_checkbox(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: bool | None

    @app.post("/parameter")
    def read_parameter(value: Annotated[bool | None, Form()]):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        pytest.param({"value": "on"}, True, id="checked"),
        pytest.param(
            {},
            False,
            id="unchecked",
            marks=pytest.mark.xfail(
                reason="An omitted nullable boolean form field uses its None default instead of False",
                raises=AssertionError,
            ),
        ),
    ],
)
def test_nullable_checkbox_with_none_default(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: bool | None = None

    @app.post("/parameter")
    def read_parameter(value: Annotated[bool | None, Form()] = None):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize(
    "data,expected",
    [
        pytest.param({"value": "on"}, True, id="checked"),
        pytest.param({}, False, id="unchecked"),
    ],
)
def test_checkbox_with_false_default_is_explicitly_set(data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: bool = False

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "fields_set": sorted(params.model_fields_set),
            "values": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert response.json() == {"fields_set": ["value"], "values": {"value": expected}}


def test_form_does_not_change_required_model_fields():
    app = FastAPI()

    class Model(BaseModel):
        value: bool

    @app.post("/form")
    def read_form(params: Annotated[Model, Form()]):
        return params.model_dump()

    @app.post("/json")
    def read_json(params: Annotated[Model, Body()]):
        return params.model_dump()

    client = TestClient(app)
    response = client.post("/form", data={"value": "on"})
    assert response.status_code == 200
    assert response.json() == {"value": True}

    # Exercise omitted-checkbox handling; its response is tested separately.
    client.post("/form")

    assert Model.model_fields["value"].is_required()
    with pytest.raises(ValidationError) as exc_info:
        Model.model_validate({})
    assert [(error["type"], error["loc"]) for error in exc_info.value.errors()] == [
        ("missing", ("value",)),
    ]

    response = client.post("/json", json={})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
    ]

    response = client.post("/json", json={"value": False})
    assert response.status_code == 200
    assert response.json() == {"value": False}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_whitespace_string_is_not_missing(path):
    app = FastAPI()

    class Model(BaseModel):
        value: str | None = "default"

    @app.post("/parameter")
    def read_parameter(value: Annotated[str | None, Form()] = "default"):
        return {"value": value, "fields_set": None}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return {"value": params.value, "fields_set": sorted(params.model_fields_set)}

    client = TestClient(app)
    response = client.post(path, data={"value": " "})
    assert response.status_code == 200
    assert response.json() == {
        "value": " ",
        "fields_set": ["value"] if path == "/model" else None,
    }
