"""Test for issue #14128: Router used directly with TestClient and yield dependencies."""

from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient


def test_router_direct_testclient_with_yield_dependency():
    """TestClient(router) should work even without wrapping in FastAPI()."""
    router = APIRouter()

    async def yield_dep():
        yield "value"

    @router.get("/test")
    async def endpoint(dep: str = Depends(yield_dep)):
        return {"dep": dep}

    client = TestClient(router)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"dep": "value"}


def test_router_direct_testclient_with_multiple_yield_dependencies():
    """Multiple yield dependencies should work with direct router TestClient."""
    router = APIRouter()

    async def dep_a():
        yield "a"

    async def dep_b():
        yield "b"

    @router.get("/test")
    async def endpoint(a: str = Depends(dep_a), b: str = Depends(dep_b)):
        return {"a": a, "b": b}

    client = TestClient(router)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"a": "a", "b": "b"}


def test_router_direct_testclient_yield_dependency_cleanup():
    """Yield dependency cleanup should run even with direct router TestClient."""
    cleaned_up = False

    router = APIRouter()

    async def yield_dep():
        nonlocal cleaned_up
        yield "value"
        cleaned_up = True

    @router.get("/test")
    async def endpoint(dep: str = Depends(yield_dep)):
        return {"dep": dep}

    client = TestClient(router)
    response = client.get("/test")
    assert response.status_code == 200
    assert cleaned_up
