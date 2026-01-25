from typing import Annotated

import pytest
from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/required-str/{p}")
async def read_required_str(p: Annotated[str, Path()]):
    return {"p": p}


@app.get("/required-alias/{p_alias}")
async def read_required_alias(p: Annotated[str, Path(alias="p_alias")]):
    return {"p": p}


@app.get("/required-validation-alias/{p_val_alias}")
def read_required_validation_alias(
    p: Annotated[str, Path(validation_alias="p_val_alias")],
):
    return {"p": p}


@app.get("/required-alias-and-validation-alias/{p_val_alias}")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Path(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


@pytest.mark.parametrize(
    ("path", "expected_name", "expected_title"),
    [
        pytest.param("/required-str/{p}", "p", "P", id="required-str"),
        pytest.param(
            "/required-alias/{p_alias}", "p_alias", "P Alias", id="required-alias"
        ),
        pytest.param(
            "/required-validation-alias/{p_val_alias}",
            "p_val_alias",
            "P Val Alias",
            id="required-validation-alias",
        ),
        pytest.param(
            "/required-alias-and-validation-alias/{p_val_alias}",
            "p_val_alias",
            "P Val Alias",
            id="required-alias-and-validation-alias",
        ),
    ],
)
def test_schema(path: str, expected_name: str, expected_title: str):
    assert app.openapi()["paths"][path]["get"]["parameters"] == [
        {
            "required": True,
            "schema": {"title": expected_title, "type": "string"},
            "name": expected_name,
            "in": "path",
        }
    ]


@pytest.mark.parametrize(
    "path",
    [
        pytest.param("/required-str", id="required-str"),
        pytest.param("/required-alias", id="required-alias"),
        pytest.param(
            "/required-validation-alias",
            id="required-validation-alias",
        ),
        pytest.param(
            "/required-alias-and-validation-alias",
            id="required-alias-and-validation-alias",
        ),
    ],
)
def test_success(path: str):
    client = TestClient(app)
    response = client.get(f"{path}/hello")
    assert response.status_code == 200, response.text
    assert response.json() == {"p": "hello"}
