import sys
import warnings
from typing import Union

import pytest

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

from fastapi import FastAPI
from fastapi.exceptions import PydanticV1NotSupportedError

with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    from pydantic.v1 import BaseModel


def test_raises_pydantic_v1_model_in_endpoint_param() -> None:
    class ParamModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.post("/param")
        def endpoint(data: ParamModelV1):  # pragma: no cover
            return data


def test_raises_pydantic_v1_model_in_return_type() -> None:
    class ReturnModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.get("/return")
        def endpoint() -> ReturnModelV1:  # pragma: no cover
            return ReturnModelV1(name="test")


def test_raises_pydantic_v1_model_in_response_model() -> None:
    class ResponseModelV1(BaseModel):
        name: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.get("/response-model", response_model=ResponseModelV1)
        def endpoint():  # pragma: no cover
            return {"name": "test"}


def test_raises_pydantic_v1_model_in_additional_responses_model() -> None:
    class ErrorModelV1(BaseModel):
        detail: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.get(
            "/responses", response_model=None, responses={400: {"model": ErrorModelV1}}
        )
        def endpoint():  # pragma: no cover
            return {"ok": True}


def test_raises_pydantic_v1_model_in_union() -> None:
    class ModelV1A(BaseModel):
        name: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.post("/union")
        def endpoint(data: Union[dict, ModelV1A]):  # pragma: no cover
            return data


def test_raises_pydantic_v1_model_in_sequence() -> None:
    class ModelV1A(BaseModel):
        name: str

    app = FastAPI()

    with pytest.raises(PydanticV1NotSupportedError):

        @app.post("/sequence")
        def endpoint(data: list[ModelV1A]):  # pragma: no cover
            return data
