from typing import Annotated

import pytest
from fastapi import APIRouter, Depends, FastAPI, Path, Query, Request
from fastapi.exceptions import FastAPIError
from pydantic import BaseModel


def test_additional_response_not_a_dict():
    app = FastAPI()

    with pytest.raises(FastAPIError, match="An additional response must be a dict"):

        @app.get("/items", responses={200: "not a dict"})  # ty: ignore[invalid-argument-type]
        async def get_items():
            pass  # pragma: no cover


def test_additional_response_body_not_allowed():
    app = FastAPI()

    class Item(BaseModel):
        name: str

    with pytest.raises(
        FastAPIError,
        match="Status code 204 must not have a response body",
    ):

        @app.get("/items", responses={204: {"model": Item}})
        async def get_items():
            pass  # pragma: no cover


def test_callable_endpoint_check():
    app = FastAPI()

    with pytest.raises(FastAPIError, match="An endpoint must be a callable"):
        app.router.add_api_route("/items", endpoint="not a callable")  # ty: ignore[invalid-argument-type]


def test_response_model_on_no_body_status():
    app = FastAPI()

    class Item(BaseModel):
        name: str

    with pytest.raises(
        FastAPIError,
        match="Status code 204 must not have a response body",
    ):

        @app.get("/items", response_model=Item, status_code=204)
        async def get_items():
            pass  # pragma: no cover


def test_apirouter_prefix_not_starting_with_slash():
    with pytest.raises(FastAPIError, match="A path prefix must start with '/'"):
        APIRouter(prefix="items")


def test_apirouter_prefix_ending_with_slash():
    with pytest.raises(
        FastAPIError,
        match="A path prefix must not end with '/'",
    ):
        APIRouter(prefix="/items/")


def test_include_router_prefix_not_starting_with_slash():
    router = APIRouter()
    child = APIRouter()
    with pytest.raises(FastAPIError, match="A path prefix must start with '/'"):
        router.include_router(child, prefix="items")


def test_include_router_prefix_ending_with_slash():
    router = APIRouter()
    child = APIRouter()
    with pytest.raises(
        FastAPIError,
        match="A path prefix must not end with '/'",
    ):
        router.include_router(child, prefix="/items/")


def test_fastapi_missing_title_for_openapi():
    with pytest.raises(
        FastAPIError,
        match="A title must be provided for OpenAPI",
    ):
        FastAPI(title="", version="1.0.0")


def test_fastapi_missing_version_for_openapi():
    with pytest.raises(
        FastAPIError,
        match="A version must be provided for OpenAPI",
    ):
        FastAPI(title="My API", version="")


def test_path_param_with_default_in_annotated():
    app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="Path parameters cannot have a default value",
    ):

        @app.get("/items/{item_id}")
        async def get_item(item_id: Annotated[int, Path(default=1)]):
            pass  # pragma: no cover


def test_annotated_annotation_with_fieldinfo_default():
    app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="Cannot specify FastAPI annotations in `Annotated` and default value",
    ):

        @app.get("/items")
        async def get_items(item_id: Annotated[int, Query()] = Query(default=1)):
            pass  # pragma: no cover


def test_query_for_path_param():
    app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="Cannot use `Query` for path param",
    ):

        @app.get("/items/{item_id}")
        async def get_item(item_id: Annotated[int, Query()]):
            pass  # pragma: no cover


def test_ujson_response_without_ujson():
    import fastapi.responses as responses_module

    original = responses_module.ujson
    try:
        responses_module.ujson = None
        with pytest.raises(ImportError, match="ujson must be installed"):
            responses_module.UJSONResponse.render(
                object.__new__(responses_module.UJSONResponse), {"key": "value"}
            )
    finally:
        responses_module.ujson = original


def test_orjson_response_without_orjson():
    import fastapi.responses as responses_module

    original = responses_module.orjson
    try:
        responses_module.orjson = None
        with pytest.raises(ImportError, match="orjson must be installed"):
            responses_module.ORJSONResponse.render(
                object.__new__(responses_module.ORJSONResponse), {"key": "value"}
            )
    finally:
        responses_module.orjson = original


def test_fastapi_annotation_on_request_type():
    app = FastAPI()

    with pytest.raises(
        FastAPIError,
        match="Cannot specify FastAPI annotation for type",
    ):

        @app.get("/items")
        async def get_items(request: Annotated[Request, Query()]):
            pass  # pragma: no cover


def test_depends_and_fieldinfo_default_together():
    app = FastAPI()

    async def dep():
        return 1  # pragma: no cover

    with pytest.raises(
        FastAPIError,
        match="Cannot specify `Depends` in `Annotated` and default value together",
    ):

        @app.get("/items")
        async def get_items(foo: Annotated[int, Depends(dep)] = Depends(dep)):
            pass  # pragma: no cover
