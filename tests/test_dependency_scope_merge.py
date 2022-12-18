from unittest.mock import Mock, call, patch

import pytest
from fastapi import APIRouter, Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient


def app_dependency(scopes: SecurityScopes):
    _app_dependency(scopes.scopes)
    return scopes.scopes


def _app_dependency(scopes):  # pragma: no cover
    pass


def app_dependency2(scopes: SecurityScopes):
    _app_dependency2(scopes.scopes)
    return scopes.scopes


def _app_dependency2(scopes):  # pragma: no cover
    pass


def dep2(foo=Depends(app_dependency)):
    return foo


def dep3(foo=Depends(app_dependency)):
    return foo


def dep4(foo=Security(dep2, scopes=["dep4"])):
    return foo


def dep5(foo=Depends(app_dependency2)):
    return foo


def dep6(foo=Security(app_dependency2, scopes=["dep6"])):
    return foo


def dep7(foo=Security(dep6, scopes=["dep7"])):
    return foo


@pytest.fixture
def mocks():
    with patch.dict(globals(), {"_app_dependency": Mock(), "_app_dependency2": Mock()}):
        yield


app = FastAPI(dependencies=[Security(dep2, scopes=["root1", "root2"])])


@app.get("/root")
def root():
    return {}


@app.get("/endpoint")
def endpoint(dep=Security(dep2, scopes=["endpoint"])):
    return {"dep": dep}


@app.get("/endpoint2")
def endpoint2(dep=Security(dep3, scopes=["endpoint"])):
    return {"dep": dep}


@app.get("/endpoint3")
def endpoint3(
    dep=Security(dep3, scopes=["endpoint1"]), dep2=Security(dep2, scopes=["endpoint2"])
):
    return {"dep": dep, "dep2": dep2}


@app.get("/endpoint4")
def endpoint4(
    dep=Security(dep2),
):
    return {"dep": dep}


@app.get("/endpoint5")
def endpoint5(
    dep=Depends(dep4),
):
    return {"dep": dep}


@app.get("/endpoint6", dependencies=[Security(app_dependency2, scopes=["endpoint6"])])
def endpoint6(
    dep=Depends(dep5),
):
    return {"dep": dep}


@app.get("/endpoint7", dependencies=[Security(dep6, scopes=["endpoint7-np"])])
def endpoint7(
    dep=Security(dep7, scopes=["endpoint7-p"]),
):
    return {"dep": dep}


def dep10(foo=Depends(app_dependency)):
    return foo


def dep11(foo=Depends(app_dependency2)):
    return foo


router1 = APIRouter(dependencies=[Depends(dep10), Security(dep11)])


@router1.get("/endpoint1.1")
def endpoint1_1(dep1=Depends(dep10), dep2=Security(dep11, scopes=["scope"])):
    return {"dep1": dep1, "dep2": dep2}


app.include_router(router1)


client = TestClient(app)


def test_root(mocks):
    """
    Test that the single app security dependency gets called
    """
    result = client.get("root")
    _app_dependency.assert_has_calls([call(["root1", "root2"])])
    assert result.json() == {}


def test_merge(mocks):
    """
    Test that the app security scopes get prepended in front of the dependency security
    """
    result = client.get("endpoint")
    _app_dependency.assert_has_calls([call(["root1", "root2", "endpoint"])])
    assert result.json() == {"dep": ["root1", "root2", "endpoint"]}


def test_merge_incorrect(mocks):
    """
    Test that the app security scopes don't get prepended on a different dependency
    """
    result = client.get("endpoint2")
    _app_dependency.assert_has_calls([call(["root1", "root2"]), call(["endpoint"])])
    assert result.json() == {"dep": ["endpoint"]}


def test_merge_correct(mocks):
    """
    Test that the app security scopes get prepended on the correct dependency
    """
    result = client.get("endpoint3")
    _app_dependency.assert_has_calls(
        [call(["endpoint1"]), call(["root1", "root2", "endpoint2"])]
    )
    assert result.json() == {
        "dep": ["endpoint1"],
        "dep2": ["root1", "root2", "endpoint2"],
    }


def test_merge_with_empty(mocks):
    """
    Test that the app security scopes get prepended on a dependency with no scopes
    """
    result = client.get("endpoint4")
    _app_dependency.assert_has_calls([call(["root1", "root2"])])
    assert result.json() == {"dep": ["root1", "root2"]}


def test_lower_level_security(mocks):
    """
    Test that we find the Security in a lower level dependency
    """
    result = client.get("endpoint5")
    _app_dependency.assert_has_calls([call(["root1", "root2", "dep4"])])
    assert result.json() == {"dep": ["root1", "root2", "dep4"]}


def test_depends_works_like_security(mocks):
    """
    Test that an Depends works like a Security with scopes=[] when
    descending the dependency graph
    """
    result = client.get("endpoint6")
    _app_dependency2.assert_has_calls([call(["endpoint6"])])
    assert result.json() == {"dep": ["endpoint6"]}


def test_scopes_inherited_by_higher_security(mocks):
    """
    Test that scopes merged to a dependency, are also inherited by lower
    level different dependencies
    """
    result = client.get("endpoint7")
    # first scope is the scope added to dep7 by endpoint 7, second
    # is scope added to dep6 from the non-parameter scope.
    _app_dependency2.assert_has_calls(
        [call(["endpoint7-p", "endpoint7-np", "dep7", "dep6"])]
    )
    assert result.json() == {"dep": ["endpoint7-p", "endpoint7-np", "dep7", "dep6"]}


def test_empty_router_scopes(mocks):
    """
    A router has dependencies and securities with no scopes.  Test that it works.
    """
    result = client.get("endpoint1.1")
    # first scope is the scope added to dep7 by endpoint 7, second
    # is scope added to dep6 from the non-parameter scope.
    _app_dependency.assert_has_calls([call([])])
    _app_dependency2.assert_has_calls([call(["scope"])])
    assert result.json() == {"dep1": [], "dep2": ["scope"]}
