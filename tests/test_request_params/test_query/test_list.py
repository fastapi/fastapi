from collections.abc import Sequence
from typing import Annotated

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from typing_extensions import TypeAliasType

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-list-str")
async def read_required_list_str(p: Annotated[list[str], Query()]):
    return {"p": p}


class QueryModelRequiredListStr(BaseModel):
    p: list[str]


@app.get("/model-required-list-str")
def read_model_required_list_str(p: Annotated[QueryModelRequiredListStr, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": True,
                "schema": {
                    "title": "P",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "name": "p",
                "in": "query",
            }
        ]
    )


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.get("/required-list-alias")
async def read_required_list_alias(p: Annotated[list[str], Query(alias="p_alias")]):
    return {"p": p}


class QueryModelRequiredListAlias(BaseModel):
    p: list[str] = Field(alias="p_alias")


@app.get("/model-required-list-alias")
async def read_model_required_list_alias(
    p: Annotated[QueryModelRequiredListAlias, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": True,
                "schema": {
                    "title": "P Alias",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "name": "p_alias",
                "in": "query",
            }
        ]
    )


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias",
        "/model-required-list-alias",
    ],
)
def test_required_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": ["hello", "world"]}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias",
        "/model-required-list-alias",
    ],
)
def test_required_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.get("/required-list-validation-alias")
def read_required_list_validation_alias(
    p: Annotated[list[str], Query(validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredListValidationAlias(BaseModel):
    p: list[str] = Field(validation_alias="p_val_alias")


@app.get("/model-required-list-validation-alias")
async def read_model_required_list_validation_alias(
    p: Annotated[QueryModelRequiredListValidationAlias, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": True,
                "schema": {
                    "title": "P Val Alias",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "name": "p_val_alias",
                "in": "query",
            }
        ]
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-validation-alias",
        "/model-required-list-validation-alias",
    ],
)
def test_required_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
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
        "/required-list-validation-alias",
        "/model-required-list-validation-alias",
    ],
)
def test_required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": ["hello", "world"]}),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    assert response.status_code == 200, response.text

    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias and validation alias


@app.get("/required-list-alias-and-validation-alias")
def read_required_list_alias_and_validation_alias(
    p: Annotated[list[str], Query(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredListAliasAndValidationAlias(BaseModel):
    p: list[str] = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-list-alias-and-validation-alias")
def read_model_required_list_alias_and_validation_alias(
    p: Annotated[QueryModelRequiredListAliasAndValidationAlias, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == snapshot(
        [
            {
                "required": True,
                "schema": {
                    "title": "P Val Alias",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "name": "p_val_alias",
                "in": "query",
            }
        ]
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
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
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "query",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    {
                        "p": [
                            "hello",
                            "world",
                        ]
                    },
                ),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    {"p_alias": ["hello", "world"]},
                ),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# TypeAliasType (PEP 695-style aliases)


Tags = TypeAliasType("Tags", list[str])


@app.get("/type-alias-list-str")
async def read_type_alias_list_str(p: Annotated[Tags, Query()]):
    return {"p": p}


def test_type_alias_list_str():
    client = TestClient(app)
    response = client.get("/type-alias-list-str?p=hello&p=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


TupleTags = TypeAliasType("TupleTags", tuple[str, ...])


@app.get("/type-alias-tuple-str")
async def read_type_alias_tuple_str(p: Annotated[TupleTags, Query()]):
    return {"p": p}


def test_type_alias_tuple_str():
    client = TestClient(app)
    response = client.get("/type-alias-tuple-str?p=hello&p=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# Sequence[str]
SeqTags = TypeAliasType("SeqTags", Sequence[str])


@app.get("/type-alias-sequence-str")
async def read_type_alias_sequence_str(p: Annotated[SeqTags, Query()]):
    return {"p": p}


def test_type_alias_sequence_str():
    client = TestClient(app)
    response = client.get("/type-alias-sequence-str?p=hello&p=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# Nested/chained alias
InnerTags = TypeAliasType("InnerTags", list[str])
OuterTags = TypeAliasType("OuterTags", InnerTags)


@app.get("/type-alias-nested-list-str")
async def read_type_alias_nested_list_str(p: Annotated[OuterTags, Query()]):
    return {"p": p}


def test_type_alias_nested_list_str():
    client = TestClient(app)
    response = client.get("/type-alias-nested-list-str?p=hello&p=world")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}
