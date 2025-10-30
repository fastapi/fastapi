import pytest
from fastapi import APIRouter


def test_router_circular_import():
    router = APIRouter()

    with pytest.raises(AssertionError, match="Cannot include router into itself"):
        router.include_router(router)
