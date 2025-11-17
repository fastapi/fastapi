from typing import List

import pytest
from dirty_equals import IsDict, IsOneOf
from fastapi import FastAPI, Query
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from tests.utils import needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-list-str")
async def read_required_list_str(p: List[str] = Query(...)):
    return {"p": p}


class QueryModelRequiredListStr(BaseModel):
    p: List[str]


@app.get("/model-required-list-str")
def read_model_required_list_str(p: QueryModelRequiredListStr = Query()):
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
            "in": "query",
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
                    "loc": ["query", "p"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "loc": ["query", "p"],
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
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.get("/required-list-alias")
async def read_required_list_alias(p: List[str] = Query(..., alias="p_alias")):
    return {"p": p}


class QueryModelRequiredListAlias(BaseModel):
    p: List[str] = Field(..., alias="p_alias")


@app.get("/model-required-list-alias")
async def read_model_required_list_alias(p: QueryModelRequiredListAlias = Query()):
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
            "in": "query",
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
                    "loc": ["query", "p_alias"],
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
                    "loc": ["query", "p_alias"],
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
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(  # /model-required-list-alias with PDv2 fails here
                        None, {"p": ["hello", "world"]}
                    ),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "p_alias"],
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
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    assert response.status_code == 200, (  # /model-required-list-alias fails here
        response.text
    )
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.get("/required-list-validation-alias")
def read_required_list_validation_alias(
    p: List[str] = Query(..., validation_alias="p_val_alias"),
):
    return {"p": p}


class QueryModelRequiredListValidationAlias(BaseModel):
    p: List[str] = Field(..., validation_alias="p_val_alias")


@app.get("/model-required-list-validation-alias")
async def read_model_required_list_validation_alias(
    p: QueryModelRequiredListValidationAlias = Query(),
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
            "in": "query",
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
                    "query",
                    "p_val_alias",  # /required-list-validation-alias fails here
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
            "/required-list-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-required-list-validation-alias",
    ],
)
def test_required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    assert response.status_code == 422  # /required-list-validation-alias fails here

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


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    assert response.status_code == 200, response.text  # both fail here

    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover


# =====================================================================================
# Alias and validation alias


@app.get("/required-list-alias-and-validation-alias")
def read_required_list_alias_and_validation_alias(
    p: List[str] = Query(..., alias="p_alias", validation_alias="p_val_alias"),
):
    return {"p": p}


class QueryModelRequiredListAliasAndValidationAlias(BaseModel):
    p: List[str] = Field(..., alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-list-alias-and-validation-alias")
def read_model_required_list_alias_and_validation_alias(
    p: QueryModelRequiredListAliasAndValidationAlias = Query(),
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
            "in": "query",
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
                    "query",
                    # /required-list-alias-and-validation-alias fails here
                    "p_val_alias",
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
                    # /required-list-alias-and-validation-alias fails here
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-required-list-alias-and-validation-alias fails here
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
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    assert (  # /required-list-alias-and-validation-alias fails here
        response.status_code == 422
    )
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-required-list-alias-and-validation-alias fails here
                    {"p_alias": ["hello", "world"]},
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
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    assert response.status_code == 200, response.text  # both fail here
    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover
