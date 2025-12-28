from typing import Annotated, Optional

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-str", operation_id="optional_str")
async def read_optional_str(p: Annotated[Optional[str], Body(embed=True)] = None):
    return {"p": p}


class BodyModelOptionalStr(BaseModel):
    p: Optional[str] = None


@app.post("/model-optional-str", operation_id="model_optional_str")
async def read_model_optional_str(p: BodyModelOptionalStr):
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


def test_optional_str_missing():
    client = TestClient(app)
    response = client.post("/optional-str")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


def test_model_optional_str_missing():
    client = TestClient(app)
    response = client.post("/model-optional-str")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["body"],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.post("/optional-alias", operation_id="optional_alias")
async def read_optional_alias(
    p: Annotated[Optional[str], Body(embed=True, alias="p_alias")] = None,
):
    return {"p": p}


class BodyModelOptionalAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias")


@app.post("/model-optional-alias", operation_id="model_optional_alias")
async def read_model_optional_alias(p: BodyModelOptionalAlias):
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


def test_optional_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-alias")
    assert response.status_code == 200
    assert response.json() == {"p": None}


def test_model_optional_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-alias")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["body"],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_model_optional_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.post("/optional-validation-alias", operation_id="optional_validation_alias")
def read_optional_validation_alias(
    p: Annotated[
        Optional[str], Body(embed=True, validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class BodyModelOptionalValidationAlias(BaseModel):
    p: Optional[str] = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-validation-alias", operation_id="model_optional_validation_alias"
)
def read_model_optional_validation_alias(
    p: BodyModelOptionalValidationAlias,
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


def test_optional_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-validation-alias")
    assert response.status_code == 200
    assert response.json() == {"p": None}


def test_model_optional_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-validation-alias")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["body"],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_model_optional_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
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
    response = client.post(path, json={"p": "hello"})
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
    response = client.post(path, json={"p_val_alias": "hello"})
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
        Optional[str], Body(embed=True, alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class BodyModelOptionalAliasAndValidationAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-optional-alias-and-validation-alias",
    operation_id="model_optional_alias_and_validation_alias",
)
def read_model_optional_alias_and_validation_alias(
    p: BodyModelOptionalAliasAndValidationAlias,
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


def test_optional_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-alias-and-validation-alias")
    assert response.status_code == 200
    assert response.json() == {"p": None}


def test_model_optional_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-alias-and-validation-alias")
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["body"],
                "msg": "Field required",
                "type": "missing",
            },
        ],
    }


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_model_optional_alias_and_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
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
    response = client.post(path, json={"p": "hello"})
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
    response = client.post(path, json={"p_alias": "hello"})
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
    response = client.post(path, json={"p_val_alias": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}
