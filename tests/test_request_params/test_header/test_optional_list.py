from typing import Annotated, Optional

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-list-str")
async def read_optional_list_str(
    p: Annotated[Optional[list[str]], Header()] = None,
):
    return {"p": p}


class HeaderModelOptionalListStr(BaseModel):
    p: Optional[list[str]] = None


@app.get("/model-optional-list-str")
async def read_model_optional_list_str(
    p: Annotated[HeaderModelOptionalListStr, Header()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P",
            },
            "name": "p",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-str", "/model-optional-list-str"],
)
def test_optional_list_str(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.get("/optional-list-alias")
async def read_optional_list_alias(
    p: Annotated[Optional[list[str]], Header(alias="p_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListAlias(BaseModel):
    p: Optional[list[str]] = Field(None, alias="p_alias")


@app.get("/model-optional-list-alias")
async def read_model_optional_list_alias(
    p: Annotated[HeaderModelOptionalListAlias, Header()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Alias",
            },
            "name": "p_alias",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-alias", "/model-optional-list-alias"],
)
def test_optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias",
        "/model-optional-list-alias",
    ],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.get("/optional-list-validation-alias")
def read_optional_list_validation_alias(
    p: Annotated[Optional[list[str]], Header(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-list-validation-alias")
def read_model_optional_list_validation_alias(
    p: Annotated[HeaderModelOptionalListValidationAlias, Header()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            },
            "name": "p_val_alias",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias and validation alias


@app.get("/optional-list-alias-and-validation-alias")
def read_optional_list_alias_and_validation_alias(
    p: Annotated[
        Optional[list[str]], Header(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class HeaderModelOptionalListAliasAndValidationAlias(BaseModel):
    p: Optional[list[str]] = Field(
        None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.get("/model-optional-list-alias-and-validation-alias")
def read_model_optional_list_alias_and_validation_alias(
    p: Annotated[HeaderModelOptionalListAliasAndValidationAlias, Header()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": False,
            "schema": {
                "anyOf": [
                    {"items": {"type": "string"}, "type": "array"},
                    {"type": "null"},
                ],
                "title": "P Val Alias",
            },
            "name": "p_val_alias",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    [
        "/optional-list-alias-and-validation-alias",
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
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
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
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
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "p": [
            "hello",
            "world",
        ]
    }
