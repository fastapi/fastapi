from unittest.mock import Mock, call, patch

import pytest
from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


def app_dependency(scopes: SecurityScopes):
    return _app_dependency(scopes.scopes)


def _app_dependency(scopes):
    pass


def dep2(foo=Depends(app_dependency)):
    pass


def dep3(foo=Depends(app_dependency)):
    pass


@pytest.fixture
def mocks():
    with patch.dict(globals(), {"_app_dependency": Mock()}):
        yield


app = FastAPI(dependencies=[Security(dep2, scopes=["root1", "root2"])])


@app.get("/root")
def root():
    return {}


@app.get("/endpoint")
def endpoint(dep=Security(dep2, scopes=["endpoint"])):
    return {}


@app.get("/endpoint2")
def endpoint2(dep=Security(dep3, scopes=["endpoint"])):
    return {}


@app.get("/endpoint3")
def endpoint3(
    dep=Security(dep3, scopes=["endpoint1"]), dep2=Security(dep2, scopes=["endpoint2"])
):
    return {}


client = TestClient(app)


def test_root(mocks):
    """
    Test that the single app security dependency gets called
    """
    client.get("root")
    _app_dependency.assert_has_calls([call(["root1", "root2"])])


def test_endpoint(mocks):
    """
    Test that the app security scopes get prepended in front of the dependency security
    """
    client.get("endpoint")
    _app_dependency.assert_has_calls([call(["root1", "root2", "endpoint"])])


def test_endpoint2(mocks):
    """
    Test that the app security scopes don't get prepended on a different dependency
    """
    client.get("endpoint2")
    _app_dependency.assert_has_calls([call(["root1", "root2"]), call(["endpoint"])])


def test_endpoint3(mocks):
    """
    Test that the app security scopes get prepended on the correct dependency
    """
    client.get("endpoint3")
    _app_dependency.assert_has_calls(
        [call(["endpoint1"]), call(["root1", "root2", "endpoint2"])]
    )
