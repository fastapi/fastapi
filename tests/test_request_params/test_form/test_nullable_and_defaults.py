from typing import Annotated
from unittest.mock import Mock

import pytest
from fastapi import Body, FastAPI, Form
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from pydantic import (
    AfterValidator,
    AliasChoices,
    AliasPath,
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
)


@pytest.mark.parametrize("path", ["/parameter", "/model"])
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


@pytest.mark.parametrize("path", ["/parameter", "/model"])
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


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
@pytest.mark.parametrize("annotation", [str, str | None])
def test_empty_required_string_is_missing(path, encoding, annotation):
    app = FastAPI()

    class Model(BaseModel):
        value: annotation

    @app.post("/parameter")
    def read_parameter(value: Annotated[annotation, Form()]):
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
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
    ]


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
@pytest.mark.parametrize("annotation", [int, int | None])
def test_empty_required_integer_is_missing(path, encoding, annotation):
    app = FastAPI()

    class Model(BaseModel):
        value: annotation

    @app.post("/parameter")
    def read_parameter(value: Annotated[annotation, Form()]):
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
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "value"]),
    ]


@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_empty_form_model_value_uses_default_factory(encoding):
    app = FastAPI()
    default_factory = Mock(return_value=10)

    class Model(BaseModel):
        value: Annotated[int, Field(default_factory=default_factory)]

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    default_factory.assert_not_called()
    client = TestClient(app)
    if encoding == "urlencoded":
        response = client.post("/", data={"value": ""})
    else:
        response = client.post("/", files={"value": (None, "")})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": 10}, "supplied": {}}
    default_factory.assert_called_once_with()


@pytest.mark.parametrize("validate_default,expected", [(False, 10), (True, 20)])
def test_empty_form_model_value_respects_default_validation(validate_default, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            int,
            AfterValidator(lambda value: value * 2),
            Field(validate_default=validate_default),
        ] = 10

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data={"value": ""})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": expected}, "supplied": {}}


@pytest.mark.parametrize(
    "field",
    [
        Field(alias="input"),
        Field(alias="legacy", validation_alias="input"),
        Field(validation_alias=AliasChoices("first", "input")),
    ],
)
def test_empty_form_model_value_uses_alias(field):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[int, field] = 10

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data={"input": "5"})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": 5}, "supplied": {"value": 5}}
    response = client.post("/", data={"input": ""})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": 10}, "supplied": {}}


@pytest.mark.parametrize(
    "config",
    [
        ConfigDict(populate_by_name=True, extra="forbid"),
        pytest.param(
            ConfigDict(validate_by_alias=False, extra="forbid"),
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_alias requires Pydantic 2.11",
            ),
        ),
    ],
)
def test_empty_form_model_value_accepts_field_name(config):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        value: Annotated[int, Field(alias="input")] = 10

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data={"value": "5"})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": 5}, "supplied": {"value": 5}}
    response = client.post("/", data={"value": ""})
    assert response.status_code == 200
    assert response.json() == {"values": {"value": 10}, "supplied": {}}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        ({"first": "", "second": ""}, 10),
        ({"first": "", "second": "5"}, 5),
        ({"first": "5", "second": ""}, 5),
        ({"first": "5", "second": "6"}, 5),
    ],
)
def test_empty_form_values_with_alias_choices(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            int, Field(validation_alias=AliasChoices("first", "second"))
        ] = 10

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            int, Form(validation_alias=AliasChoices("first", "second"))
        ] = 10,
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump()

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_required_form_alias_choices_preserve_validation_precedence(path):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[int, Field(validation_alias=AliasChoices("first", "second"))]

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[int, Form(validation_alias=AliasChoices("first", "second"))],
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump()

    client = TestClient(app)
    response = client.post(path, data={"first": "", "second": "5"})
    assert response.status_code == 200
    assert response.json() == {"value": 5}

    response = client.post(path, data={"first": "invalid", "second": "5"})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("int_parsing", ["body", "first"]),
    ]

    response = client.post(path, data={"first": "", "second": ""})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "first"]),
    ]

    response = client.post(path, data={"first": "", "second": "invalid"})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("int_parsing", ["body", "second"]),
    ]

    response = client.post(path, data={"second": "invalid"})
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("int_parsing", ["body", "second"]),
    ]

    response = client.post(path)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "first"]),
    ]


@pytest.mark.parametrize(
    "data,expected,supplied",
    [
        ({"first": "", "value": ""}, 10, {}),
        ({"first": "", "value": "5"}, 5, {"value": 5}),
    ],
)
def test_empty_form_model_alias_falls_back_to_field_name(data, expected, supplied):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        value: Annotated[
            int, Field(validation_alias=AliasChoices("first", "second"))
        ] = 10

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return {
            "value": params.value,
            "supplied": params.model_dump(exclude_unset=True),
        }

    client = TestClient(app)
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected, "supplied": supplied}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        ({"second": [""]}, [""]),
        ({"second": ["", "hello"]}, ["", "hello"]),
        ({"first": [""], "second": ["hello"]}, [""]),
    ],
)
def test_form_list_alias_choices_preserve_empty_items(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            list[str], Field(validation_alias=AliasChoices("first", "second"))
        ]

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            list[str], Form(validation_alias=AliasChoices("first", "second"))
        ],
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_form_list_alias_choices_error_uses_selected_alias(encoding):
    app = FastAPI()

    @app.post("/")
    def read_form(
        values: Annotated[
            list[int],
            Form(alias="legacy", validation_alias=AliasChoices("first", "second")),
        ],
    ):
        return values

    client = TestClient(app)
    if encoding == "urlencoded":
        response = client.post("/", data={"second": ["1", "2"]})
    else:
        response = client.post(
            "/", files=[("second", (None, "1")), ("second", (None, "2"))]
        )
    assert response.status_code == 200
    assert response.json() == [1, 2]

    if encoding == "urlencoded":
        response = client.post("/", data={"second": ["1", "invalid"], "legacy": "3"})
    else:
        response = client.post(
            "/",
            files=[
                ("second", (None, "1")),
                ("second", (None, "invalid")),
                ("legacy", (None, "3")),
            ],
        )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "second", 1],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


def test_individual_form_parameters_can_share_an_alias_choice():
    app = FastAPI()

    @app.post("/")
    def read_form(
        values: Annotated[
            list[int], Form(validation_alias=AliasChoices("values", "shared"))
        ],
        value: Annotated[int, Form(validation_alias=AliasChoices("value", "shared"))],
    ):
        return {"values": values, "value": value}

    client = TestClient(app)
    response = client.post("/", data={"shared": ["1", "2"]})
    assert response.status_code == 200
    assert response.json() == {"values": [1, 2], "value": 2}


@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
def test_form_model_fields_can_share_an_unused_alias_choice(encoding):
    app = FastAPI()

    class Model(BaseModel):
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("names", "legacy"))
        ]
        text: Annotated[str, Field(validation_alias=AliasChoices("text", "legacy"))]

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return params

    client = TestClient(app)
    if encoding == "urlencoded":
        response = client.post("/", data={"legacy": ["one", "two"], "text": "hello"})
    else:
        response = client.post(
            "/",
            files=[
                ("legacy", (None, "one")),
                ("legacy", (None, "two")),
                ("text", (None, "hello")),
            ],
        )
    assert response.status_code == 200
    assert response.json() == {"names": ["one", "two"], "text": "hello"}


