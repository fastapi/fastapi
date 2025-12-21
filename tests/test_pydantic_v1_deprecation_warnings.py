import sys

import pytest

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

from fastapi import FastAPI
from fastapi._compat.v1 import BaseModel
from fastapi.testclient import TestClient


def test_warns_pydantic_v1_model_in_endpoint_param() -> None:
    class ParamModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.warns(
        DeprecationWarning,
        match=r"pydantic\.v1 is deprecated.*Please update the param data:",
    ):

        @app.post("/param")
        def endpoint(data: ParamModelV1):
            return data

    client = TestClient(app)
    response = client.post("/param", json={"name": "test"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "test"}


def test_warns_pydantic_v1_model_in_return_type() -> None:
    class ReturnModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.warns(
        DeprecationWarning,
        match=r"pydantic\.v1 is deprecated.*Please update the response model",
    ):

        @app.get("/return")
        def endpoint() -> ReturnModelV1:
            return ReturnModelV1(name="test")

    client = TestClient(app)
    response = client.get("/return")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "test"}


def test_warns_pydantic_v1_model_in_response_model() -> None:
    class ResponseModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.warns(
        DeprecationWarning,
        match=r"pydantic\.v1 is deprecated.*Please update the response model",
    ):

        @app.get("/response-model", response_model=ResponseModelV1)
        def endpoint():
            return {"name": "test"}

    client = TestClient(app)
    response = client.get("/response-model")
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "test"}


def test_warns_pydantic_v1_model_in_additional_responses_model() -> None:
    class ErrorModelV1(BaseModel):
        detail: str

    app = FastAPI()

    with pytest.warns(
        DeprecationWarning,
        match=r"pydantic\.v1 is deprecated.*In responses=\{\}, please update",
    ):

        @app.get(
            "/responses", response_model=None, responses={400: {"model": ErrorModelV1}}
        )
        def endpoint():
            return {"ok": True}

    client = TestClient(app)
    response = client.get("/responses")
    assert response.status_code == 200, response.text
    assert response.json() == {"ok": True}
