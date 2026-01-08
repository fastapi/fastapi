from typing import Annotated

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: str):
    return {"p": p}


class QueryModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: Annotated[QueryModelRequiredStr, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {"title": "P", "type": "string"},
            "name": "p",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str_missing(path: str):
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
    ["/required-str", "/model-required-str"],
)
def test_required_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Query(alias="p_alias")]):
    return {"p": p}


class QueryModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: Annotated[QueryModelRequiredAlias, Query()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-alias", "/model-required-alias"],
)
def test_required_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {"title": "P Alias", "type": "string"},
            "name": "p_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-alias", "/model-required-alias"],
)
def test_required_alias_missing(path: str):
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
        "/required-alias",
        "/model-required-alias",
    ],
)
def test_required_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    {"p": "hello"},
                ),
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias",
        "/model-required-alias",
    ],
)
def test_required_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_alias=hello")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Query(validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: Annotated[QueryModelRequiredValidationAlias, Query()],
):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-validation-alias", "/model-required-validation-alias"],
)
def test_required_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {"title": "P Val Alias", "type": "string"},
            "name": "p_val_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    [
        "/required-validation-alias",
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_missing(path: str):
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
        "/required-validation-alias",
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_val_alias=hello")
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Query(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: Annotated[QueryModelRequiredAliasAndValidationAlias, Query()],
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
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {"title": "P Val Alias", "type": "string"},
            "name": "p_val_alias",
            "in": "query",
        }
    ]


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_missing(path: str):
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
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
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
                    {"p": "hello"},
                ),
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
    response = client.get(f"{path}?p_alias=hello")
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    {"p_alias": "hello"},
                ),
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
    response = client.get(f"{path}?p_val_alias=hello")
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}
