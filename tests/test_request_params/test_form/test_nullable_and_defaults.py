from typing import Annotated, Any, Union
from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsList, IsOneOf
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
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
        Union[int, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ],
    str_val: Annotated[
        Union[str, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ],
    list_val: Annotated[
        Union[list[int], None],
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
    int_val: Union[int, None]
    str_val: Union[str, None]
    list_val: Union[list[int], None]

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

    assert app.openapi()["components"]["schemas"][body_model_name] == {
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
        "title": body_model_name,
        "type": "object",
    }


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
    assert response.json() == {
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


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-required",
            marks=pytest.mark.xfail(
                reason="Empty str is replaced with None, but then None gets dropped"
            ),
        ),
        pytest.param(
            "/model-nullable-required",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for models"
            ),
        ),
    ],
)
def test_nullable_required_pass_empty_str(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "0",  # Empty strings are not treated as null for lists. It's Ok
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert mock_convert.call_args_list == [
        (""),  # int_val
        (""),  # str_val
        (["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": [0],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


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
        Union[int, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        Union[str, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    list_val: Annotated[
        Union[list[int], None],
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
    int_val: Union[int, None] = None
    str_val: Union[str, None] = None
    list_val: Union[list[int], None] = None

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

    assert app.openapi()["components"]["schemas"][body_model_name] == {
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
        "title": body_model_name,
        "type": "object",
    }


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
        pytest.param(
            "/nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Empty str is replaced with None, but then None gets dropped"
            ),
        ),
        pytest.param(
            "/model-nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for models"
            ),
        ),
    ],
)
def test_nullable_non_required_pass_empty_str(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "0",  # Empty strings are not treated as null for lists. It's Ok
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert mock_convert.call_args_list == [
        (""),  # int_val
        (""),  # str_val
        (["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": [0],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


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
        Union[int, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        Union[str, None],
        Form(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
    list_val: Annotated[
        Union[list[int], None],
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
    int_val: Union[int, None] = -1
    str_val: Union[str, None] = "default"
    list_val: Union[list[int], None] = [0]

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
        pytest.param(
            "/nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="`default_factory` is not reflected in OpenAPI schema"
            ),
        ),
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
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
            "list_val": {
                "title": "List Val",
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "default": [0],  # default_factory is not reflected in OpenAPI schema
            },
        },
        "title": body_model_name,
        "type": "object",
    }


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
    assert response.status_code == 200
    assert response.json() == {
        "int_val": -1,
        "str_val": "default",
        "list_val": [0],
        "fields_set": IsOneOf(None, []),
    }


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty str is replaced with default value, not with None"  # Is this correct ???
            ),
        ),
        pytest.param(
            "/model-nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Empty strings are not replaced with None for models"
            ),
        ),
    ],
)
def test_nullable_with_non_null_default_pass_empty_str(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            data={
                "int_val": "",
                "str_val": "",
                "list_val": "0",  # Empty strings are not treated as null for lists. It's Ok
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert mock_convert.call_args_list == [
        (""),  # int_val
        (""),  # str_val
        (["0"]),  # list_val
    ]
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": [0],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


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
