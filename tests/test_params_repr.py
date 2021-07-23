from typing import Any, List

import pytest
from fastapi.params import Body, Cookie, Depends, Header, Param, Path, Query
from fastapi.dependencies.cache import DependencyCacheScope
from fastapi.dependencies.lifetime import DependencyLifetime


test_data: List[Any] = ["teststr", None, ..., 1, []]


def get_user():
    return {}  # pragma: no cover


@pytest.fixture(scope="function", params=test_data)
def params(request):
    return request.param


def test_param_repr(params):
    assert repr(Param(params)) == "Param(" + str(params) + ")"


def test_path_repr(params):
    assert repr(Path(params)) == "Path(Ellipsis)"


def test_query_repr(params):
    assert repr(Query(params)) == "Query(" + str(params) + ")"


def test_header_repr(params):
    assert repr(Header(params)) == "Header(" + str(params) + ")"


def test_cookie_repr(params):
    assert repr(Cookie(params)) == "Cookie(" + str(params) + ")"


def test_body_repr(params):
    assert repr(Body(params)) == "Body(" + str(params) + ")"


def test_depends_repr():
    assert repr(Depends()) == "Depends(NoneType)"
    assert repr(Depends(get_user)) == "Depends(get_user)"
    assert repr(Depends(use_cache=False)) == "Depends(NoneType, use_cache=DependencyCacheScope.nocache)"
    assert repr(Depends(use_cache=DependencyCacheScope.nocache)) == "Depends(NoneType, use_cache=DependencyCacheScope.nocache)"
    assert (
        repr(Depends(get_user, use_cache=False)) == "Depends(get_user, use_cache=DependencyCacheScope.nocache)"
    )
    assert repr(Depends(lifetime="app")) == "Depends(NoneType, lifetime=DependencyLifetime.app)"
    assert repr(Depends(lifetime=DependencyLifetime.app)) == "Depends(NoneType, lifetime=DependencyLifetime.app)"
    assert (
        repr(Depends(get_user, lifetime="app")) == "Depends(get_user, lifetime=DependencyLifetime.app)"
    )
    assert repr(Depends(lifetime="app", use_cache=False)) == "Depends(NoneType, use_cache=DependencyCacheScope.nocache, lifetime=DependencyLifetime.app)"
