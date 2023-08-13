import pytest
from fastapi import Depends, FastAPI, Path
from fastapi.param_functions import Query
from typing_extensions import Annotated

app = FastAPI()


def test_no_annotated_defaults():
    with pytest.raises(
        AssertionError, match="Path parameters cannot have a default value"
    ):

        @app.get("/items/{item_id}/")
        async def get_item(item_id: Annotated[int, Path(default=1)]):
            pass  # pragma: nocover

    with pytest.raises(
        AssertionError,
        match=(
            "`Query` default value cannot be set in `Annotated` for 'item_id'. Set the"
            " default value with `=` instead."
        ),
    ):

        @app.get("/")
        async def get(item_id: Annotated[int, Query(default=1)]):
            pass  # pragma: nocover


def test_no_multiple_annotations():
    async def dep():
        pass  # pragma: nocover

    with pytest.raises(
        AssertionError,
        match="Cannot specify multiple `Annotated` FastAPI arguments for 'foo'",
    ):

        @app.get("/")
        async def get(foo: Annotated[int, Query(min_length=1), Query()]):
            pass  # pragma: nocover

    with pytest.raises(
        AssertionError,
        match=(
            "Cannot specify `Depends` in `Annotated` and default value"
            " together for 'foo'"
        ),
    ):

        @app.get("/")
        async def get2(foo: Annotated[int, Depends(dep)] = Depends(dep)):
            pass  # pragma: nocover

    with pytest.raises(
        AssertionError,
        match=(
            "Cannot specify a FastAPI annotation in `Annotated` and `Depends` as a"
            " default value together for 'foo'"
        ),
    ):

        @app.get("/")
        async def get3(foo: Annotated[int, Query(min_length=1)] = Depends(dep)):
            pass  # pragma: nocover
