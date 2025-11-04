from typing import Annotated, Optional

import pytest
from dirty_equals import IsOneOf
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================================================================
# Field(alias=...)
# Current situation: fully works

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    param: str = Field(alias="param_alias")


@app.post("/required-field-alias-model")
async def required_field_alias_model(data: Annotated[RequiredFieldAliasModel, Form()]):
    return {"param": data.param}


def test_required_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias-model", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {"title": "Param Alias", "type": "string"}
    }


# ------------------------------
# optional field


class OptionalFieldAliasModel(BaseModel):
    param: Optional[str] = Field(None, alias="param_alias")


@app.post("/optional-field-alias-model")
async def optional_field_alias_model(data: Annotated[OptionalFieldAliasModel, Form()]):
    return {"param": data.param}


def test_optional_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", data={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias-model", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Alias",
        },
    }


# ------------------------------
# list field


class ListFieldAliasModel(BaseModel):
    param: list[str] = Field(alias="param_alias")


@app.post("/list-field-alias-model")
async def list_field_alias_model(data: Annotated[ListFieldAliasModel, Form()]):
    return {"param": data.param}


def test_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias-model", data={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias-model", data={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "title": "Param Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasModel(BaseModel):
    param: Optional[list[str]] = Field(None, alias="param_alias")


@app.post("/optional-list-field-alias-model")
async def optional_list_field_alias_model(
    data: Annotated[OptionalListFieldAliasModel, Form()],
):
    return {"param": data.param}


def test_optional_list_field_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-model", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# =====================================================================================
# Field(validation_alias=...)
# Current situation: works except lists


# ------------------------------
# required field


class RequiredFieldValidationAliasModel(BaseModel):
    param: str = Field(validation_alias="param_val_alias")


@app.post(
    "/required-field-validation-alias-model",
    operation_id="required_field_validation_alias_model",
)
async def required_field_validation_alias_model(
    data: Annotated[RequiredFieldValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_required_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-validation-alias-model", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias-model", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "param_val_alias": {"title": "Param Val Alias", "type": "string"}
    }


# ------------------------------
# optional field


class OptionalFieldValidationAliasModel(BaseModel):
    param: Optional[str] = Field(None, validation_alias="param_val_alias")


@app.post(
    "/optional-field-validation-alias-model",
    operation_id="optional_field_validation_alias_model",
)
async def optional_field_validation_alias_model(
    data: Annotated[OptionalFieldValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_optional_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-validation-alias-model", data={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias-model", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }


# ------------------------------
# list field


class ListFieldValidationAliasModel(BaseModel):
    param: list[str] = Field(validation_alias="param_val_alias")


@app.post(
    "/list-field-validation-alias-model",
    operation_id="list_field_validation_alias_model",
)
async def list_field_validation_alias_model(
    data: Annotated[ListFieldValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_list_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias-model", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias-model", data={"param_val_alias": ["123", "456"]}
    )
    assert resp.status_code == 200, resp.text
    # Currently fails due to some issue:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","param_val_alias"],"msg":"Input should be a valid list","input":"456"}]}

    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "items": {"type": "string"},
            "title": "Param Val Alias",
            "type": "array",
        }
    }


# ------------------------------
# optional list field


class OptionalListFieldValidationAliasModel(BaseModel):
    param: Optional[list[str]] = Field(None, validation_alias="param_val_alias")


@app.post(
    "/optional-list-field-validation-alias-model",
    operation_id="optional_list_field_validation_alias_model",
)
async def optional_list_field_validation_alias_model(
    data: Annotated[OptionalListFieldValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_optional_list_field_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias-model",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200, resp.text
    # Currently fails due to some issue:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","param_val_alias"],"msg":"Input should be a valid list","input":"456"}]}

    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalListFieldValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }


# =====================================================================================
# Field(alias=..., validation_alias=...)
# Current situation: works except lists

# ------------------------------
# required field


class RequiredFieldAliasAndValidationAliasModel(BaseModel):
    param: str = Field(alias="param_alias", validation_alias="param_val_alias")


@app.post(
    "/required-field-alias-and-validation-alias-model",
    operation_id="required_field_alias_and_validation_alias_model",
)
async def required_field_alias_and_validation_alias_model(
    data: Annotated[RequiredFieldAliasAndValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_required_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model", data={"param": "123"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model", data={"param_alias": "123"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias-model",
        data={"param_val_alias": "123"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "RequiredFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {"title": "Param Val Alias", "type": "string"}
    }


# ------------------------------
# optional field


class OptionalFieldAliasAndValidationAliasModel(BaseModel):
    param: Optional[str] = Field(
        None, alias="param_alias", validation_alias="param_val_alias"
    )


@app.post(
    "/optional-field-alias-and-validation-alias-model",
    operation_id="optional_field_alias_and_validation_alias_model",
)
async def optional_field_alias_and_validation_alias_model(
    data: Annotated[OptionalFieldAliasAndValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_optional_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model", data={"param": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model", data={"param_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias-model",
        data={"param_val_alias": "123"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Val Alias",
        }
    }


# ------------------------------
# list field


class ListFieldAliasAndValidationAliasModel(BaseModel):
    param: list[str] = Field(alias="param_alias", validation_alias="param_val_alias")


@app.post(
    "/list-field-alias-and-validation-alias-model",
    operation_id="list_field_alias_and_validation_alias_model",
)
async def list_field_alias_and_validation_alias_model(
    data: Annotated[ListFieldAliasAndValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_list_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


def test_list_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        data={"param_alias": ["123", "456"]},
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == IsOneOf(
        "Field required",
        "field required",  # TODO: remove when deprecating Pydantic v1
    )
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias-model",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200, resp.text
    # Currently fails due to some issue:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","param_val_alias"],"msg":"Input should be a valid list","input":"456"}]}

    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "ListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "items": {"type": "string"},
            "title": "Param Val Alias",
            "type": "array",
        }
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasAndValidationAliasModel(BaseModel):
    param: Optional[list[str]] = Field(
        None, alias="param_alias", validation_alias="param_val_alias"
    )


@app.post(
    "/optional-list-field-alias-and-validation-alias-model",
    operation_id="optional_list_field_alias_and_validation_alias_model",
)
async def optional_list_field_alias_and_validation_alias_model(
    data: Annotated[OptionalListFieldAliasAndValidationAliasModel, Form()],
):
    return {"param": data.param}


def test_optional_list_field_alias_and_validation_alias_model_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        data={"param": ["123", "456"]},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_and_validation_alias_model_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        data={"param_alias": ["123", "456"]},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"param": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_and_validation_alias_model_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias-model",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200, resp.text
    # Currently fails due to some issue:
    # AssertionError: assert 422 == 200
    # {"detail":[{"type":"list_type","loc":["body","param_val_alias"],"msg":"Input should be a valid list","input":"456"}]}

    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_and_validation_alias_model_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Val Alias",
        }
    }
