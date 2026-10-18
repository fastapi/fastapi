from typing import Annotated

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


@app.get("/parameter")
def read_parameter(int_val: Annotated[int | None, Header()]):
    return int_val


class Model(BaseModel):
    int_val: int | None


@app.get("/model")
def read_model(params: Annotated[Model, Header()]):
    return params.int_val


client = TestClient(app)


@pytest.mark.parametrize("path", ["/parameter", "/model"])
def test_nullable_header_uses_hyphenated_name(path):
    response = client.get(path, headers={"int-val": "0"})
    assert response.status_code == 200
    assert response.json() == 0
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    field = response.json()["paths"][path]["get"]["parameters"][0]
    assert field["name"] == "int-val"
    assert field["in"] == "header"
    assert field["required"] is True
    assert field["schema"]["anyOf"] == [{"type": "integer"}, {"type": "null"}]


@pytest.mark.parametrize(
    "path",
    [
        "/parameter",
        pytest.param(
            "/model",
            marks=pytest.mark.xfail(
                reason="Header model errors use underscores instead of hyphens",
                raises=AssertionError,
            ),
        ),
    ],
)
@pytest.mark.parametrize(
    "headers,error_type",
    [({}, "missing"), ({"int-val": "invalid"}, "int_parsing")],
)
def test_nullable_header_error_uses_hyphenated_name(path, headers, error_type):
    response = client.get(path, headers=headers)
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        (error_type, ["header", "int-val"]),
    ]
