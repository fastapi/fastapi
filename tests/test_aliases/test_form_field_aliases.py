from typing import List, Optional

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient

from ..utils import needs_pydanticv2

pytestmark = needs_pydanticv2


app = FastAPI()

# =====================================================================================
# Form(alias=...)
# Current situation: Works, but schema is wrong

# ------------------------------
# required field


@app.post("/required-field-alias", operation_id="required_field_alias")
async def required_field_alias(param: str = Form(alias="param_alias")):
    return {"param": param}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_alias" in detail[0]["loc"]


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_required_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {"title": "Param Alias", "type": "string"}
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': {'type': 'string', 'title': 'Param'}} ==
    # {'param_alias': {'title': 'Param Alias', 'type': 'string'}}


# ------------------------------
# optional field


@app.post("/optional-field-alias", operation_id="optional_field_alias")
async def optional_field_alias(
    param: Optional[str] = Form(None, alias="param_alias"),
):
    return {"param": param}


def test_optional_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", data={"param": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/optional-field-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Alias",
        }
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'param': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'title': 'Param'}} ==
    # {'param_alias': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'title': 'Param Alias'}}


# ------------------------------
# list field


@app.post("/list-field-alias", operation_id="list_field_alias")
async def list_field_alias(param: List[str] = Form(alias="param_alias")):
    return {"param": param}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_alias" in detail[0]["loc"]


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "title": "Param Alias",
            "type": "array",
            "items": {"type": "string"},
        }
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'param': {'items': {'type': 'string'}, 'type': 'array', 'title': 'Param'}} ==
    # {'param_alias': {'title': 'Param Alias', 'type': 'array', 'items': {'type': 'string'}}}


# ------------------------------
# optional list field


@app.post("/optional-list-field-alias", operation_id="optional_list_field_alias")
async def optional_list_field_alias(
    param: Optional[List[str]] = Form(None, alias="param_alias"),
):
    return {"param": param}


def test_optional_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-list-field-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


def test_optional_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_list_field_alias"]
    assert body_schema["properties"] == {
        "param_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Alias",
        },
    }
    # Currently fails due to issue with aliases:
    # AssertionError: assert
    # {'param': {'anyOf': [{'items': {'type': 'string'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Param'}} ==
    # {'param_alias': {'anyOf': [{'items': {'type': 'string'}, 'type': 'array'}, {'type': 'null'}], 'title': 'Param Alias'}}


# =====================================================================================
# Form(validation_alias=...)
# Current situation: schema is correct, but doesn't work (parameter name is used)


# ------------------------------
# required field


@app.post(
    "/required-field-validation-alias", operation_id="required_field_validation_alias"
)
async def required_field_validation_alias(
    param: str = Form(validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-validation-alias", data={"param": "123"})
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"param": "123"}


def test_required_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {"title": "Param Val Alias", "type": "string"},
    }


# ------------------------------
# optional field


@app.post(
    "/optional-field-validation-alias", operation_id="optional_field_validation_alias"
)
async def optional_field_validation_alias(
    param: Optional[str] = Form(None, validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-validation-alias", data={"param": "123"})
    assert resp.json() == {"param": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': '123'} == {'param': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': None} == {'param': '123'}


def test_optional_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }


# ------------------------------
# list field


@app.post("/list-field-validation-alias", operation_id="list_field_validation_alias")
async def list_field_validation_alias(
    param: List[str] = Form(validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-validation-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias", data={"param_val_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_validation_alias"]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "items": {"type": "string"},
            "title": "Param Val Alias",
            "type": "array",
        },
    }


# ------------------------------
# optional list field


@app.post(
    "/optional-list-field-validation-alias",
    operation_id="optional_list_field_validation_alias",
)
async def optional_list_field_validation_alias(
    param: Optional[List[str]] = Form(None, validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': ['123', '456']} == {'param': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': None} == {'param': ['123', '456']}


def test_optional_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }


# =====================================================================================
# Form(alias=..., validation_alias=...)
# Current situation: Schema is correct (validation_alias), but doesn't work (alias is used)

# ------------------------------
# required field


@app.post(
    "/required-field-alias-and-validation-alias",
    operation_id="required_field_alias_and_validation_alias",
)
async def required_field_alias_and_validation_alias(
    param: str = Form(alias="param_alias", validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param": "123"}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]
    # Currently fails due to issue with aliases:
    # AssertionError: assert 'param_val_alias' in ['body', 'param_alias']


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param_alias": "123"}
    )
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_required_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"param": "123"}


def test_required_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {"title": "Param Val Alias", "type": "string"}
    }


# ------------------------------
# optional field


@app.post(
    "/optional-field-alias-and-validation-alias",
    operation_id="optional_field_alias_and_validation_alias",
)
async def optional_field_alias_and_validation_alias(
    param: Optional[str] = Form(
        None, alias="param_alias", validation_alias="param_val_alias"
    ),
):
    return {"param": param}


def test_optional_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': '123'} == {'param': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': None} == {'param': '123'}


def test_optional_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "title": "Param Val Alias",
        }
    }


# ------------------------------
# list field


@app.post(
    "/list-field-alias-and-validation-alias",
    operation_id="list_field_alias_and_validation_alias",
)
async def list_field_alias_and_validation_alias(
    param: List[str] = Form(alias="param_alias", validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]
    # Currently fails due to issue with aliases:
    # AssertionError: assert 'param_val_alias' in ['body', 'param_alias']


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 422
    # Currently fails due to issue with aliases:
    # AssertionError: assert 200 == 422

    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_val_alias" in detail[0]["loc"]


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    # Currently fails due to issue with aliases:
    # AssertionError: assert 422 == 200

    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_list_field_alias_and_validation_alias"
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


@app.post(
    "/optional-list-field-alias-and-validation-alias",
    operation_id="optional_list_field_alias_and_validation_alias",
)
async def optional_list_field_alias_and_validation_alias(
    param: Optional[List[str]] = Form(
        None, alias="param_alias", validation_alias="param_val_alias"
    ),
):
    return {"param": param}


def test_optional_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        data={"param": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        data={"param_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': ['123', '456']} == {'param': None}


@pytest.mark.xfail(raises=AssertionError, strict=False)
def test_optional_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}
    # Currently fails due to issue with aliases:
    # AssertionError: assert {'param': None} == {'param': ['123', '456']}


def test_optional_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_alias_and_validation_alias"
    ]
    assert body_schema["properties"] == {
        "param_val_alias": {
            "anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}],
            "title": "Param Val Alias",
        },
    }


# =====================================================================================
# Form(alias=..., validation_alias=...)  # alias == validation_alias
# The only working solution (current workaround)
# TODO: remove when issue with Form field aliases is fixed


@app.post("/workaround", operation_id="workaround")
async def workaround(
    param: str = Form(alias="param_alias", validation_alias="param_alias"),
):
    return {"param": param}


def test_workaround_by_name():
    client = TestClient(app)
    resp = client.post("/workaround", data={"param": "123"})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert detail[0]["msg"] == "Field required"
    assert "param_alias" in detail[0]["loc"]


def test_workaround_by_alias():
    client = TestClient(app)
    resp = client.post("/workaround", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_workaround_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_workaround"]
    assert body_schema["properties"] == {
        "param_alias": {"title": "Param Alias", "type": "string"}
    }
