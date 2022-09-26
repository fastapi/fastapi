from unittest.mock import Mock, patch

import pytest
from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient


def app_dependency():
    return _app_dependency()


def _app_dependency():
    pass


@pytest.fixture
def mocks():
    with patch.dict(globals(), {"_app_dependency": Mock()}):
        yield


app = FastAPI(dependencies=[Depends(app_dependency)])

router1 = APIRouter()
disable_root = APIRouter(dependencies=[Depends(app_dependency, disable=True)])


@app.get("/root")
def root():
    return {}

@app.get("/root_disabled", dependencies=[Depends(app_dependency, disable=True)])
def root_disabled():
    return {}



@router1.get("/test1")
def test1():
    return {}


@disable_root.get("/test2")
def test2():
    return {}

@disable_root.get("/test2_re_enable", dependencies=[Depends(app_dependency)])
def test2_re():
    return {}


app.include_router(router1, dependencies=[Depends(app_dependency, disable=True)])
app.include_router(disable_root)
client = TestClient(app)


def test_root(mocks):
    client.get("root_disabled")
    _app_dependency.assert_not_called()
    client.get("root")
    _app_dependency.assert_called()


def test_router1(mocks):
    client.get("test1")
    _app_dependency.assert_not_called()


def test_router2(mocks):
    client.get("test2")
    _app_dependency.assert_not_called()
    client.get("test2_re_enable")
    _app_dependency.assert_called()
