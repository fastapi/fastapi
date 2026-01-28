from typing import Annotated, Union

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# =====================================================================================
# Without aliases which exercise the "Wildcard" capture behavior


@app.get("/required-dict-str")
async def read_required_dict_str(p: Annotated[dict[str, str], Query()]):
    return {"p": p}


class QueryModelRequiredDictStr(BaseModel):
    p: dict[str, str]


@app.get("/model-required-dict-str")
def read_model_required_dict_str(p: Annotated[QueryModelRequiredDictStr, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-dict-str", "/model-required-dict-str"],
)
def test_required_dict_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P",
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-dict-str", "/model-required-dict-str"],
)
def test_required_dict_str_missing(path: str):
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
    ["/required-dict-str", "/model-required-dict-str"],
)
def test_required_dict_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?foo=bar&baz=qux")
    assert response.status_code == 200
    assert response.json() == {"p": {"foo": "bar", "baz": "qux"}}


# =====================================================================================
# With union types


@app.get("/required-dict-union")
async def read_required_dict_union(
    p: Annotated[Union[dict[str, str], dict[str, int]], Query()],
):
    return {"p": p}


class QueryModelRequiredDictUnion(BaseModel):
    p: dict[str, str] | dict[str, int]


@app.get("/model-required-dict-union")
def read_model_required_dict_union(p: Annotated[QueryModelRequiredDictUnion, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-dict-union", "/model-required-dict-union"],
)
def test_required_dict_union_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P",
                "anyOf": [
                    {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                    },
                    {
                        "type": "object",
                        "additionalProperties": {"type": "integer"},
                    },
                ],
            },
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-dict-union", "/model-required-dict-union"],
)
def test_required_dict_union_missing(path: str):
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
    ["/required-dict-union", "/model-required-dict-union"],
)
def test_required_dict_union(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?foo=bar&baz=42")
    assert response.status_code == 200
    assert response.json() == {"p": {"foo": "bar", "baz": "42"}}


@app.get("/required-dict-of-union")
async def read_required_dict_of_union(p: Annotated[dict[str, int | bool], Query()]):
    return {"p": p}


class QueryModelRequiredDictOfUnion(BaseModel):
    p: dict[str, int | bool]


@app.get("/model-required-dict-of-union")
def read_model_required_dict_of_union(
    p: Annotated[QueryModelRequiredDictOfUnion, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-dict-of-union", "/model-required-dict-of-union"],
)
def test_required_dict_of_union_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P",
                "type": "object",
                "additionalProperties": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "boolean"},
                    ]
                },
            },
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-dict-of-union", "/model-required-dict-of-union"],
)
def test_required_dict_of_union_missing(path: str):
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
    ["/required-dict-of-union", "/model-required-dict-of-union"],
)
def test_required_dict_of_union(path: str):
    client = TestClient(app)
    # Testing the "Wildcard" capture behavior for dicts
    response = client.get(f"{path}?foo=True&baz=42")
    assert response.status_code == 200
    assert response.json() == {"p": {"foo": True, "baz": 42}}


@app.get("/required-dict-of-list")
async def read_required_dict_of_list(p: Annotated[dict[str, list[int]], Query()]):
    return {"p": p}


class QueryModelRequiredDictOfList(BaseModel):
    p: dict[str, list[int]]


@app.get("/model-required-dict-of-list")
def read_model_required_dict_of_list(
    p: Annotated[QueryModelRequiredDictOfList, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-dict-of-list", "/model-required-dict-of-list"],
)
def test_required_dict_of_list_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P",
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "integer"},
                },
            },
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-dict-of-list", "/model-required-dict-of-list"],
)
def test_required_dict_of_list_missing(path: str):
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
    ["/required-dict-of-list", "/model-required-dict-of-list"],
)
def test_required_dict_of_list(path: str):
    client = TestClient(app)
    # Testing the "Wildcard" capture behavior for dicts with list values
    response = client.get(f"{path}?foo=1&foo=2&baz=3")
    assert response.status_code == 200
    assert response.json() == {"p": {"foo": [1, 2], "baz": [3]}}
