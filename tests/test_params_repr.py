from typing import Any

from fastapi.params import Body, Cookie, Header, Param, Path, Query

test_data: list[Any] = ["teststr", None, ..., 1, []]


def get_user():
    return {}  # pragma: no cover


def test_param_repr_str():
    assert repr(Param("teststr")) == "Param(teststr)"


def test_param_repr_none():
    assert repr(Param(None)) == "Param(None)"


def test_param_repr_ellipsis():
    assert repr(Param(...)) == "Param(PydanticUndefined)"


def test_param_repr_number():
    assert repr(Param(1)) == "Param(1)"


def test_param_repr_list():
    assert repr(Param([])) == "Param([])"


def test_path_repr():
    assert repr(Path()) == "Path(PydanticUndefined)"
    assert repr(Path(...)) == "Path(PydanticUndefined)"


def test_query_repr_str():
    assert repr(Query("teststr")) == "Query(teststr)"


def test_query_repr_none():
    assert repr(Query(None)) == "Query(None)"


def test_query_repr_ellipsis():
    assert repr(Query(...)) == "Query(PydanticUndefined)"


def test_query_repr_number():
    assert repr(Query(1)) == "Query(1)"


def test_query_repr_list():
    assert repr(Query([])) == "Query([])"


def test_header_repr_str():
    assert repr(Header("teststr")) == "Header(teststr)"


def test_header_repr_none():
    assert repr(Header(None)) == "Header(None)"


def test_header_repr_ellipsis():
    assert repr(Header(...)) == "Header(PydanticUndefined)"


def test_header_repr_number():
    assert repr(Header(1)) == "Header(1)"


def test_header_repr_list():
    assert repr(Header([])) == "Header([])"


def test_cookie_repr_str():
    assert repr(Cookie("teststr")) == "Cookie(teststr)"


def test_cookie_repr_none():
    assert repr(Cookie(None)) == "Cookie(None)"


def test_cookie_repr_ellipsis():
    assert repr(Cookie(...)) == "Cookie(PydanticUndefined)"


def test_cookie_repr_number():
    assert repr(Cookie(1)) == "Cookie(1)"


def test_cookie_repr_list():
    assert repr(Cookie([])) == "Cookie([])"


def test_body_repr_str():
    assert repr(Body("teststr")) == "Body(teststr)"


def test_body_repr_none():
    assert repr(Body(None)) == "Body(None)"


def test_body_repr_ellipsis():
    assert repr(Body(...)) == "Body(PydanticUndefined)"


def test_body_repr_number():
    assert repr(Body(1)) == "Body(1)"


def test_body_repr_list():
    assert repr(Body([])) == "Body([])"
