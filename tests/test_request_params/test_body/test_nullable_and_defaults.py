from typing import Annotated, Any, Union

import pytest
from dirty_equals import IsList, IsOneOf
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .utils import get_body_model_name

app = FastAPI()


# =====================================================================================
# Nullable required


@app.post("/nullable-required")
async def read_nullable_required(
    int_val: Annotated[Union[int, None], Body()],
    str_val: Annotated[Union[str, None], Body()],
    list_val: Union[list[int], None],
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
    str_val: Annotated[Union[str, None], Body()],
):
    return {"val": str_val}


@app.post("/nullable-required-int")
async def read_nullable_required_no_embed_int(
    int_val: Annotated[Union[int, None], Body()],
):
    return {"val": int_val}


@app.post("/nullable-required-list")
async def read_nullable_required_no_embed_list(
    list_val: Annotated[Union[list[int], None], Body()],
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
def test_nullable_required_pass_empty_dict(path: str, msg: str, error_type: str):
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
    response = client.post(
        path,
        json={
            "int_val": None,
            "str_val": None,
            "list_val": None,
        },
    )
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
    response = client.post(path, content="null")
    assert response.status_code == 200, response.text
    assert response.json() == {"val": None}
    # TODO: add test with BeforeValidator to ensure that it recieves `None` value


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-required",
        "/model-nullable-required",
    ],
)
def test_nullable_required_pass_value(path: str):
    client = TestClient(app)
    response = client.post(
        path, json={"int_val": "1", "str_val": "test", "list_val": ["1", "2"]}
    )
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
    ("path", "value"),
    [
        ("/nullable-required-str", "test"),
        ("/nullable-required-int", 1),
        ("/nullable-required-list", [1, 2]),
    ],
)
def test_nullable_required_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)
    response = client.post(
        path,
        json=value,
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}


# =====================================================================================
# Nullable with default=None


@app.post("/nullable-non-required")
async def read_nullable_non_required(
    int_val: Annotated[Union[int, None], Body()] = None,
    str_val: Annotated[Union[str, None], Body()] = None,
    list_val: Union[list[int], None] = None,
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
    str_val: Annotated[Union[str, None], Body()] = None,
):
    return {"val": str_val}


@app.post("/nullable-non-required-int")
async def read_nullable_non_required_no_embed_int(
    int_val: Annotated[Union[int, None], Body()] = None,
):
    return {"val": int_val}


@app.post("/nullable-non-required-list")
async def read_nullable_non_required_no_embed_list(
    list_val: Annotated[Union[list[int], None], Body()] = None,
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
    response = client.post(path, json={})
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
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"val": None}


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_pass_null(path: str):
    client = TestClient(app)
    response = client.post(
        path,
        json={
            "int_val": None,
            "str_val": None,
            "list_val": None,
        },
    )
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
def test_nullable_non_required_no_embed_pass_null(path: str):
    client = TestClient(app)
    response = client.post(path, content="null")
    assert response.status_code == 200, response.text
    assert response.json() == {"val": None}
    # TODO: add test with BeforeValidator to ensure that it recieves `None` value


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-non-required",
        "/model-nullable-non-required",
    ],
)
def test_nullable_non_required_pass_value(path: str):
    client = TestClient(app)
    response = client.post(
        path, json={"int_val": 1, "str_val": "test", "list_val": [1, 2]}
    )
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
    ("path", "value"),
    [
        ("/nullable-non-required-str", "test"),
        ("/nullable-non-required-int", 1),
        ("/nullable-non-required-list", [1, 2]),
    ],
)
def test_nullable_non_required_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)
    response = client.post(path, json=value)
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}


# =====================================================================================
# Nullable with not-None default


@app.post("/nullable-with-non-null-default")
async def read_nullable_with_non_null_default(
    *,
    int_val: Annotated[Union[int, None], Body()] = -1,
    str_val: Annotated[Union[str, None], Body()] = "default",
    list_val: Annotated[Union[list[int], None], Body(default_factory=lambda: [0])],
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
    str_val: Annotated[Union[str, None], Body()] = "default",
):
    return {"val": str_val}


@app.post("/nullable-with-non-null-default-int")
async def read_nullable_with_non_null_default_no_embed_int(
    int_val: Annotated[Union[int, None], Body()] = -1,
):
    return {"val": int_val}


@app.post("/nullable-with-non-null-default-list")
async def read_nullable_with_non_null_default_no_embed_list(
    list_val: Annotated[Union[list[int], None], Body(default_factory=lambda: [0])],
):
    return {"val": list_val}


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
        pytest.param(
            "/nullable-with-non-null-default-list",
            {
                "anyOf": [
                    {"type": "array", "items": {"type": "integer"}},
                    {"type": "null"},
                ],
                "title": "List Val",
                "default": [0],  # default_factory is not reflected in OpenAPI schema
            },
            marks=pytest.mark.xfail(
                reason="`default_factory` is not reflected in OpenAPI schema"
            ),
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
    response = client.post(path, json={})
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
    response = client.post(path)
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
    response = client.post(
        path,
        json={
            "int_val": None,
            "str_val": None,
            "list_val": None,
        },
    )
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
    response = client.post(path, content="null")
    assert response.status_code == 200, response.text
    assert response.json() == {"val": None}


@pytest.mark.parametrize(
    "path",
    [
        "/nullable-with-non-null-default",
        "/model-nullable-with-non-null-default",
    ],
)
def test_nullable_with_non_null_default_pass_value(path: str):
    client = TestClient(app)
    response = client.post(
        path, json={"int_val": "1", "str_val": "test", "list_val": ["1", "2"]}
    )
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
    ("path", "value"),
    [
        ("/nullable-with-non-null-default-str", "test"),
        ("/nullable-with-non-null-default-int", 1),
        ("/nullable-with-non-null-default-list", [1, 2]),
    ],
)
def test_nullable_with_non_null_default_no_embed_pass_value(path: str, value: Any):
    client = TestClient(app)
    response = client.post(path, json=value)
    assert response.status_code == 200, response.text
    assert response.json() == {"val": value}
