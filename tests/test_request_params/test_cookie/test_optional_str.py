from typing import Optional

import pytest
from dirty_equals import IsDict
from fastapi import Cookie, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from tests.utils import needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-str")
async def read_optional_str(p: Optional[str] = Cookie(None)):
    return {"p": p}


class CookieModelOptionalStr(BaseModel):
    p: Optional[str] = None


@app.get("/model-optional-str")
async def read_model_optional_str(p: CookieModelOptionalStr = Cookie()):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-str", "/model-optional-str"],
)
def test_optional_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        IsDict(
            {
                "required": False,
                "schema": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "title": "P",
                },
                "name": "p",
                "in": "cookie",
            }
        )
        | IsDict(
            # TODO: remove when deprecating Pydantic v1
            {
                "required": False,
                "schema": {"title": "P", "type": "string"},
                "name": "p",
                "in": "cookie",
            }
        )
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.get("/optional-alias")
async def read_optional_alias(p: Optional[str] = Cookie(None, alias="p_alias")):
    return {"p": p}


class CookieModelOptionalAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias")


@app.get("/model-optional-alias")
async def read_model_optional_alias(p: CookieModelOptionalAlias = Cookie()):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/optional-alias", "/model-optional-alias"],
)
def test_optional_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        IsDict(
            {
                "required": False,
                "schema": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "title": "P Alias",
                },
                "name": "p_alias",
                "in": "cookie",
            }
        )
        | IsDict(
            # TODO: remove when deprecating Pydantic v1
            {
                "required": False,
                "schema": {"title": "P Alias", "type": "string"},
                "name": "p_alias",
                "in": "cookie",
            }
        )
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias",
        pytest.param(
            "/model-optional-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
    ],
)
def test_optional_alias_by_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}  # /model-optional-alias fails here


# =====================================================================================
# Validation alias


@app.get("/optional-validation-alias")
def read_optional_validation_alias(
    p: Optional[str] = Cookie(None, validation_alias="p_val_alias"),
):
    return {"p": p}


class CookieModelOptionalValidationAlias(BaseModel):
    p: Optional[str] = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-validation-alias")
def read_model_optional_validation_alias(
    p: CookieModelOptionalValidationAlias = Cookie(),
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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
            "in": "cookie",
        }
    ]


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    ["/optional-validation-alias", "/model-optional-validation-alias"],
)
def test_optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-validation-alias",
    ],
)
def test_optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-validation-alias",
    ],
)
def test_optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}  # /optional-validation-alias fails here


# =====================================================================================
# Alias and validation alias


@app.get("/optional-alias-and-validation-alias")
def read_optional_alias_and_validation_alias(
    p: Optional[str] = Cookie(None, alias="p_alias", validation_alias="p_val_alias"),
):
    return {"p": p}


class CookieModelOptionalAliasAndValidationAlias(BaseModel):
    p: Optional[str] = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-optional-alias-and-validation-alias")
def read_model_optional_alias_and_validation_alias(
    p: CookieModelOptionalAliasAndValidationAlias = Cookie(),
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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
            "in": "cookie",
        }
    ]


@needs_pydanticv2
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


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/optional-alias-and-validation-alias",
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {
        "p": None  # /optional-alias-and-validation-alias fails here
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-alias-and-validation-alias",
    ],
)
def test_optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {
        "p": "hello"  # /optional-alias-and-validation-alias fails here
    }
