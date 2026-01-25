from typing import Annotated

import pytest
from dirty_equals import AnyThing, IsOneOf, IsPartialDict
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: Annotated[str, Header()]):
    return {"p": p}


class HeaderModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: Annotated[HeaderModelRequiredStr, Header()]):
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
            "in": "header",
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
                "loc": ["header", "p"],
                "msg": "Field required",
                "input": AnyThing,
            }
        ]
    }


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str(path: str):
    client = TestClient(app)
    response = client.get(path, headers={"p": "hello"})
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Header(alias="p_alias")]):
    return {"p": p}


class HeaderModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: Annotated[HeaderModelRequiredAlias, Header()]):
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
            "in": "header",
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
                "loc": ["header", "p_alias"],
                "msg": "Field required",
                "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "p_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, IsPartialDict({"p": "hello"})),
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
    response = client.get(path, headers={"p_alias": "hello"})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Header(validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: Annotated[HeaderModelRequiredValidationAlias, Header()],
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
            "in": "header",
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
                    "header",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    assert response.status_code == 422, response.text

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, IsPartialDict({"p": "hello"})),
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
    response = client.get(path, headers={"p_val_alias": "hello"})
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Header(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: Annotated[HeaderModelRequiredAliasAndValidationAlias, Header()],
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
            "in": "header",
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
                    "header",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "header",
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    IsPartialDict({"p": "hello"}),
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
    response = client.get(path, headers={"p_alias": "hello"})
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    IsPartialDict({"p_alias": "hello"}),
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
    response = client.get(path, headers={"p_val_alias": "hello"})
    assert response.status_code == 200, response.text

    assert response.json() == {"p": "hello"}
