import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient

app = FastAPI()

router = APIRouter()


@router.get("")
def get_empty():
    return ["OK"]


app.include_router(router, prefix="/prefix")


client = TestClient(app)


def test_use_empty():
    with client:
        response = client.get("/prefix")
        assert response.status_code == 200, response.text
        assert response.json() == ["OK"]

        response = client.get("/prefix/")
        assert response.status_code == 200, response.text
        assert response.json() == ["OK"]


def test_include_empty():
    # if both include and router.path are empty - it should raise exception
    with pytest.raises(FastAPIError):
        app.include_router(router)


def test_include_empty_nested_with_inner_prefix():
    # the inner include gives a prefix, the outer include has none
    leaf = APIRouter()

    @leaf.get("")
    def list_items():
        return ["items"]

    inner = APIRouter()
    inner.include_router(leaf, prefix="/items")
    nested_app = FastAPI()
    nested_app.include_router(inner)

    response = TestClient(nested_app).get("/items")
    assert response.status_code == 200, response.text
    assert response.json() == ["items"]


def test_include_empty_nested_without_prefix():
    # included elsewhere with a prefix, but included here directly without one:
    # the effective path is still empty, it should raise
    leaf = APIRouter()

    @leaf.get("")
    def list_items():  # pragma: no cover
        return ["items"]

    inner = APIRouter()
    inner.include_router(leaf, prefix="/items")
    with pytest.raises(FastAPIError):
        FastAPI().include_router(leaf)
