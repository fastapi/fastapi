from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from dirty_equals import AnyThing, IsList, IsOneOf, IsPartialDict
from fastapi import FastAPI, Header
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
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ],
    str_val: Annotated[
        str | None,
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ],
    list_val: Annotated[
        list[int] | None,
        Header(),
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
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-required")
async def read_model_nullable_required(
    params: Annotated[ModelNullableRequired, Header()],
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
            "/nullable-required",
            marks=pytest.mark.xfail(
                reason="Title contains hyphens for single Header parameters"
            ),
        ),
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
                "name": "int-val",
                "in": "header",
            },
            {
                "required": True,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                },
                "name": "str-val",
                "in": "header",
            },
            {
                "required": True,
                "schema": {
                    "title": "List Val",
                    "anyOf": [
                        {"type": "array", "items": {"type": "integer"}},
                        {"type": "null"},
                    ],
                },
                "name": "list-val",
                "in": "header",
            },
        ]
    )


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        pytest.param(
            "/model-nullable-required",
            marks=pytest.mark.xfail(
                reason=(
                    "For parameters declared as model, underscores are not replaced "
                    "with hyphens in error loc"
                )
            ),
        ),
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
                    "loc": ["header", "int-val"],
                    "msg": "Field required",
                    "input": AnyThing(),
                },
                {
                    "type": "missing",
                    "loc": ["header", "str-val"],
                    "msg": "Field required",
                    "input": AnyThing(),
                },
                {
                    "type": "missing",
                    "loc": ["header", "list-val"],
                    "msg": "Field required",
                    "input": AnyThing(),
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
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", "test"),
                ("list-val", "1"),
                ("list-val", "2"),
            ],
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


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_pass_empty_str_to_str_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", ""),
                ("list-val", "1"),
            ],
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "",
        "list_val": [1],
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
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        str | None,
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    list_val: Annotated[
        list[int] | None,
        Header(),
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
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-non-required")
async def read_model_nullable_non_required(
    params: Annotated[ModelNullableNonRequired, Header()],
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
            "/nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Title contains hyphens for single Header parameters"
            ),
        ),
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
                "name": "int-val",
                "in": "header",
            },
            {
                "required": False,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "name": "str-val",
                "in": "header",
            },
            {
                "required": False,
                "schema": {
                    "title": "List Val",
                    "anyOf": [
                        {"type": "array", "items": {"type": "integer"}},
                        {"type": "null"},
                    ],
                    # "default": None, # `None` values are omitted in OpenAPI schema
                },
                "name": "list-val",
                "in": "header",
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
def test_nullable_non_required_pass_value(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", "test"),
                ("list-val", "1"),
                ("list-val", "2"),
            ],
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


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_pass_empty_str_to_str_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", ""),
                ("list-val", "1"),
            ],
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "",
        "list_val": [1],
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
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        str | None,
        Header(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
    list_val: Annotated[
        list[int] | None,
        Header(default_factory=lambda: [0]),
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
    def convert_fields(cls, v):
        return convert(v)


@app.get("/model-nullable-with-non-null-default")
async def read_model_nullable_with_non_null_default(
    params: Annotated[ModelNullableWithNonNullDefault, Header()],
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
                reason="Title contains hyphens for single Header parameters"
            ),
        ),
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_schema(path: str):
    parameters = app.openapi()["paths"][path]["get"]["parameters"]
    assert parameters == snapshot(
        [
            {
                "required": False,
                "schema": {
                    "title": "Int Val",
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "default": -1,
                },
                "name": "int-val",
                "in": "header",
            },
            {
                "required": False,
                "schema": {
                    "title": "Str Val",
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "default": "default",
                },
                "name": "str-val",
                "in": "header",
            },
            {
                "required": False,
                "schema": IsPartialDict(
                    {
                        "title": "List Val",
                        "anyOf": [
                            {"type": "array", "items": {"type": "integer"}},
                            {"type": "null"},
                        ],
                    }
                ),
                "name": "list-val",
                "in": "header",
            },
        ]
    )

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
def test_nullable_with_non_null_default_pass_value(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", "test"),
                ("list-val", "1"),
                ("list-val", "2"),
            ],
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


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_pass_empty_str_to_str_val(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.get(
            path,
            headers=[
                ("int-val", "1"),
                ("str-val", ""),
                ("list-val", "1"),
            ],
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": 1,
        "str_val": "",
        "list_val": [1],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }
