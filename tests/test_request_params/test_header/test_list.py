from typing import List

import pytest
from dirty_equals import AnyThing, IsDict, IsOneOf, IsPartialDict
from fastapi import FastAPI, Header
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from tests.utils import needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-list-str")
async def read_required_list_str(p: List[str] = Header(...)):
    return {"p": p}


class HeaderModelRequiredListStr(BaseModel):
    p: List[str]


@app.get("/model-required-list-str")
def read_model_required_list_str(p: HeaderModelRequiredListStr = Header()):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P",
                "type": "array",
                "items": {"type": "string"},
            },
            "name": "p",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p"],
                    "msg": "Field required",
                    "input": AnyThing,
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "loc": ["header", "p"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.get("/required-list-alias")
async def read_required_list_alias(p: List[str] = Header(..., alias="p_alias")):
    return {"p": p}


class HeaderModelRequiredListAlias(BaseModel):
    p: List[str] = Field(..., alias="p_alias")


@app.get("/model-required-list-alias")
async def read_model_required_list_alias(p: HeaderModelRequiredListAlias = Header()):
    return {"p": p.p}  # pragma: no cover


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_str_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P Alias",
                "type": "array",
                "items": {"type": "string"},
            },
            "name": "p_alias",
            "in": "header",
        }
    ]


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_alias"],
                    "msg": "Field required",
                    "input": AnyThing,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["header", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias",
        pytest.param(
            "/model-required-list-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 models",
                strict=False,
            ),
        ),
    ],
)
def test_required_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(  # /model-required-list-alias with PDv2 fails here
                        None, IsPartialDict({"p": ["hello", "world"]})
                    ),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["header", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias",
        pytest.param(
            "/model-required-list-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
    ],
)
def test_required_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    assert response.status_code == 200, (  # /model-required-list-alias fails here
        response.text
    )
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.get("/required-list-validation-alias")
def read_required_list_validation_alias(
    p: List[str] = Header(..., validation_alias="p_val_alias"),
):
    return {"p": p}


class HeaderModelRequiredListValidationAlias(BaseModel):
    p: List[str] = Field(..., validation_alias="p_val_alias")


@app.get("/model-required-list-validation-alias")
async def read_model_required_list_validation_alias(
    p: HeaderModelRequiredListValidationAlias = Header(),
):
    return {"p": p.p}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P Val Alias",
                "type": "array",
                "items": {"type": "string"},
            },
            "name": "p_val_alias",
            "in": "header",
        }
    ]


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-list-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
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
                    "header",
                    "p_val_alias",  # /required-list-validation-alias fails here
                ],
                "msg": "Field required",
                "input": AnyThing,
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-list-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-required-list-validation-alias",
    ],
)
def test_required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 422  # /required-list-validation-alias fails here

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, IsPartialDict({"p": ["hello", "world"]})),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    assert response.status_code == 200, response.text  # both fail here

    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover


# =====================================================================================
# Alias and validation alias


@app.get("/required-list-alias-and-validation-alias")
def read_required_list_alias_and_validation_alias(
    p: List[str] = Header(..., alias="p_alias", validation_alias="p_val_alias"),
):
    return {"p": p}


class HeaderModelRequiredListAliasAndValidationAlias(BaseModel):
    p: List[str] = Field(..., alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-list-alias-and-validation-alias")
def read_model_required_list_alias_and_validation_alias(
    p: HeaderModelRequiredListAliasAndValidationAlias = Header(),
):
    return {"p": p.p}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_schema(path: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {
                "title": "P Val Alias",
                "type": "array",
                "items": {"type": "string"},
            },
            "name": "p_val_alias",
            "in": "header",
        }
    ]


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-list-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
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
                    "header",
                    # /required-list-alias-and-validation-alias fails here
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": AnyThing,
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "header",
                    # /required-list-alias-and-validation-alias fails here
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-required-list-alias-and-validation-alias fails here
                    IsPartialDict({"p": ["hello", "world"]}),
                ),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    assert (  # /required-list-alias-and-validation-alias fails here
        response.status_code == 422
    )
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-required-list-alias-and-validation-alias fails here
                    IsPartialDict({"p_alias": ["hello", "world"]}),
                ),
            }
        ]
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    assert response.status_code == 200, response.text  # both fail here
    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover
