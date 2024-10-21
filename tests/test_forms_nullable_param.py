from typing import Optional
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()

default_uuid = uuid4()


@app.post("/form-optional/")
def post_form_optional(
    test_id: Annotated[Optional[UUID], Form(alias="testId")] = default_uuid,
) -> Optional[UUID]:
    return test_id


@app.post("/form-required/")
def post_form_required(
    test_id: Annotated[Optional[UUID], Form(alias="testId")],
) -> Optional[UUID]:
    return test_id


client = TestClient(app)


def test_unspecified_optional() -> None:
    response = client.post("/form-optional/", data={})
    assert response.status_code == 200, response.text
    assert response.json() == str(default_uuid)


def test_unspecified_required() -> None:
    response = client.post("/form-required/", data={})
    assert response.status_code == 422, response.text


@pytest.mark.parametrize("url", ["/form-optional/", "/form-required/"])
@pytest.mark.parametrize("test_id", [None, str(uuid4())])
def test_specified(url: str, test_id: Optional[str]) -> None:
    response = client.post(url, data={"testId": test_id})
    assert response.status_code == 200, response.text
    assert response.json() == test_id
