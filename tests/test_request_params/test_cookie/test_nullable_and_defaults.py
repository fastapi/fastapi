from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsList, IsOneOf
from fastapi import Cookie, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
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
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ],
    str_val: Annotated[
        str | None,
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ],
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "fields_set": None,
    }


class ModelNullableRequired(BaseModel):
    int_val: int | None
    str_val: str | None

    @field_validator("*", mode="before")
    @classmethod
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-required")
async def read_model_nullable_required(
    params: Annotated[ModelNullableRequired, Cookie()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": True,
                "schema": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                },
                "name": "int_val",
                "in": "cookie",
            },
            {
                "required": True,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                },
                "name": "str_val",
                "in": "cookie",
            },
        ]
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
        response = client.get(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 422
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "int_val"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                },
                {
                    "type": "missing",
                    "loc": ["cookie", "str_val"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
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
@pytest.mark.parametrize(
    "values",
    [
        {"int_val": "1", "str_val": "test"},
        {"int_val": "0", "str_val": ""},
    ],
)
def test_nullable_required_pass_value(path: str, values: dict[str, str]):
    client = TestClient(app)
    client.cookies.set("int_val", values["int_val"])
    client.cookies.set("str_val", values["str_val"])
    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path)

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "fields_set": IsOneOf(None, IsList("int_val", "str_val", check_order=False)),
    }


# =====================================================================================
# Nullable with default=None


@app.get("/nullable-non-required")
async def read_nullable_non_required(
    int_val: Annotated[
        int | None,
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        str | None,
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "fields_set": None,
    }


class ModelNullableNonRequired(BaseModel):
    int_val: int | None = None
    str_val: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-non-required")
async def read_model_nullable_non_required(
    params: Annotated[ModelNullableNonRequired, Cookie()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": False,
                "schema": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "name": "int_val",
                "in": "cookie",
            },
            {
                "required": False,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "name": "str_val",
                "in": "cookie",
            },
        ]
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
        response = client.get(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200
    assert response.json() == {
        "int_val": None,
        "str_val": None,
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
        {"int_val": "1", "str_val": "test"},
        {"int_val": "0", "str_val": ""},
    ],
)
def test_nullable_non_required_pass_value(path: str, values: dict[str, str]):
    client = TestClient(app)
    client.cookies.set("int_val", values["int_val"])
    client.cookies.set("str_val", values["str_val"])

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path)

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "fields_set": IsOneOf(None, IsList("int_val", "str_val", check_order=False)),
    }


# =====================================================================================
# Nullable with not-None default


@app.get("/nullable-with-non-null-default")
async def read_nullable_with_non_null_default(
    *,
    int_val: Annotated[
        int | None,
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        str | None,
        Cookie(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
):
    return {
        "int_val": int_val,
        "str_val": str_val,
        "fields_set": None,
    }


class ModelNullableWithNonNullDefault(BaseModel):
    int_val: int | None = -1
    str_val: str | None = "default"

    @field_validator("*", mode="before")
    @classmethod
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-with-non-null-default")
async def read_model_nullable_with_non_null_default(
    params: Annotated[ModelNullableWithNonNullDefault, Cookie()],
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": False,
                "schema": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "default": -1,
                },
                "name": "int_val",
                "in": "cookie",
            },
            {
                "required": False,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "default": "default",
                },
                "name": "str_val",
                "in": "cookie",
            },
        ]
    )


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
        {"int_val": "1", "str_val": "test"},
        {"int_val": "0", "str_val": ""},
    ],
)
def test_nullable_with_non_null_default_pass_value(path: str, values: dict[str, str]):
    client = TestClient(app)
    client.cookies.set("int_val", values["int_val"])
    client.cookies.set("str_val", values["str_val"])

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(path)

    assert mock_convert.call_count == 2, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "fields_set": IsOneOf(None, IsList("int_val", "str_val", check_order=False)),
    }
