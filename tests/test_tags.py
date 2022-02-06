import pytest
from fastapi import APIRouter, FastAPI


def test_string_is_invalid_in_router_tags():
    with pytest.raises(AssertionError):
        router = APIRouter(tags="test")

def test_string_is_invalid_in_router_route_tags():
    router = APIRouter()

    with pytest.raises(AssertionError):
        @router.get("", tags="test")
        def test():
            ...


def test_string_is_invalid_in_include_router_tags():
    app = FastAPI()
    router = APIRouter()

    @router.get("")
    def test():
        ...

    with pytest.raises(AssertionError):
        app.include_router(router, prefix="/test", tags="test")