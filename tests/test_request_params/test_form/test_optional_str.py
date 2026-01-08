from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-str", operation_id="optional_str")
async def read_optional_str(p: Annotated[Optional[str], Form()] = None):
    return {"p": p}


class FormModelOptionalStr(BaseModel):
    p: Optional[str] = None


@app.post("/model-optional-str", operation_id="model_optional_str")
async def read_model_optional_str(p: Annotated[FormModelOptionalStr, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.post("/optional-alias", operation_id="optional_alias")
async def read_optional_alias(
    p: Annotated[Optional[str], Form(alias="p_alias")] = None,
):
    return {"p": p}


class FormModelOptionalAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias")


@app.post("/model-optional-alias", operation_id="model_optional_alias")
async def read_model_optional_alias(p: Annotated[FormModelOptionalAlias, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias",
        "/model-optional-alias",
    ],
)
def test_optional_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.post("/optional-validation-alias", operation_id="optional_validation_alias")
def read_optional_validation_alias(
    p: Annotated[Optional[str], Form(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class FormModelOptionalValidationAlias(BaseModel):
    p: Optional[str] = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-validation-alias", operation_id="model_optional_validation_alias"
)
def read_model_optional_validation_alias(
    p: Annotated[FormModelOptionalValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Val Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-validation-alias",
        "/model-optional-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-validation-alias",
        "/model-optional-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-alias-and-validation-alias",
    operation_id="optional_alias_and_validation_alias",
)
def read_optional_alias_and_validation_alias(
    p: Annotated[
        Optional[str], Form(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class FormModelOptionalAliasAndValidationAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-optional-alias-and-validation-alias",
    operation_id="model_optional_alias_and_validation_alias",
)
def read_model_optional_alias_and_validation_alias(
    p: Annotated[FormModelOptionalAliasAndValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Val Alias",
            },
        },
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}
