from typing import Annotated, Any
from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsList, IsOneOf, IsPartialDict
from fastapi import Body, FastAPI
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
    int_val: Annotated[int | None, Body(), BeforeValidator(lambda v: convert(v))],
    str_val: Annotated[str | None, Body(), BeforeValidator(lambda v: convert(v))],
    list_val: Annotated[
        list[int] | None,
        Body(),
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
    def validate_all(cls, v):
        return convert(v)


@app.post("/model-nullable-required")
async def read_model_nullable_required(params: ModelNullableRequired):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@app.post("/nullable-required-str")
async def read_nullable_required_no_embed_str(
    str_val: Annotated[str | None, Body(), BeforeValidator(lambda v: convert(v))],
):
    return {"val": str_val}


@app.post("/nullable-required-int")
async def read_nullable_required_no_embed_int(
    int_val: Annotated[int | None, Body(), BeforeValidator(lambda v: convert(v))],
):
    return {"val": int_val}


@app.post("/nullable-required-list")
async def read_nullable_required_no_embed_list(
    list_val: Annotated[
        list[int] | None, Body(), BeforeValidator(lambda v: convert(v))
    ],
):
    return {"val": list_val}


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
    ("path", "schema"),
    [
        (
            "/nullable-required-str",
            {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "Str Val",
            },
        ),
        (
            "/nullable-required-int",
            {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "title": "Int Val",
            },
        ),
        (
            "/nullable-required-list",
            {
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "title": "List Val",
            },
        ),
    ],
)
def test_nullable_required_no_embed_schema(path: str, schema: dict):
    openapi = app.openapi()
    path_operation = openapi["paths"][path]["post"]
    assert (
        path_operation["requestBody"]["content"]["application/json"]["schema"] == schema
    )
    assert path_operation["requestBody"]["required"] is True


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_missing(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
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
                reason="For non-model Body parameters, gives errors for each parameter separately"
            ),
        ),
        "/model-nullable-required",
    ],
)
def test_nullable_required_no_body(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body"],
                "msg": "Field required",
                "input": None,
            },
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-str",
        "/nullable-required-int",
        "/nullable-required-list",
    ],
)
def test_nullable_required_no_embed_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["body"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }


@pytest.mark.parametrize(
    ("path", "msg", "error_type"),
    [
        (
            "/nullable-required-str",
            "Input should be a valid string",
            "string_type",
        ),
        (
            "/nullable-required-int",
            "Input should be a valid integer",
            "int_type",
        ),
        (
            "/nullable-required-list",
            "Input should be a valid list",
            "list_type",
        ),
    ],
)
def test_nullable_required_no_embed_pass_empty_dict(
    path: str, msg: str, error_type: str
):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body"],
                "msg": msg,
                "type": error_type,
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-required",
            marks=pytest.mark.xfail(
                reason="Null values are treated as missing for non-model Body parameters"
            ),
        ),
        pytest.param(
            "/model-nullable-required",
        ),
    ],
)
def test_nullable_required_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            json={
                "int_val": None,
                "str_val": None,
                "list_val": None,
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": None,
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required-str",
        "/nullable-required-int",
        "/nullable-required-list",
    ],
)
@pytest.mark.xfail(reason="Explicit null-body is treated as missing")
def test_nullable_required_no_embed_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, content="null")

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text  # pragma: no cover
    assert response.json() == {"val": None}  # pragma: no cover
    # TODO: Remove 'no cover' when the issue is fixed


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
        response = client.post(path, json=values)

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


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ("/nullable-required-str", "test"),
        ("/nullable-required-str", ""),
        ("/nullable-required-int", 1),
        ("/nullable-required-list", [1, 2]),
    ],
)
def test_nullable_required_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, json=value)

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}


# =====================================================================================
# Nullable with default=None


@app.post("/nullable-non-required")
async def read_nullable_non_required(
    int_val: Annotated[
        int | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    str_val: Annotated[
        str | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
    list_val: Annotated[
        list[int] | None,
        Body(),
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
    def validate_all(cls, v):
        return convert(v)


@app.post("/model-nullable-non-required")
async def read_model_nullable_non_required(
    params: ModelNullableNonRequired,
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@app.post("/nullable-non-required-str")
async def read_nullable_non_required_no_embed_str(
    str_val: Annotated[
        str | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {"val": str_val}


@app.post("/nullable-non-required-int")
async def read_nullable_non_required_no_embed_int(
    int_val: Annotated[
        int | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {"val": int_val}


@app.post("/nullable-non-required-list")
async def read_nullable_non_required_no_embed_list(
    list_val: Annotated[
        list[int] | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = None,
):
    return {"val": list_val}


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
    ("path", "schema"),
    [
        (
            "/nullable-non-required-str",
            {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "Str Val",
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
        ),
        (
            "/nullable-non-required-int",
            {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "title": "Int Val",
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
        ),
        (
            "/nullable-non-required-list",
            {
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "title": "List Val",
                # "default": None, # `None` values are omitted in OpenAPI schema
            },
        ),
    ],
)
def test_nullable_non_required_no_embed_schema(path: str, schema: dict):
    openapi = app.openapi()
    path_operation = openapi["paths"][path]["post"]
    assert (
        path_operation["requestBody"]["content"]["application/json"]["schema"] == schema
    )
    assert "required" not in path_operation["requestBody"]


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
        response = client.post(path, json={})

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
                reason="For non-model Body parameters, validates each parameter separately"
            ),
        ),
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_no_body(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body"],
                "msg": "Field required",
                "input": None,
            },
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-str",
        "/nullable-non-required-int",
        "/nullable-non-required-list",
    ],
)
def test_nullable_non_required_no_embed_missing(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200
    assert response.json() == {"val": None}


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-non-required",
            marks=pytest.mark.xfail(
                reason="Null values are treated as missing for non-model Body parameters"
            ),
        ),
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            json={
                "int_val": None,
                "str_val": None,
                "list_val": None,
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": None,
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required-str",
        "/nullable-non-required-int",
        "/nullable-non-required-list",
    ],
)
@pytest.mark.xfail(reason="Explicit null-body is treated as missing")
def test_nullable_non_required_no_embed_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, content="null")

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text  # pragma: no cover
    assert response.json() == {"val": None}  # pragma: no cover
    # TODO: Remove 'no cover' when the issue is fixed


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
        response = client.post(path, json=values)

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


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ("/nullable-non-required-str", "test"),
        ("/nullable-non-required-str", ""),
        ("/nullable-non-required-int", 1),
        ("/nullable-non-required-list", [1, 2]),
    ],
)
def test_nullable_non_required_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, json=value)

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}


# =====================================================================================
# Nullable with not-None default


@app.post("/nullable-with-non-null-default")
async def read_nullable_with_non_null_default(
    *,
    int_val: Annotated[
        int | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
    str_val: Annotated[
        str | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
    list_val: Annotated[
        list[int] | None,
        Body(default_factory=lambda: [0]),
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
    def validate_all(cls, v):
        return convert(v)


@app.post("/model-nullable-with-non-null-default")
async def read_model_nullable_with_non_null_default(
    params: ModelNullableWithNonNullDefault,
):
    return {
        "int_val": params.int_val,
        "str_val": params.str_val,
        "list_val": params.list_val,
        "fields_set": params.model_fields_set,
    }


@app.post("/nullable-with-non-null-default-str")
async def read_nullable_with_non_null_default_no_embed_str(
    str_val: Annotated[
        str | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = "default",
):
    return {"val": str_val}


@app.post("/nullable-with-non-null-default-int")
async def read_nullable_with_non_null_default_no_embed_int(
    int_val: Annotated[
        int | None,
        Body(),
        BeforeValidator(lambda v: convert(v)),
    ] = -1,
):
    return {"val": int_val}


@app.post("/nullable-with-non-null-default-list")
async def read_nullable_with_non_null_default_no_embed_list(
    list_val: Annotated[
        list[int] | None,
        Body(default_factory=lambda: [0]),
        BeforeValidator(lambda v: convert(v)),
    ],
):
    return {"val": list_val}


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
    body_model = app.openapi()["components"]["schemas"][body_model_name]

    assert body_model == {
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
                },
            ),
        },
        "title": body_model_name,
        "type": "object",
    }

    if path == "/model-nullable-with-non-null-default":
        # Check default value for list_val param for model-based parameters only.
        # default_factory is not reflected in OpenAPI schema
        assert body_model["properties"]["list_val"]["default"] == [0]


@pytest.mark.parametrize(
    ("path", "schema"),
    [
        (
            "/nullable-with-non-null-default-str",
            {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "Str Val",
                "default": "default",
            },
        ),
        (
            "/nullable-with-non-null-default-int",
            {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "title": "Int Val",
                "default": -1,
            },
        ),
        (
            "/nullable-with-non-null-default-list",
            {
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "title": "List Val",
            },
        ),
    ],
)
def test_nullable_with_non_null_default_no_embed_schema(path: str, schema: dict):
    openapi = app.openapi()
    path_operation = openapi["paths"][path]["post"]
    assert (
        path_operation["requestBody"]["content"]["application/json"]["schema"] == schema
    )
    assert "required" not in path_operation["requestBody"]


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_missing(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, json={})

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200, response.text
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
                reason="For non-model Body parameters, validates each parameter separately"
            ),
        ),
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_no_body(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body"],
                "msg": "Field required",
                "input": None,
            },
        ]
    }


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/nullable-with-non-null-default-str", "default"),
        ("/nullable-with-non-null-default-int", -1),
        ("/nullable-with-non-null-default-list", [0]),
    ],
)
def test_nullable_with_non_null_default_no_embed_missing(path: str, expected: Any):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path)

    assert mock_convert.call_count == 0, (
        "Validator should not be called if the value is missing"
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"val": expected}


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Null values are treated as missing for non-model Body parameters"
            ),
        ),
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(
            path,
            json={
                "int_val": None,
                "str_val": None,
                "list_val": None,
            },
        )

    assert mock_convert.call_count == 3, "Validator should be called for each field"
    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": None,
        "str_val": None,
        "list_val": None,
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default-str",
        "/nullable-with-non-null-default-int",
        "/nullable-with-non-null-default-list",
    ],
)
@pytest.mark.xfail(reason="Explicit null-body is treated as missing")
def test_nullable_with_non_null_default_no_embed_pass_null(path: str):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, content="null")

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text  # pragma: no cover
    assert response.json() == {"val": None}  # pragma: no cover
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
        response = client.post(path, json=values)

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


@pytest.mark.parametrize(
    ("path", "value"),
    [
        ("/nullable-with-non-null-default-str", "test"),
        ("/nullable-with-non-null-default-str", ""),
        ("/nullable-with-non-null-default-int", 1),
        ("/nullable-with-non-null-default-list", [1, 2]),
    ],
)
def test_nullable_with_non_null_default_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)

    with patch(f"{__name__}.convert", Mock(wraps=convert)) as mock_convert:
        response = client.post(path, json=value)

    assert mock_convert.call_count == 1, "Validator should be called once for the field"
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}
