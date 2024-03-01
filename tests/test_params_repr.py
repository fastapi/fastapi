from typing import Any, List

from dirty_equals import IsOneOf
from fastapi.params import Body, Cookie, Depends, Header, Param, Path, Query

test_data: List[Any] = ["teststr", None, ..., 1, []]


def get_user():
    return {}  # pragma: no cover


def test_param_repr_str():
    assert repr(Param("teststr")) == "Param(teststr)"


def test_param_repr_none():
    assert repr(Param(None)) == "Param(None)"


def test_param_repr_ellipsis():
    assert repr(Param(...)) == IsOneOf(
        "Param(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Param(Ellipsis)",
    )


def test_param_repr_number():
    assert repr(Param(1)) == "Param(1)"


def test_param_repr_list():
    assert repr(Param([])) == "Param([])"


def test_path_repr():
    assert repr(Path()) == IsOneOf(
        "Path(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Path(Ellipsis)",
    )
    assert repr(Path(...)) == IsOneOf(
        "Path(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Path(Ellipsis)",
    )


def test_query_repr_str():
    assert repr(Query("teststr")) == "Query(teststr)"


def test_query_repr_none():
    assert repr(Query(None)) == "Query(None)"


def test_query_repr_ellipsis():
    assert repr(Query(...)) == IsOneOf(
        "Query(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Query(Ellipsis)",
    )


def test_query_repr_number():
    assert repr(Query(1)) == "Query(1)"


def test_query_repr_list():
    assert repr(Query([])) == "Query([])"


def test_header_repr_str():
    assert repr(Header("teststr")) == "Header(teststr)"


def test_header_repr_none():
    assert repr(Header(None)) == "Header(None)"


def test_header_repr_ellipsis():
    assert repr(Header(...)) == IsOneOf(
        "Header(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Header(Ellipsis)",
    )


def test_header_repr_number():
    assert repr(Header(1)) == "Header(1)"


def test_header_repr_list():
    assert repr(Header([])) == "Header([])"


def test_cookie_repr_str():
    assert repr(Cookie("teststr")) == "Cookie(teststr)"


def test_cookie_repr_none():
    assert repr(Cookie(None)) == "Cookie(None)"


def test_cookie_repr_ellipsis():
    assert repr(Cookie(...)) == IsOneOf(
        "Cookie(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Cookie(Ellipsis)",
    )


def test_cookie_repr_number():
    assert repr(Cookie(1)) == "Cookie(1)"


def test_cookie_repr_list():
    assert repr(Cookie([])) == "Cookie([])"


def test_body_repr_str():
    assert repr(Body("teststr")) == "Body(teststr)"


def test_body_repr_none():
    assert repr(Body(None)) == "Body(None)"


def test_body_repr_ellipsis():
    assert repr(Body(...)) == IsOneOf(
        "Body(PydanticUndefined)",
        # TODO: remove when deprecating Pydantic v1
        "Body(Ellipsis)",
    )


def test_body_repr_number():
    assert repr(Body(1)) == "Body(1)"


def test_body_repr_list():
    assert repr(Body([])) == "Body([])"


def test_depends_repr():
    assert repr(Depends()) == "Depends(NoneType)"
    assert repr(Depends(get_user)) == "Depends(get_user)"
    assert repr(Depends(use_cache=False)) == "Depends(NoneType, use_cache=False)"
    assert (
        repr(Depends(get_user, use_cache=False)) == "Depends(get_user, use_cache=False)"
    )
