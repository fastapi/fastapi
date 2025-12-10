import pytest
from dirty_equals import IsDict, IsOneOf
from fastapi import Cookie, FastAPI
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from tests.utils import needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: Annotated[str, Cookie()]):
    return {"p": p}


class CookieModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: CookieModelRequiredStr = Cookie()):
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
            "in": "cookie",
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
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["cookie", "p"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    ["/required-str", "/model-required-str"],
)
def test_required_str(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Cookie(alias="p_alias")]):
    return {"p": p}


class CookieModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: CookieModelRequiredAlias = Cookie()):
    return {"p": p.p}  # pragma: no cover


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
            "in": "cookie",
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
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["cookie", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias",
        pytest.param(
            "/model-required-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 models",
                strict=False,
            ),
        ),
    ],
)
def test_required_alias_by_name(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(
                        None,
                        {"p": "hello"},  # /model-required-alias PDv2 fails here
                    ),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["cookie", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-alias",
        pytest.param(
            "/model-required-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
    ],
)
def test_required_alias_by_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200, (  # /model-required-alias fails here
        response.text
    )
    assert response.json() == {"p": "hello"}


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Cookie(validation_alias="p_val_alias")],
):
    return {"p": p}


class CookieModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: CookieModelRequiredValidationAlias = Cookie(),
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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
            "in": "cookie",
        }
    ]


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
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
                    "cookie",
                    "p_val_alias",  # /required-validation-alias fails here
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_by_name(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 422, (  # /required-validation-alias fails here
        response.text
    )

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["cookie", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p": "hello"}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-required-validation-alias",
    ],
)
def test_required_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200, (  # /required-validation-alias fails here
        response.text
    )

    assert response.json() == {"p": "hello"}


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Cookie(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class CookieModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: CookieModelRequiredAliasAndValidationAlias = Cookie(),
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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
            "in": "cookie",
        }
    ]


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
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
                    "cookie",
                    "p_val_alias",  # /required-alias-and-validation-alias fails here
                ],
                "msg": "Field required",
                "input": IsOneOf(None, {}),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    client.cookies.set("p", "hello")
    response = client.get(path)
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "cookie",
                    "p_val_alias",  # /required-alias-and-validation-alias fails here
                ],
                "msg": "Field required",
                "input": IsOneOf(  # /model-alias-and-validation-alias fails here
                    None,
                    {"p": "hello"},
                ),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-alias-and-validation-alias",
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    assert (
        response.status_code == 422  # /required-alias-and-validation-alias fails here
    )

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["cookie", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(  # /model-alias-and-validation-alias fails here
                    None,
                    {"p_alias": "hello"},
                ),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-required-alias-and-validation-alias",
    ],
)
def test_required_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    assert response.status_code == 200, (
        response.text  # /required-alias-and-validation-alias fails here
    )

    assert response.json() == {"p": "hello"}
