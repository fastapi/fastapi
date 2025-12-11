from typing import List

import pytest
from dirty_equals import IsDict, IsOneOf, IsPartialDict
from fastapi import FastAPI, Form
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from tests.utils import needs_pydanticv2

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-list-str", operation_id="required_list_str")
async def read_required_list_str(p: Annotated[List[str], Form()]):
    return {"p": p}


class FormModelRequiredListStr(BaseModel):
    p: List[str]


@app.post("/model-required-list-str", operation_id="model_required_list_str")
def read_model_required_list_str(p: Annotated[FormModelRequiredListStr, Form()]):
    return {"p": p.p}


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p": {
                "items": {"type": "string"},
                "title": "P",
                "type": "array",
            },
        },
        "required": ["p"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/required-list-str", "/model-required-list-str"],
)
def test_required_list_str_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    ) | IsDict(
        {
            "detail": [
                {
                    "loc": ["body", "p"],
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
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 200
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Alias


@app.post("/required-list-alias", operation_id="required_list_alias")
async def read_required_list_alias(p: Annotated[List[str], Form(alias="p_alias")]):
    return {"p": p}


class FormModelRequiredListAlias(BaseModel):
    p: List[str] = Field(alias="p_alias")


@app.post("/model-required-list-alias", operation_id="model_required_list_alias")
async def read_model_required_list_alias(
    p: Annotated[FormModelRequiredListAlias, Form()],
):
    return {"p": p.p}  # pragma: no cover


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/required-list-alias",
            marks=pytest.mark.xfail(
                raises=AssertionError,
                condition=PYDANTIC_V2,
                reason="Fails only with PDv2 models",
                strict=False,
            ),
        ),
        "/model-required-list-alias",
    ],
)
def test_required_list_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_alias": {
                "items": {"type": "string"},
                "title": "P Alias",
                "type": "array",
            },
        },
        "required": ["p_alias"],
        "title": body_model_name,
        "type": "object",
    }


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
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
                    "loc": ["body", "p_alias"],
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
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
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
                    "loc": ["body", "p_alias"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@pytest.mark.parametrize(
    "path",
    ["/required-list-alias", "/model-required-list-alias"],
)
def test_required_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text
    assert response.json() == {"p": ["hello", "world"]}


# =====================================================================================
# Validation alias


@app.post(
    "/required-list-validation-alias", operation_id="required_list_validation_alias"
)
def read_required_list_validation_alias(
    p: Annotated[List[str], Form(validation_alias="p_val_alias")],
):
    return {"p": p}


class FormModelRequiredListValidationAlias(BaseModel):
    p: List[str] = Field(validation_alias="p_val_alias")


@app.post(
    "/model-required-list-validation-alias",
    operation_id="model_required_list_validation_alias",
)
async def read_model_required_list_validation_alias(
    p: Annotated[FormModelRequiredListValidationAlias, Form()],
):
    return {"p": p.p}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    ["/required-list-validation-alias", "/model-required-list-validation-alias"],
)
def test_required_list_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "items": {"type": "string"},
                "title": "P Val Alias",
                "type": "array",
            },
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
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
def test_required_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
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
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 422, (
        response.text  # /required-list-validation-alias fails here
    )

    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
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
    response = client.post(path, data={"p_val_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text  # both fail here

    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-list-alias-and-validation-alias",
    operation_id="required_list_alias_and_validation_alias",
)
def read_required_list_alias_and_validation_alias(
    p: Annotated[List[str], Form(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class FormModelRequiredListAliasAndValidationAlias(BaseModel):
    p: List[str] = Field(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-list-alias-and-validation-alias",
    operation_id="model_required_list_alias_and_validation_alias",
)
def read_model_required_list_alias_and_validation_alias(
    p: Annotated[FormModelRequiredListAliasAndValidationAlias, Form()],
):
    return {"p": p.p}  # pragma: no cover


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        "/required-list-alias-and-validation-alias",
        "/model-required-list-alias-and-validation-alias",
    ],
)
def test_required_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    assert app.openapi()["components"]["schemas"][body_model_name] == {
        "properties": {
            "p_val_alias": {
                "items": {"type": "string"},
                "title": "P Val Alias",
                "type": "array",
            },
        },
        "required": ["p_val_alias"],
        "title": body_model_name,
        "type": "object",
    }


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
    response = client.post(path)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
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
    response = client.post(path, data={"p": ["hello", "world"]})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    # /required-list-alias-and-validation-alias fails here
                    "p_val_alias",
                ],
                "msg": "Field required",
                "input": IsOneOf(
                    None,
                    # /model-required-list-alias-and-validation-alias fails here
                    {"p": ["hello", "world"]},
                ),
            }
        ]
    }


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
def test_required_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": ["hello", "world"]})
    assert (  # /required-list-alias-and-validation-alias fails here
        response.status_code == 422
    )
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "p_val_alias"],
                "msg": "Field required",
                "input": IsOneOf(None, {"p_alias": ["hello", "world"]}),
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
    response = client.post(path, data={"p_val_alias": ["hello", "world"]})
    assert response.status_code == 200, response.text  # both fail here
    assert response.json() == {"p": ["hello", "world"]}  # pragma: no cover
