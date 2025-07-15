from typing import Optional

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient

app = FastAPI()

# =====================================================================================
# alias
# Current situation: Works, but schema is wrong

# ------------------------------
# required field


@app.post("/required-field-alias")
async def required_field_alias(param: str = Form(alias="param_alias")):
    return {"param": param}


def test_required_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param": "123"})
    assert resp.status_code == 422


def test_required_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/required-field-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


@pytest.mark.xfail
def test_required_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_required_field_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# ------------------------------
# optional field


@app.post("/optional-field-alias")
async def optional_field_alias(param: Optional[str] = Form(None, alias="param_alias")):
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


@pytest.mark.xfail
def test_optional_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_field_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# ------------------------------
# list field


@app.post("/list-field-alias")
async def list_field_alias(param: list[str] = Form(alias="param_alias")):
    return {"param": param}


def test_list_field_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 422


def test_list_field_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/list-field-alias", data={"param_alias": ["123", "456"]})
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


@pytest.mark.xfail
def test_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# ------------------------------
# optional list field


@app.post("/optional-list-field-alias")
async def optional_list_field_alias(
    param: Optional[list[str]] = Form(None, alias="param_alias"),
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


@pytest.mark.xfail
def test_optional_list_field_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_optional_list_field_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# =====================================================================================
# validation alias
# Current situation: schema is correct, but doesn't work (name is used)


# ------------------------------
# required field


@app.post(
    "/required-field-validation-alias", operation_id="required_field_validation_alias"
)
async def required_field_validation_alias(
    param: str = Form(validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail
def test_required_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/required-field-validation-alias", data={"param": "123"})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_required_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_validation_alias"
    ]
    print(body_schema)
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# optional field


@app.post(
    "/optional-field-validation-alias", operation_id="optional_field_validation_alias"
)
async def optional_field_validation_alias(
    param: Optional[str] = Form(None, validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail
def test_optional_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/optional-field-validation-alias", data={"param": "123"})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_optional_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# list field


@app.post("/list-field-validation-alias", operation_id="list_field_validation_alias")
async def list_field_validation_alias(
    param: list[str] = Form(validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail
def test_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/list-field-validation-alias", data={"param": ["123", "456"]})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-validation-alias", data={"param_val_alias": ["123", "456"]}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_list_field_validation_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# optional list field


@app.post(
    "/optional-list-field-validation-alias",
    operation_id="optional_list_field_validation_alias",
)
async def optional_list_field_validation_alias(
    param: Optional[list[str]] = Form(None, validation_alias="param_val_alias"),
):
    return {"param": param}


@pytest.mark.xfail
def test_optional_list_field_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_optional_list_field_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# =====================================================================================
# alias and validation alias
# Current situation: Schema is correct (val_alias), but doesn't work (alias is used)

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


def test_required_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param": "123"}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_required_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param_alias": "123"}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_required_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/required-field-alias-and-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_required_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_required_field_alias_and_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# optional field


@app.post(
    "/optional-field-alias-and-validation-alias",
    operation_id="optional_field_alias_and_validation_alias",
)
async def optional_field_alias_and_validation_alias(
    param: str = Form(None, alias="param_alias", validation_alias="param_val_alias"),
):
    return {"param": param}


def test_optional_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": None}


@pytest.mark.xfail
def test_optional_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param_alias": "123"}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_optional_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-field-alias-and-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_optional_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_field_alias_and_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# list field


@app.post(
    "/list-field-alias-and-validation-alias",
    operation_id="list_field_alias_and_validation_alias",
)
async def list_field_alias_and_validation_alias(
    param: list[str] = Form(alias="param_alias", validation_alias="param_val_alias"),
):
    return {"param": param}


def test_list_field_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", data={"param": ["123", "456"]}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias", data={"param_alias": ["123", "456"]}
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/list-field-alias-and-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_list_field_alias_and_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# ------------------------------
# optional list field


@app.post(
    "/optional-list-field-alias-and-validation-alias",
    operation_id="optional_list_field_alias_and_validation_alias",
)
async def optional_list_field_alias_and_validation_alias(
    param: Optional[list[str]] = Form(
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


@pytest.mark.xfail
def test_optional_list_field_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        data={"param_alias": ["123", "456"]},
    )
    assert resp.status_code == 422


@pytest.mark.xfail
def test_optional_list_field_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/optional-list-field-alias-and-validation-alias",
        data={"param_val_alias": ["123", "456"]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": ["123", "456"]}


def test_optional_list_field_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_optional_list_field_alias_and_validation_alias"
    ]
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]