@pytest.mark.parametrize("encoding", ["urlencoded", "multipart"])
@pytest.mark.parametrize("unused", ["unused", ""])
def test_unused_form_alias_choice_keeps_extra_value_shape(encoding, unused):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("names", "legacy-names"))
        ]
        text: Annotated[
            str, Field(validation_alias=AliasChoices("text", "legacy-text"))
        ]

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return params

    client = TestClient(app)
    if encoding == "urlencoded":
        response = client.post(
            "/",
            data={
                "names": ["one", "two"],
                "text": "hello",
                "legacy-names": unused,
                "legacy-text": ["", "unused"],
            },
        )
    else:
        response = client.post(
            "/",
            files=[
                ("names", (None, "one")),
                ("names", (None, "two")),
                ("text", (None, "hello")),
                ("legacy-names", (None, unused)),
                ("legacy-text", (None, "")),
                ("legacy-text", (None, "unused")),
            ],
        )
    assert response.status_code == 200
    assert response.json() == {
        "names": ["one", "two"],
        "text": "hello",
        "legacy-names": unused,
        "legacy-text": ["", "unused"],
    }


def test_empty_form_model_value_preserves_extra_and_json_strings():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        value: str = "default"

    @app.post("/form")
    def read_form(params: Annotated[Model, Form()]):
        return {
            "values": params.model_dump(),
            "supplied": params.model_dump(exclude_unset=True),
        }

    @app.post("/json")
    def read_json(params: Model):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/form", data={"value": "", "extra": ""})
    assert response.status_code == 200
    assert response.json() == {
        "values": {"value": "default", "extra": ""},
        "supplied": {"extra": ""},
    }
    response = client.post("/json", json={"value": "", "extra": ""})
    assert response.status_code == 200
    assert response.json() == {"value": "", "extra": ""}
    assert Model.model_validate({"value": ""}).model_dump(exclude_unset=True) == {
        "value": ""
    }


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
        "/parameter",
        "/model",
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
        pytest.param({}, False, id="unchecked"),
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
        pytest.param({}, False, id="unchecked"),
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
        pytest.param({}, False, id="unchecked"),
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


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "alias,validation_alias", [("enabled", None), ("legacy", "enabled")]
)
@pytest.mark.parametrize("data,expected", [({"enabled": "on"}, True), ({}, False)])
def test_checkbox_uses_alias(path, alias, validation_alias, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            bool, Field(alias=alias, validation_alias=validation_alias)
        ] = True

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            bool, Form(alias=alias, validation_alias=validation_alias)
        ] = True,
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize(
    "config",
    [
        ConfigDict(populate_by_name=True, extra="forbid"),
        pytest.param(
            ConfigDict(validate_by_alias=False, extra="forbid"),
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_alias requires Pydantic 2.11",
            ),
        ),
    ],
)
@pytest.mark.parametrize("data,expected", [({"value": "on"}, True), ({}, False)])
@pytest.mark.parametrize(
    "validation_alias", [None, AliasChoices("enabled", "checkbox")]
)
def test_checkbox_model_accepts_field_name(config, data, expected, validation_alias):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        value: Annotated[
            bool, Field(alias="enabled", validation_alias=validation_alias)
        ]

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize(
    "data,expected",
    [
        ({"enabled": "on"}, True),
        ({"checkbox": "on"}, True),
        ({"checkbox": ["off", "on"]}, True),
        ({"enabled": "", "checkbox": "on"}, True),
        ({}, False),
    ],
)
def test_checkbox_with_alias_choices(path, data, expected):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[
            bool,
            Field(alias="legacy", validation_alias=AliasChoices("enabled", "checkbox")),
        ]

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            bool,
            Form(alias="legacy", validation_alias=AliasChoices("enabled", "checkbox")),
        ],
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"value": expected}


