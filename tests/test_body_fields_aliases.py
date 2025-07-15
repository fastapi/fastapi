from pydantic import Field
import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient


app = FastAPI()

# =====================================================================================
# Form alias
# Current situation: Works, but schema is wrong


@app.post("/form-alias", operation_id="form_alias")
async def form_alias(param: str = Form(alias="param_alias")):
    return {"param": param}


def test_form_alias_by_name():
    client = TestClient(app)
    resp = client.post("/form-alias", data={"param": "123"})
    assert resp.status_code == 422


def test_form_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/form-alias", data={"param_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


@pytest.mark.xfail
def test_form_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_form_alias"]
    assert len(body_schema["properties"]) == 1
    assert "param_alias" in body_schema["properties"]


# =====================================================================================
# Form validation alias
# Current situation: schema is correct, but doesn't work (name is used)


@app.post("/form-validation-alias", operation_id="form_validation_alias")
async def form_validation_alias(param: str = Form(validation_alias="param_val_alias")):
    return {"param": param}


@pytest.mark.xfail
def test_form_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/form-validation-alias", data={"param": "123"})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_form_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/form-validation-alias", data={"param_val_alias": "123"})
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_form_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"]["Body_form_validation_alias"]
    print(body_schema)
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# alias and validation alias
# Current situation: Schema is correct (val_alias), but doesn't work (alias is used)


@app.post(
    "/form-alias-and-validation-alias", operation_id="form_alias_and_validation_alias"
)
async def form_alias_and_validation_alias(
    param: str = Form(alias="param_alias", validation_alias="param_val_alias"),
):
    return {"param": param}


def test_form_alias_and_validation_alias_by_name():
    client = TestClient(app)
    resp = client.post("/form-alias-and-validation-alias", data={"param": "123"})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_form_alias_and_validation_alias_by_alias():
    client = TestClient(app)
    resp = client.post("/form-alias-and-validation-alias", data={"param_alias": "123"})
    assert resp.status_code == 422


@pytest.mark.xfail
def test_form_alias_and_validation_alias_by_validation_alias():
    client = TestClient(app)
    resp = client.post(
        "/form-alias-and-validation-alias", data={"param_val_alias": "123"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"param": "123"}


def test_form_alias_and_validation_alias_schema():
    openapi = app.openapi()
    body_schema = openapi["components"]["schemas"][
        "Body_form_alias_and_validation_alias"
    ]
    print(body_schema)
    assert len(body_schema["properties"]) == 1
    assert "param_val_alias" in body_schema["properties"]


# alias_priority - not supported officially, but probably works with Pydantic V2
# alias_choices?

{
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/form-alias": {
            "post": {
                "summary": "Form Alias",
                "operationId": "form_alias_form_alias_post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_form_alias_form_alias_post"
                            }
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_form_alias_form_alias_post": {
                "properties": {"param": {"type": "string", "title": "Param"}},
                "type": "object",
                "required": ["param"],
                "title": "Body_form_alias_form_alias_post",
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "type": "array",
                        "title": "Detail",
                    }
                },
                "type": "object",
                "title": "HTTPValidationError",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                        "type": "array",
                        "title": "Location",
                    },
                    "msg": {"type": "string", "title": "Message"},
                    "type": {"type": "string", "title": "Error Type"},
                },
                "type": "object",
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
            },
        }
    },
}
