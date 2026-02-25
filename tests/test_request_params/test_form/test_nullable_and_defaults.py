from typing import Annotated, Any
from unittest.mock import Mock, call, patch

import pytest
from dirty_equals import IsList, IsOneOf, IsPartialDict
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from pydantic import BaseModel, BeforeValidator, field_validator

from .utils import get_body_model_name

app = FastAPI()


def convert(v: Any) -> Any:
    return v


# =====================================================================================
# Nullable required


@app.post("/nullable-required")
async def read_nullable_required(
    int_val: Annotated[
        int | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ],
    str_val: Annotated[
        str | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ],
    list_val: Annotated[
        list[int] | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ],
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "list_val": list_val,
        "fields_set": None,
    }


class ModelNullableRequired(BaseModel):
    int_val: int | None
    str_val: str | None
    list_val: list[int] | None

    @field_validator("*", mode="before")
    def convert_fields(cls, v):
        return convert(v)


@app.post("/model-nullable-required")
async def read_model_nullable_required(
    params: Annotated[ModelNullableRequired, Form()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert openapi["components"]["schemas"][body_model_name] == snapshot(
        {
            "properties": {
                "int_val": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                },
                "str_val": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                },
                "list_val": {
                    "title": "List Val",
                    "anyOf": [
                        {"type": "array", "items": {"type": "integer"}},
                        {"type": "null"},
                    ],
                },
            },
            "required": ["int_val", "str_val", "list_val"],
            "title": Is(body_model_name),
            "type": "object",
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_missing(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "int_val"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
                {
                    "type": "missing",
                    "loc": ["body", "str_val"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
                {
                    "type": "missing",
                    "loc": ["body", "list_val"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-required",
            marks=pytest.mark.xfail(
                reason="Empty str is replaced with None even for required parameters"
            ),
        ),
        "/model-nullable-required",
    ],
)
def test_nullable_required_pass_empty_str_to_str_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "0",  # Empty string would cause validation error (see below)
                "str_val": "",
                "list_val": "0",  # Empty string would cause validation error (see below)
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert mock_convert.call_args_list == [
        call("0"),  # int_val
        call(""),  # str_val
        call(["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 0,
        "str_val": "",
        "list_val": [0],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-required",
            marks=pytest.mark.xfail(
                reason="Empty str is replaced with None even for required parameters"
            ),
        ),
        "/model-nullable-required",
    ],
)
def test_nullable_required_pass_empty_str_to_int_val_and_list_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "",
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert mock_convert.call_args_list == [
        call(""),  # int_val
        call(""),  # str_val
        call([""]),  # list_val
    ]
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "input": "",
                    "loc": ["body", "int_val"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                },
                {
                    "input": "",
                    "loc": ["body", "list_val", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                },
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_pass_value(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path, data={"int_val": "1", "str_val": "test", "list_val": ["1", "2"]}
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "test",
        "list_val": [1, 2],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


# =====================================================================================
# Nullable with default=None


@app.post("/nullable-non-required")
async def read_nullable_non_required(
    int_val: Annotated[
        int | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        str | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    list_val: Annotated[
        list[int] | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "list_val": list_val,
        "fields_set": None,
    }


class ModelNullableNonRequired(BaseModel):
    int_val: int | None = None
    str_val: str | None = None
    list_val: list[int] | None = None

    @field_validator("*", mode="before")
    def convert_fields(cls, v):
        return convert(v)


@app.post("/model-nullable-non-required")
async def read_model_nullable_non_required(
    params: Annotated[ModelNullableNonRequired, Form()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert openapi["components"]["schemas"][body_model_name] == snapshot(
        {
            "properties": {
                "int_val": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "str_val": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "list_val": {
                    "title": "List Val",
                    "anyOf": [
                        {"type": "array", "items": {"type": "integer"}},
                        {"type": "null"},
                    ],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
            },
            "title": Is(body_model_name),
            "type": "object",
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_missing(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": None,
        "fields_set": IsOneOf(None, []),
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        pytest.param(
            "/model-nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for parameters declared as model"
            ),
        ),
    ],
)
def test_nullable_non_required_pass_empty_str_to_str_val_and_int_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "0",  # Empty string would cause validation error (see below)
            },
        )

    assert mock_convert.call_count == 1, "Validator should be called for list_val only"
    assert mock_convert.call_args_list == [
        call(["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": [0],
        "fields_set": IsOneOf(None, IsList("list_val", check_order=False)),
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        pytest.param(
            "/model-nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for parameters declared as model"
            ),
        ),
    ],
)
def test_nullable_non_required_pass_empty_str_to_all(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "",
            },
        )

    assert mock_convert.call_count == 1, "Validator should be called for list_val only"
    assert mock_convert.call_args_list == [
        call([""]),  # list_val
    ]
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "input": "",
                    "loc": ["body", "list_val", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                },
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_pass_value(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path, data={"int_val": "1", "str_val": "test", "list_val": ["1", "2"]}
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "test",
        "list_val": [1, 2],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


# =====================================================================================
# Nullable with not-None default


@app.post("/nullable-with-non-null-default")
async def read_nullable_with_non_null_default(
    *,
    int_val: Annotated[
        int | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        str | None,
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
    list_val: Annotated[
        list[int] | None,
        Form(default_factory=lambda: [0]),
        BeforeValidator(lambda v: convert(v)),
    ],
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "list_val": list_val,
        "fields_set": None,
    }


class ModelNullableWithNonNullDefault(BaseModel):
    int_val: int | None = -1
    str_val: str | None = "default"
    list_val: list[int] | None = [0]

    @field_validator("*", mode="before")
    def convert_fields(cls, v):
        return convert(v)


@app.post("/model-nullable-with-non-null-default")
async def read_model_nullable_with_non_null_default(
    params: Annotated[ModelNullableWithNonNullDefault, Form()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)
    body_model = openapi["components"]["schemas"][body_model_name]

    assert body_model == snapshot(
        {
            "properties": {
                "int_val": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "default": -1,
                },
                "str_val": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "default": "default",
                },
                "list_val": IsPartialDict(
                    {
                        "title": "List Val",
                        "anyOf": [
                            {"type": "array", "items": {"type": "integer"}},
                            {"type": "null"},
                        ],
                    }
                ),
            },
            "title": Is(body_model_name),
            "type": "object",
        }
    )

    if path == "/model-nullable-with-non-null-default":
        # Check default value for list_val param for model-based parameters only.
        # default_factory is not reflected in OpenAPI schema
        assert body_model["properties"]["list_val"]["default"] == [0]


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
@pytest.mark.xfail(
    reason="Missing parameters are pre-populated with default values before validation"
)
def test_nullable_with_non_null_default_missing(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200  # pragma: no cover
    assert response.json() == {  # pragma: no cover
        "int_val": -1,
        "str_val": "default",
        "list_val": [0],
        "fields_set": IsOneOf(None, []),
    }
    # TODO: Remove 'no cover' when the issue is fixed


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty strings are replaced with default values before validation"
            ),
        ),
        pytest.param(
            "/model-nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for parameters declared as model"
            ),
        ),
    ],
)
def test_nullable_with_non_null_default_pass_empty_str_to_str_val_and_int_val(
    path: str,
):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "0",  # Empty string would cause validation error (see below)
            },
        )

    assert mock_convert.call_count == 1, "Validator should be called for list_val only"
    assert mock_convert.call_args_list == [  # pragma: no cover
        call(["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text  # pragma: no cover
    assert response.json() == {  # pragma: no cover
        "int_val": -1,
        "str_val": "default",
        "list_val": [0],
        "fields_set": IsOneOf(None, IsList("list_val", check_order=False)),
    }
    # TODO: Remove 'no cover' when the issue is fixed


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty strings are replaced with default values before validation"
            ),
        ),
        pytest.param(
            "/model-nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for parameters declared as model"
            ),
        ),
    ],
)
def test_nullable_with_non_null_default_pass_empty_str_to_all(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "",
            },
        )

    assert mock_convert.call_count == 1, "Validator should be called for list_val only"
    assert mock_convert.call_args_list == [  # pragma: no cover
        call([""]),  # list_val
    ]
    assert response.status_code == 422, response.text  # pragma: no cover
    assert response.json() == snapshot(  # pragma: no cover
        {
            "detail": [
                {
                    "input": "",
                    "loc": ["body", "list_val", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                },
            ]
        }
    )
    # TODO: Remove 'no cover' when the issue is fixed


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_pass_value(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path, data={"int_val": "1", "str_val": "test", "list_val": ["1", "2"]}
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "test",
        "list_val": [1, 2],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }
