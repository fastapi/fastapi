from typing import Annotated, Optional

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-list-str", operation_id="optional_list_str")
async def read_optional_list_str(
    p: Annotated[Optional[list[str]], Body(embed=True)] = None,
):
    return {"p": p}


class BodyModelOptionalListStr(BaseModel):
    p: Optional[list[str]] = None


@app.post("/model-optional-list-str", operation_id="model_optional_list_str")
async def read_model_optional_list_str(p: BodyModelOptionalListStr):
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


def test_optional_list_str_missing():
    client = TestClient(app)
    response = client.post("/optional-list-str")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


def test_model_optional_list_str_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-str")
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
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.post("/optional-list-alias", operation_id="optional_list_alias")
async def read_optional_list_alias(
    p: Annotated[Optional[list[str]], Body(embed=True, alias="p_alias")] = None,
):
    return {"p": p}


class BodyModelOptionalListAlias(BaseModel):
    p: Optional[list[str]] = Field(None, alias="p_alias")


@app.post("/model-optional-list-alias", operation_id="model_optional_list_alias")
async def read_model_optional_list_alias(p: BodyModelOptionalListAlias):
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


def test_optional_list_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-alias")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


def test_model_optional_list_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-alias")
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
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.post(
    "/optional-list-validation-alias", operation_id="optional_list_validation_alias"
)
def read_optional_list_validation_alias(
    p: Annotated[
        Optional[list[str]], Body(embed=True, validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class BodyModelOptionalListValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-list-validation-alias",
    operation_id="model_optional_list_validation_alias",
)
def read_model_optional_list_validation_alias(
    p: BodyModelOptionalListValidationAlias,
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


def test_optional_list_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-validation-alias")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


def test_model_optional_list_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-validation-alias")
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
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
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
    response = client.post(path, json={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-validation-alias",
        "/model-optional-list-validation-alias",
    ],
)
def test_optional_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
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
        Optional[list[str]],
        Body(embed=True, alias="p_alias", validation_alias="p_val_alias"),
    ] = None,
):
    return {"p": p}


class BodyModelOptionalListAliasAndValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(
        None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.post(
    "/model-optional-list-alias-and-validation-alias",
    operation_id="model_optional_list_alias_and_validation_alias",
)
def read_model_optional_list_alias_and_validation_alias(
    p: BodyModelOptionalListAliasAndValidationAlias,
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


def test_optional_list_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-alias-and-validation-alias")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


def test_model_optional_list_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-alias-and-validation-alias")
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
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    assert response.status_code == 200, response.text
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
    response = client.post(path, json={"p": ["hello", "world"]})
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
    response = client.post(path, json={"p_alias": ["hello", "world"]})
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
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "p": [
            "hello",
            "world",
        ]
    }
