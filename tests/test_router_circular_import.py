import pytest
from fastapi import APIRouter, FastAPI


def test_router_circular_import():
    app = FastAPI()
    router = APIRouter()

    app.include_router(router)
    with pytest.raises(AssertionError, match="Cannot include router into itself"):
        router.include_router(router)
