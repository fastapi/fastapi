from typing import List, Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from ..utils import needs_pydanticv2

pytestmark = needs_pydanticv2


app = FastAPI()

# =====================================================================================
# Pydantic model with Field(alias=...)

# ------------------------------
# required field


class RequiredFieldAliasModel(BaseModel):
    param: str = Field(alias="param_alias")


@app.post("/required-field-alias", operation_id="required_field_alias")
async def required_field_alias(body: RequiredFieldAliasModel):
    return {"param": body.param}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", json={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", json={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {"type": "string", "title": "Param Alias"}
    }


# ------------------------------
# optional field


class OptionalFieldAliasModel(BaseModel):
    param: Optional[str] = Field(None, alias="param_alias")


@app.post("/optional-field-alias", operation_id="optional_field_alias")
async def optional_field_alias(body: OptionalFieldAliasModel):
    return {"param": body.param}


def test_optional_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", json={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", json={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_schema():
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
    param: List[str] = Field(alias="param_alias")


@app.post("/list-field-alias", operation_id="list_field_alias")
async def list_field_alias(body: ListFieldAliasModel):
    return {"param": body.param}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias", json={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias", json={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "items": {"type": "string"},
            "type": "array",
            "title": "Param Alias",
        }
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasModel(BaseModel):
    param: Optional[List[str]] = Field(None, alias="param_alias")


@app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
async def optional_list_field_alias(body: OptionalListFieldAliasModel):
    return {"param": body.param}


def test_optional_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-list-field-alias", json={"param": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias", json={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["OptionalListFieldAliasModel"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Alias",
        },
    }


# =====================================================================================
# Pydantic model with Field(validation_alias=...)

# ------------------------------
# required field


class RequiredFieldValidationAliasModel(BaseModel):
    param: str = Field(validation_alias="param_val_alias")


@app.post(
    "/required-field-validation-alias", operation_id="required_field_validation_alias"
)
async def required_field_validation_alias(body: RequiredFieldValidationAliasModel):
    return {"param": body.param}


def test_required_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-validation-alias", json={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias", json={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["RequiredFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "param_val_alias": {"title": "Param Val Alias", "type": "string"},
    }


# ------------------------------
# optional field


class OptionalFieldValidationAliasModel(BaseModel):
    param: Optional[str] = Field(None, validation_alias="param_val_alias")


@app.post(
    "/optional-field-validation-alias", operation_id="optional_field_validation_alias"
)
async def optional_field_validation_alias(body: OptionalFieldValidationAliasModel):
    return {"param": body.param}


def test_optional_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-validation-alias", json={"param": "123"})
    assert resp.json() == {"param": None}


def test_optional_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias", json={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_validation_alias_schema():
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
    param: List[str] = Field(validation_alias="param_val_alias")


@app.post("/list-field-validation-alias", operation_id="list_field_validation_alias")
async def list_field_validation_alias(body: ListFieldValidationAliasModel):
    return {"param": body.param}


def test_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-validation-alias", json={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias", json={"param_val_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["ListFieldValidationAliasModel"]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "items": {"type": "string"},
            "title": "Param Val Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


class OptionalListFieldValidationAliasModel(BaseModel):
    param: Optional[List[str]] = Field(None, validation_alias="param_val_alias")


@app.post(
    "/optional-list-field-validation-alias",
    operation_id="optional_list_field_validation_alias",
)
async def optional_list_field_validation_alias(
    body: OptionalListFieldValidationAliasModel,
):
    return {"param": body.param}


def test_optional_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias", json={"param": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias",
        json={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_validation_alias_schema():
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
# Pydantic model with Field(alias=..., validation_alias=...)

# ------------------------------
# required field


class RequiredFieldAliasAndValidationAliasModel(BaseModel):
    param: str = Field(alias="param_alias", validation_alias="param_val_alias")


@app.post(
    "/required-field-alias-and-validation-alias",
    operation_id="required_field_alias_and_validation_alias",
)
async def required_field_alias_and_validation_alias(
    body: RequiredFieldAliasAndValidationAliasModel,
):
    return {"param": body.param}


def test_required_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", json={"param": "123"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", json={"param_alias": "123"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_required_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", json={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_and_validation_alias_schema():
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
    "/optional-field-alias-and-validation-alias",
    operation_id="optional_field_alias_and_validation_alias",
)
async def optional_field_alias_and_validation_alias(
    body: OptionalFieldAliasAndValidationAliasModel,
):
    return {"param": body.param}


def test_optional_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", json={"param": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", json={"param_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", json={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_and_validation_alias_schema():
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
    param: List[str] = Field(alias="param_alias", validation_alias="param_val_alias")


@app.post(
    "/list-field-alias-and-validation-alias",
    operation_id="list_field_alias_and_validation_alias",
)
async def list_field_alias_and_validation_alias(
    body: ListFieldAliasAndValidationAliasModel,
):
    return {"param": body.param}


def test_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", json={"param": ["123", "456"]}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", json={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


def test_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        json={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "ListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "items": {"type": "string"},
            "title": "Param Val Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


class OptionalListFieldAliasAndValidationAliasModel(BaseModel):
    param: Optional[List[str]] = Field(
        None, alias="param_alias", validation_alias="param_val_alias"
    )


@app.post(
    "/optional-list-field-alias-and-validation-alias",
    operation_id="optional_list_field_alias_and_validation_alias",
)
async def optional_list_field_alias_and_validation_alias(
    body: OptionalListFieldAliasAndValidationAliasModel,
):
    return {"param": body.param}


def test_optional_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        json={"param": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        json={"param_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        json={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "OptionalListFieldAliasAndValidationAliasModel"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }
