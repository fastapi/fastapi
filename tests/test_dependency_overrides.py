from typing import Optional

import pytest
from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

router = APIRouter()


async def common_parameters(q: str, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/main-depends/")
async def main_depends(commons: dict = Depends(common_parameters)):
    return {"in": "main-depends", "params": commons}


@app.get("/decorator-depends/", dependencies=[Depends(common_parameters)])
async def decorator_depends():
    return {"in": "decorator-depends"}


@router.get("/router-depends/")
async def router_depends(commons: dict = Depends(common_parameters)):
    return {"in": "router-depends", "params": commons}


@router.get("/router-decorator-depends/", dependencies=[Depends(common_parameters)])
async def router_decorator_depends():
    return {"in": "router-decorator-depends"}


app.include_router(router)

client = TestClient(app)


async def overrider_dependency_simple(q: Optional[str] = None):
    return {"q": q, "skip": 5, "limit": 10}


async def overrider_sub_dependency(k: str):
    return {"k": k}


async def overrider_dependency_with_sub(msg: dict = Depends(overrider_sub_dependency)):
    return msg


@pytest.mark.parametrize(
    "url,status_code,expected",
    [
        (
            "/main-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "q"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/main-depends/?q=foo",
            200,
            {"in": "main-depends", "params": {"q": "foo", "skip": 0, "limit": 100}},
        ),
        (
            "/main-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "main-depends", "params": {"q": "foo", "skip": 100, "limit": 200}},
        ),
        (
            "/decorator-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "q"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        ("/decorator-depends/?q=foo", 200, {"in": "decorator-depends"}),
        (
            "/decorator-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "decorator-depends"},
        ),
        (
            "/router-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "q"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/router-depends/?q=foo",
            200,
            {"in": "router-depends", "params": {"q": "foo", "skip": 0, "limit": 100}},
        ),
        (
            "/router-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "router-depends", "params": {"q": "foo", "skip": 100, "limit": 200}},
        ),
        (
            "/router-decorator-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "q"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        ("/router-decorator-depends/?q=foo", 200, {"in": "router-decorator-depends"}),
        (
            "/router-decorator-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "router-decorator-depends"},
        ),
    ],
)
def test_normal_app(url, status_code, expected):
    response = client.get(url)
    assert response.status_code == status_code
    assert response.json() == expected


@pytest.mark.parametrize(
    "url,status_code,expected",
    [
        (
            "/main-depends/",
            200,
            {"in": "main-depends", "params": {"q": None, "skip": 5, "limit": 10}},
        ),
        (
            "/main-depends/?q=foo",
            200,
            {"in": "main-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
        ),
        (
            "/main-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "main-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
        ),
        ("/decorator-depends/", 200, {"in": "decorator-depends"}),
        (
            "/router-depends/",
            200,
            {"in": "router-depends", "params": {"q": None, "skip": 5, "limit": 10}},
        ),
        (
            "/router-depends/?q=foo",
            200,
            {"in": "router-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
        ),
        (
            "/router-depends/?q=foo&skip=100&limit=200",
            200,
            {"in": "router-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
        ),
        ("/router-decorator-depends/", 200, {"in": "router-decorator-depends"}),
    ],
)
def test_override_simple(url, status_code, expected):
    app.dependency_overrides[common_parameters] = overrider_dependency_simple
    response = client.get(url)
    assert response.status_code == status_code
    assert response.json() == expected
    app.dependency_overrides = {}


@pytest.mark.parametrize(
    "url,status_code,expected",
    [
        (
            "/main-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/main-depends/?q=foo",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        ("/main-depends/?k=bar", 200, {"in": "main-depends", "params": {"k": "bar"}}),
        (
            "/decorator-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/decorator-depends/?q=foo",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        ("/decorator-depends/?k=bar", 200, {"in": "decorator-depends"}),
        (
            "/router-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/router-depends/?q=foo",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/router-depends/?k=bar",
            200,
            {"in": "router-depends", "params": {"k": "bar"}},
        ),
        (
            "/router-decorator-depends/",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            "/router-decorator-depends/?q=foo",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "k"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        ("/router-decorator-depends/?k=bar", 200, {"in": "router-decorator-depends"}),
    ],
)
def test_override_with_sub(url, status_code, expected):
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get(url)
    assert response.status_code == status_code
    assert response.json() == expected
    app.dependency_overrides = {}
