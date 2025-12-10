from typing import List, Optional

import pytest
from dirty_equals import IsDict
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from tests.utils import needs_pydanticv2

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-list-str")
async def read_optional_list_str(
    p: Annotated[Optional[List[str]], Header()] = None,
):
    return {"p": p}


class HeaderModelOptionalListStr(BaseModel):
    p: Optional[List[str]] = None


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
        IsDict(
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
        )
        | IsDict(
            # TODO: remove when deprecating Pydantic v1
            {
                "required": False,
                "schema": {"items": {"type": "string"}, "type": "array", "title": "P"},
                "name": "p",
                "in": "header",
            }
        )
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
    p: Annotated[Optional[List[str]], Header(alias="p_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListAlias(BaseModel):
    p: Optional[List[str]] = Field(None, alias="p_alias")


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
        IsDict(
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
        )
        | IsDict(
            # TODO: remove when deprecating Pydantic v1
            {
                "required": False,
                "schema": {
                    "items": {"type": "string"},
                    "type": "array",
                    "title": "P Alias",
                },
                "name": "p_alias",
                "in": "header",
            }
        )
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
        pytest.param(
            "/model-optional-list-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
    ],
)
def test_optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    assert response.status_code == 200
    assert response.json() == {
        "p": ["hello", "world"]  # /model-optional-list-alias fails here
    }


# =====================================================================================
# Validation alias


@app.get("/optional-list-validation-alias")
def read_optional_list_validation_alias(
    p: Annotated[Optional[List[str]], Header(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListValidationAlias(BaseModel):
    p: Optional[List[str]] = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-list-validation-alias")
def read_model_optional_list_validation_alias(
    p: Annotated[HeaderModelOptionalListValidationAlias, Header()],
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"p": None}


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-list-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-list-validation-alias",
    ],
)
def test_optional_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    assert response.status_code == 200
    assert response.json() == {"p": None}  # /optional-list-validation-alias fails here


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
@pytest.mark.parametrize(
    "path",
    ["/optional-list-validation-alias", "/model-optional-list-validation-alias"],
)
def test_optional_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    assert response.status_code == 200, (
        response.text  # /model-optional-list-validation-alias fails here
    )
    assert response.json() == {  # /optional-list-validation-alias fails here
        "p": ["hello", "world"]
    }


# =====================================================================================
# Alias and validation alias


@app.get("/optional-list-alias-and-validation-alias")
def read_optional_list_alias_and_validation_alias(
    p: Annotated[
        Optional[List[str]], Header(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class HeaderModelOptionalListAliasAndValidationAlias(BaseModel):
    p: Optional[List[str]] = Field(
        None, alias="p_alias", validation_alias="p_val_alias"
    )


@app.get("/model-optional-list-alias-and-validation-alias")
def read_model_optional_list_alias_and_validation_alias(
    p: Annotated[HeaderModelOptionalListAliasAndValidationAlias, Header()],
):
    return {"p": p.p}


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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


@needs_pydanticv2
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


@needs_pydanticv2
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


@needs_pydanticv2
@pytest.mark.parametrize(
    "path",
    [
        pytest.param(
            "/optional-list-alias-and-validation-alias",
            marks=pytest.mark.xfail(raises=AssertionError, strict=False),
        ),
        "/model-optional-list-alias-and-validation-alias",
    ],
)
def test_optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    assert response.status_code == 200
    assert response.json() == {
        "p": None  # /optional-list-alias-and-validation-alias fails here
    }


@needs_pydanticv2
@pytest.mark.xfail(raises=AssertionError, strict=False)
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
    assert response.status_code == 200, (
        response.text  # /model-optional-list-alias-and-validation-alias fails here
    )
    assert response.json() == {
        "p": [  # /optional-list-alias-and-validation-alias fails here
            "hello",
            "world",
        ]
    }
