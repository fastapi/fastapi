import pytest
from fastapi import APIRouter


def test_router_circular_import():
    router = APIRouter()

    with pytest.raises(
        AssertionError,
        match="Cannot include the same APIRouter instance into itself. Did you mean to include a different router?",
    ):
        router.include_router(router)
