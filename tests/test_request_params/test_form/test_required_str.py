from typing import Annotated

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-str", operation_id="required_str")
async def read_required_str(p: Annotated[str, Form()]):
    return {"p": p}


class FormModelRequiredStr(BaseModel):
    p: str


@app.post("/model-required-str", operation_id="model_required_str")
async def read_model_required_str(p: Annotated[FormModelRequiredStr, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {"title": "P", "type": "string"},
        },
        "required": ["p"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.post("/required-alias", operation_id="required_alias")
async def read_required_alias(p: Annotated[str, Form(alias="p_alias")]):
    return {"p": p}


class FormModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.post("/model-required-alias", operation_id="model_required_alias")
async def read_model_required_alias(p: Annotated[FormModelRequiredAlias, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias",
        "/model-required-alias",
    ],
)
def test_required_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {"title": "P Alias", "type": "string"},
        },
        "required": ["p_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/required-alias", "/model-required-alias"],
)
def test_required_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-alias", "/model-required-alias"],
)
def test_required_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": "hello"}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-alias", "/model-required-alias"],
)
def test_required_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.post("/required-validation-alias", operation_id="required_validation_alias")
def read_required_validation_alias(
    p: Annotated[str, Form(validation_alias="p_val_alias")],
):
    return {"p": p}


class FormModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.post(
    "/model-required-validation-alias", operation_id="model_required_validation_alias"
)
def read_model_required_validation_alias(
    p: Annotated[FormModelRequiredValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-validation-alias", "/model-required-validation-alias"],
)
def test_required_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {"title": "P Val Alias", "type": "string"},
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-validation-alias",
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-validation-alias",
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": "hello"}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-validation-alias",
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-alias-and-validation-alias",
    operation_id="required_alias_and_validation_alias",
)
def read_required_alias_and_validation_alias(
    p: Annotated[str, Form(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class FormModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-alias-and-validation-alias",
    operation_id="model_required_alias_and_validation_alias",
)
def read_model_required_alias_and_validation_alias(
    p: Annotated[FormModelRequiredAliasAndValidationAlias, Form()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {"title": "P Val Alias", "type": "string"},
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": "hello"}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p_alias": "hello"}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}
