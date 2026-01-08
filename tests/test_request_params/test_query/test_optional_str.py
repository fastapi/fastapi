from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-str")
async def read_optional_str(p: Optional[str] = None):
    return {"p": p}


class QueryModelOptionalStr(BaseModel):
    p: Optional[str] = None


@app.get("/model-optional-str")
async def read_model_optional_str(p: Annotated[QueryModelOptionalStr, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P",
            },
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.get("/optional-alias")
async def read_optional_alias(
    p: Annotated[Optional[str], Query(alias="p_alias")] = None,
):
    return {"p": p}


class QueryModelOptionalAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias")


@app.get("/model-optional-alias")
async def read_model_optional_alias(p: Annotated[QueryModelOptionalAlias, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Alias",
            },
            "name": "p_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias",
        "/model-optional-alias",
    ],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_alias=hello")
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.get("/optional-validation-alias")
def read_optional_validation_alias(
    p: Annotated[Optional[str], Query(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class QueryModelOptionalValidationAlias(BaseModel):
    p: Optional[str] = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-validation-alias")
def read_model_optional_validation_alias(
    p: Annotated[QueryModelOptionalValidationAlias, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_optional_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Val Alias",
            },
            "name": "p_val_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
    response = client.get(f"{path}?p=hello")
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
    response = client.get(f"{path}?p_val_alias=hello")
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.get("/optional-alias-and-validation-alias")
def read_optional_alias_and_validation_alias(
    p: Annotated[
        Optional[str], Query(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class QueryModelOptionalAliasAndValidationAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-optional-alias-and-validation-alias")
def read_model_optional_alias_and_validation_alias(
    p: Annotated[QueryModelOptionalAliasAndValidationAlias, Query()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "title": "P Val Alias",
            },
            "name": "p_val_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
    response = client.get(f"{path}?p=hello")
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
    response = client.get(f"{path}?p_alias=hello")
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
    response = client.get(f"{path}?p_val_alias=hello")
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}
