from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsList, IsOneOf, IsPartialDict
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, BeforeValidator, field_validator

app = FastAPI()


def convert(v: Any) -> Any:
    return v


# =====================================================================================
# Nullable required


@app.get("/nullable-required")
async def read_nullable_required(
    int_val: Annotated[
        int | None,
        BeforeValidator(lambda v: convert(v)),
    ],
    str_val: Annotated[
        str | None,
        BeforeValidator(lambda v: convert(v)),
    ],
    list_val: Annotated[
        list[int] | None,
        Query(),
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
    @classmethod
    def convert_all(cls, v: Any) -> Any:
        return convert(v)


@app.get("/model-nullable-required")
async def read_model_nullable_required(
    params: Annotated[ModelNullableRequired, Query()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "Int Val",
                "anyOf": [{"type": "integer"}, {"type": "null"}],
            },
            "name": "int_val",
            "in": "query",
        },
        {
            "required": True,
            "schema": {
                "title": "Str Val",
                "anyOf": [{"type": "string"}, {"type": "null"}],
            },
            "name": "str_val",
            "in": "query",
        },
        {
            "in": "query",
            "name": "list_val",
            "required": True,
            "schema": {
                "anyOf": [
                    {"items": {"type": "integer"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "List Val",
            },
        },
    ]


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
        response = client.get(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "int_val"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            },
            {
                "type": "missing",
                "loc": ["query", "str_val"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            },
            {
                "type": "missing",
                "loc": ["query", "list_val"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            },
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
@pytest.mark.parametrize(
    "values",
    [
        {"int_val": "1", "str_val": "test", "list_val": ["1", "2"]},
        {"int_val": "0", "str_val": "", "list_val": ["0"]},
    ],
)
def test_nullable_required_pass_value(path: str, values: dict[str, Any]):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path, params=values)

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "list_val": [int(v) for v in values["list_val"]],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


# =====================================================================================
# Nullable with default=None


@app.get("/nullable-non-required")
async def read_nullable_non_required(
    int_val: Annotated[
        int | None,
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        str | None,
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    list_val: Annotated[
        list[int] | None,
        Query(),
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
    @classmethod
    def convert_all(cls, v: Any) -> Any:
        return convert(v)


@app.get("/model-nullable-non-required")
async def read_model_nullable_non_required(
    params: Annotated[ModelNullableNonRequired, Query()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "title": "Int Val",
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
            "name": "int_val",
            "in": "query",
        },
        {
            "required": False,
            "schema": {
                "title": "Str Val",
                "anyOf": [{"type": "string"}, {"type": "null"}],
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
            "name": "str_val",
            "in": "query",
        },
        {
            "in": "query",
            "name": "list_val",
            "required": False,
            "schema": {
                "anyOf": [
                    {"items": {"type": "integer"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "List Val",
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
        },
    ]


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
        response = client.get(path)

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
        "/model-nullable-non-required",
    ],
)
@pytest.mark.parametrize(
    "values",
    [
        {"int_val": "1", "str_val": "test", "list_val": ["1", "2"]},
        {"int_val": "0", "str_val": "", "list_val": ["0"]},
    ],
)
def test_nullable_non_required_pass_value(path: str, values: dict[str, Any]):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path, params=values)

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "list_val": [int(v) for v in values["list_val"]],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


# =====================================================================================
# Nullable with not-None default


@app.get("/nullable-with-non-null-default")
async def read_nullable_with_non_null_default(
    *,
    int_val: Annotated[
        int | None,
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        str | None,
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
    list_val: Annotated[
        list[int] | None,
        Query(default_factory=lambda: [0]),
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
    @classmethod
    def convert_all(cls, v: Any) -> Any:
        return convert(v)


@app.get("/model-nullable-with-non-null-default")
async def read_model_nullable_with_non_null_default(
    params: Annotated[ModelNullableWithNonNullDefault, Query()],
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
    parameters = app.openapi()["paths"][path]["get"]["parameters"]
    assert parameters == [
        {
            "required": False,
            "schema": {
                "title": "Int Val",
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "default": -1,
            },
            "name": "int_val",
            "in": "query",
        },
        {
            "required": False,
            "schema": {
                "title": "Str Val",
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "default": "default",
            },
            "name": "str_val",
            "in": "query",
        },
        {
            "in": "query",
            "name": "list_val",
            "required": False,
            "schema": IsPartialDict(
                {
                    "anyOf": [
                        {"items": {"type": "integer"}, "type": "array"},
                        {"type": "null"},
                    ],
                    "title": "List Val",
                }
            ),
        },
    ]

    if path == "/model-nullable-with-non-null-default":
        # Check default value for list_val param for model-based parameters only.
        # default_factory is not reflected in OpenAPI schema
        assert parameters[2]["schema"]["default"] == [0]


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
        response = client.get(path)

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
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
@pytest.mark.parametrize(
    "values",
    [
        {"int_val": "1", "str_val": "test", "list_val": ["1", "2"]},
        {"int_val": "0", "str_val": "", "list_val": ["0"]},
    ],
)
def test_nullable_with_non_null_default_pass_value(path: str, values: dict[str, Any]):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path, params=values)

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "list_val": [int(v) for v in values["list_val"]],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }
