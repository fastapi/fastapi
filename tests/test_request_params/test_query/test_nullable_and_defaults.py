from typing import Annotated, Any

import pytest
from dirty_equals import IsList, IsOneOf, IsPartialDict
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel

app = FastAPI()


# =====================================================================================
# Nullable required


@app.get("/nullable-required")
async def read_nullable_required(
    int_val: int | None,
    str_val: str | None,
    list_val: Annotated[list[int] | None, Query()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
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

    response = client.get(path)

    assert response.status_code == 422
    assert response.json() == snapshot(
        {
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
        {"int_val": "1", "str_val": "test", "list_val": ["1", "2"]},
        {"int_val": "0", "str_val": "", "list_val": ["0"]},
    ],
)
def test_nullable_required_pass_value(path: str, values: dict[str, Any]):
    client = TestClient(app)

    response = client.get(path, params=values)

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
    int_val: int | None = None,
    str_val: str | None = None,
    list_val: Annotated[list[int] | None, Query()] = None,
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

    response = client.get(path)

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

    response = client.get(path, params=values)

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
    int_val: int | None = -1,
    str_val: str | None = "default",
    list_val: Annotated[list[int] | None, Query(default_factory=lambda: [0])],
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
    assert parameters == snapshot(
        [
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
    )

    if path == "/model-nullable-with-non-null-default":
        # Check default value for list_val param for model-based parameters only.
        # default_factory is not reflected in OpenAPI schema
        assert parameters[2]["schema"]["default"] == [0]


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        pytest.param(
            "/model-nullable-with-non-null-default",
            marks=pytest.mark.xfail(
                reason="Missing model fields are marked as explicitly set"
            ),
        ),
    ],
)
def test_nullable_with_non_null_default_missing(path: str):
    client = TestClient(app)

    response = client.get(path)

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

    response = client.get(path, params=values)

    assert response.status_code == 200, response.text
    assert response.json() == {
        "int_val": int(values["int_val"]),
        "str_val": values["str_val"],
        "list_val": [int(v) for v in values["list_val"]],
        "fields_set": IsOneOf(
            None, IsList("int_val", "str_val", "list_val", check_order=False)
        ),
    }
