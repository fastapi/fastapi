from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-list-str", operation_id="optional_list_str")
async def read_optional_list_str(
    p: Annotated[Optional[list[str]], Form()] = None,
):
    return {"p": p}


class FormModelOptionalListStr(BaseModel):
    p: Optional[list[str]] = None


@app.post("/model-optional-list-str", operation_id="model_optional_list_str")
async def read_model_optional_list_str(p: Annotated[FormModelOptionalListStr, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.post("/optional-list-alias", operation_id="optional_list_alias")
async def read_optional_list_alias(
    p: Annotated[Optional[list[str]], Form(alias="p_alias")] = None,
):
    return {"p": p}


class FormModelOptionalListAlias(BaseModel):
    p: Optional[list[str]] = Field(None, alias="p_alias")


@app.post("/model-optional-list-alias", operation_id="model_optional_list_alias")
async def read_model_optional_list_alias(
    p: Annotated[FormModelOptionalListAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias",
        "/model-optional-list-alias",
    ],
)
def test_optional_list_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.post(
    "/optional-list-validation-alias", operation_id="optional_list_validation_alias"
)
def read_optional_list_validation_alias(
    p: Annotated[Optional[list[str]], Form(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class FormModelOptionalListValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-list-validation-alias",
    operation_id="model_optional_list_validation_alias",
)
def read_model_optional_list_validation_alias(
    p: Annotated[FormModelOptionalListValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-validation-alias",
        "/model-optional-list-validation-alias",
    ],
)
def test_optional_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-list-alias-and-validation-alias",
    operation_id="optional_list_alias_and_validation_alias",
)
def read_optional_list_alias_and_validation_alias(
    p: Annotated[
        Optional[list[str]], Form(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class FormModelOptionalListAliasAndValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(
        None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post(
    "/model-optional-list-alias-and-validation-alias",
    operation_id="model_optional_list_alias_and_validation_alias",
)
def read_model_optional_list_alias_and_validation_alias(
    p: Annotated[FormModelOptionalListAliasAndValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "p": [
            "hello",
            "world",
        ]
    }
