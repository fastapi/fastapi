from typing import Annotated

import pytest
from fastapi import Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class DefaultModel(BaseModel):
    field_1: bool = True


class InvalidDefaultModel(BaseModel):
    field_1: Annotated[str, Field(default=0)]


@app.get("/query")
def read_query(model: Annotated[DefaultModel, Query()]) -> dict[str, object]:
    return {"fields_set": sorted(model.model_fields_set), "model": model.model_dump()}


@app.get("/header")
def read_header(model: Annotated[DefaultModel, Header()]) -> dict[str, object]:
    return {"fields_set": sorted(model.model_fields_set), "model": model.model_dump()}


@app.get("/cookie")
def read_cookie(model: Annotated[DefaultModel, Cookie()]) -> dict[str, object]:
    return {"fields_set": sorted(model.model_fields_set), "model": model.model_dump()}


@app.post("/form")
def read_form(model: Annotated[DefaultModel, Form()]) -> dict[str, object]:
    return {"fields_set": sorted(model.model_fields_set), "model": model.model_dump()}


@app.post("/body-invalid-default")
def read_body_invalid_default(model: InvalidDefaultModel) -> dict[str, list[str]]:
    return {"fields_set": sorted(model.model_fields_set)}


@app.post("/form-invalid-default")
def read_form_invalid_default(
    model: Annotated[InvalidDefaultModel, Form()],
) -> dict[str, list[str]]:
    return {"fields_set": sorted(model.model_fields_set)}


client = TestClient(app)


@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("get", "/query", {}),
        ("get", "/header", {}),
        ("get", "/cookie", {}),
        ("post", "/form", {"data": {}}),
    ],
)
def test_missing_model_defaults_not_marked_as_set(
    method: str, path: str, kwargs: dict[str, object]
) -> None:
    response = getattr(client, method)(path, **kwargs)

    assert response.status_code == 200, response.text
    assert response.json() == {
        "fields_set": [],
        "model": {"field_1": True},
    }


def test_explicit_form_model_value_is_still_marked_as_set() -> None:
    response = client.post("/form", data={"field_1": "false"})

    assert response.status_code == 200, response.text
    assert response.json() == {
        "fields_set": ["field_1"],
        "model": {"field_1": False},
    }


@pytest.mark.parametrize(
    "path",
    ["/body-invalid-default", "/form-invalid-default"],
)
def test_omitted_invalid_defaults_do_not_trigger_validation(path: str) -> None:
    if path == "/body-invalid-default":
        response = client.post(path, json={})
    else:
        response = client.post(path, data={})

    assert response.status_code == 200, response.text
    assert response.json() == {"fields_set": []}
