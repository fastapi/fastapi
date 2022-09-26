from unittest.mock import Mock, call, patch

import pytest
from fastapi import APIRouter, Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


def app_dependency():
    return _app_dependency()


def app_security(scopes: SecurityScopes):
    _app_security(scopes.scopes)


def _app_dependency():  # pragma: no cover
    pass


def _app_security(scopes):  # pragma: no cover
    pass


@pytest.fixture
def mocks():
    with patch.dict(globals(), {"_app_dependency": Mock(), "_app_security": Mock()}):
        yield


app = FastAPI(
    dependencies=[Depends(app_dependency), Security(app_security, scopes=["b", "a"])]
)

router1 = APIRouter()
disable_root = APIRouter(
    dependencies=[
        Depends(app_dependency, disable=True),
        Security(app_security, scopes=["a"], disable=True),
    ]
)


@app.get("/root")
def root():
    return {}


@app.get(
    "/root_disabled",
    dependencies=[
        Depends(app_dependency, disable=True),
        Security(app_security, disable=True),
    ],
)
def root_disabled():
    return {}


@app.get(
    "/root_double",
    dependencies=[Depends(app_dependency), Security(app_security, scopes=["c"])],
)
def root_double():
    return {}


@router1.get("/router1_test")
def router1_test1():
    return {}


@disable_root.get("/disable_root_test")
def disable_root_test():
    return {}


@disable_root.get(
    "/disable_root_re_enable",
    dependencies=[Depends(app_dependency), Security(app_security, scopes=["c"])],
)
def disable_root_re_enable():
    return {}


app.include_router(
    router1,
    dependencies=[
        Depends(app_dependency, disable=True),
        Security(app_security, scopes=["b"], disable=True),
    ],
)
app.include_router(disable_root)
client = TestClient(app)


def test_root(mocks):
    client.get("root_disabled")
    _app_dependency.assert_not_called()
    _app_security.assert_not_called()
    client.get("root")
    _app_dependency.assert_has_calls([call()])
    _app_security.assert_has_calls([call(["b", "a"])])


def test_root_collapse(mocks):
    client.get("root_double")
    _app_dependency.assert_has_calls([call()])
    _app_security.assert_has_calls([call(["b", "a", "c"])])


def test_router1(mocks):
    client.get("router1_test")
    _app_dependency.assert_not_called()
    _app_security.assert_has_calls([call(["a"])])


def test_disable_root(mocks):
    client.get("disable_root_test")
    _app_dependency.assert_not_called()
    _app_security.assert_has_calls([call(["b"])])
    client.get("disable_root_re_enable")
    _app_dependency.assert_has_calls([call()])
    _app_security.assert_has_calls([call(["b", "c"])])