@pytest.mark.parametrize(
    "config",
    [
        ConfigDict(extra="forbid"),
        pytest.param(
            ConfigDict(validate_by_alias=False, extra="forbid"),
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_alias requires Pydantic 2.11",
            ),
        ),
    ],
)
def test_unchecked_checkbox_with_alias_choices_overrides_defaults(config):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        value: Annotated[
            bool, Field(validation_alias=AliasChoices("enabled", "checkbox"))
        ] = True
        nullable: Annotated[
            bool | None, Field(validation_alias=AliasChoices("optional", "nullable"))
        ] = None

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == {"value": False, "nullable": False}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_checkbox_alias_choices_preserve_validation_precedence(path):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            bool,
            Field(alias="legacy", validation_alias=AliasChoices("enabled", "checkbox")),
        ]

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            bool,
            Form(alias="legacy", validation_alias=AliasChoices("enabled", "checkbox")),
        ],
    ):
        return {"value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post(
        path, data={"enabled": "on", "checkbox": "invalid", "legacy": "invalid"}
    )
    assert response.status_code == 200
    assert response.json() == {"value": True}

    response = client.post(path, data={"enabled": "", "legacy": "on"})
    assert response.status_code == 422

    response = client.post(path, data={"enabled": "invalid", "checkbox": "on"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "bool_parsing",
                "loc": ["body", "enabled"],
                "msg": "Input should be a valid boolean, unable to interpret input",
                "input": "invalid",
            }
        ]
    }


@pytest.mark.parametrize(
    "validation_alias,missing_name",
    [
        (AliasPath("enabled"), "enabled"),
        (AliasChoices("checkbox", AliasPath("enabled")), "checkbox"),
    ],
)
def test_checkbox_alias_path_is_unchanged(validation_alias, missing_name):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[bool, Field(validation_alias=validation_alias)]

    @app.post("/")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    response = client.post("/", data={"enabled": "on"})
    assert response.status_code == 200
    assert response.json() == {"value": True}

    response = client.post("/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", missing_name],
                "msg": "Field required",
                "input": {},
            }
        ]
    }


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("checked", [True, False])
def test_checkbox_in_multipart_form(path, checked):
    app = FastAPI()

    class Model(BaseModel):
        name: str
        value: bool = True

    @app.post("/parameter")
    def read_parameter(
        name: Annotated[str, Form()], value: Annotated[bool, Form()] = True
    ):
        return {"name": name, "value": value}

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.model_dump(exclude_unset=True)

    client = TestClient(app)
    if checked:
        response = client.post(
            path, files={"name": (None, "Alice"), "value": (None, "on")}
        )
    else:
        response = client.post(path, files={"name": (None, "Alice")})
    assert response.status_code == 200
    assert response.json() == {"name": "Alice", "value": checked}


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_unchecked_checkbox_is_validated_without_calling_default_factory(path):
    app = FastAPI()
    default_factory = Mock(return_value=True)

    def require_checked(value: bool) -> bool:
        if not value:
            raise ValueError("The checkbox must be checked")
        return value

    class Model(BaseModel):
        value: Annotated[
            bool,
            AfterValidator(require_checked),
            Field(default_factory=default_factory),
        ]

    @app.post("/parameter")
    def read_parameter(
        value: Annotated[
            bool, AfterValidator(require_checked), Form(default_factory=default_factory)
        ],
    ):
        return value

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.value

    client = TestClient(app)
    checked = client.post(path, data={"value": "on"})
    assert checked.status_code == 200
    assert checked.json() is True
    response = client.post(path)
    assert response.status_code == 422
    assert [
        (error["type"], error["loc"], error["input"])
        for error in response.json()["detail"]
    ] == [("value_error", ["body", "value"], False)]
    default_factory.assert_not_called()


@pytest.mark.parametrize("path", ["/parameter", "/model"])
@pytest.mark.parametrize("annotation", [list[bool] | None, bool | str | None])
def test_omitted_boolean_list_or_union_uses_default(path, annotation):
    app = FastAPI()

    class Model(BaseModel):
        value: annotation = None

    @app.post("/parameter")
    def read_parameter(value: Annotated[annotation, Form()] = None):
        return value

    @app.post("/model")
    def read_model(params: Annotated[Model, Form()]):
        return params.value

    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() is None


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

    response = client.post("/form")
    assert response.status_code == 200
    assert response.json() == {"value": False}

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
