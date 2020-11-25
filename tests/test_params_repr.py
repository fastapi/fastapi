import pytest
from fastapi.params import Body, Cookie, Depends, Header, Param, Path, Query

test_data = ["teststr", None, ..., 1, []]


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
    assert repr(Depends(use_cache=False)) == "Depends(NoneType, use_cache=False)"
    assert (
        repr(Depends(get_user, use_cache=False)) == "Depends(get_user, use_cache=False)"
    )
