from unittest.mock import Mock, call, patch

import pytest
from fastapi import FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


async def security1(scopes: SecurityScopes):
    return _security1(scopes.scopes)


def _security1(scopes):  # pragma: no cover
    pass


async def security2(scopes: SecurityScopes):
    return _security2(scopes.scopes)


def _security2(scopes):  # pragma: no cover
    pass


async def dep3(
    dep=Security(security1, scopes=["scope1"]),
    dep2=Security(security2, scopes=["scope2"]),
):
    return {}


@pytest.fixture
def mocks():
    with patch.dict(globals(), {"_security1": Mock()}):
        with patch.dict(globals(), {"_security2": Mock()}):
            yield


app = FastAPI()


@app.get("/recursive_scopes")
def recursive_scopes(dep=Security(dep3, scopes=["scope3"])):
    return {}


client = TestClient(app)


# issue https://github.com/tiangolo/fastapi/issues/5623
def test_recursive_scopes(mocks):
    """
    Test that scope recursion properly applies.  Scopes added to a dependency should propagate
    and be prepended correctly to all sub-dependencies.
    """
    client.get("recursive_scopes")
    _security1.assert_has_calls([call(["scope3", "scope1"])])
    _security2.assert_has_calls([call(["scope3", "scope2"])])
