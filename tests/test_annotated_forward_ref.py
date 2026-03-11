"""Regression tests for issue #13056.

``Annotated[SomeClass, Depends()]`` must work even when *SomeClass* is defined
after the route handler and ``from __future__ import annotations`` is active.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, get_args, get_origin

from fastapi import Depends, FastAPI, Query, params
from fastapi.dependencies.utils import (
    _LenientDict,
    _try_resolve_annotated,
    get_typed_annotation,
)
from fastapi.testclient import TestClient

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}


@dataclass
class Potato:
    color: str
    size: int


client = TestClient(app)


# -- Integration tests -------------------------------------------------------


def test_annotated_forward_ref():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"color": "red", "size": 10}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    root_path = schema["paths"]["/"]["get"]
    params = root_path.get("parameters", [])
    potato_params = [p for p in params if "potato" in p.get("name", "").lower()]
    assert potato_params == [], "potato must not appear as a query parameter"


# -- _LenientDict -----------------------------------------------------------


def test_lenient_dict_returns_any_for_missing_keys():
    d = _LenientDict({"existing": int})
    assert d["existing"] is int
    assert d["missing"] is Any


# -- _try_resolve_annotated: strict path ------------------------------------


def test_try_resolve_strict_success():
    """Fully resolvable annotation returns immediately via strict eval."""

    def dep() -> str:
        return "ok"  # pragma: no cover

    ns = {"Annotated": Annotated, "str": str, "Depends": Depends, "dep": dep}
    result = _try_resolve_annotated("Annotated[str, Depends(dep)]", ns)
    assert result is not None
    assert get_origin(result) is Annotated
    args = get_args(result)
    assert args[0] is str


# -- _try_resolve_annotated: lenient path with Depends ----------------------


def test_try_resolve_lenient_with_depends():
    """Unresolvable type + Depends → Annotated[Any, Depends(...)]."""

    def dep() -> str:
        return "ok"  # pragma: no cover

    ns = {"Annotated": Annotated, "Depends": Depends, "dep": dep}
    result = _try_resolve_annotated("Annotated[MissingClass, Depends(dep)]", ns)
    assert result is not None
    assert get_origin(result) is Annotated
    args = get_args(result)
    assert args[0] is Any
    assert isinstance(args[1], params.Depends)


# -- _try_resolve_annotated: lenient path without Depends -------------------


def test_try_resolve_lenient_non_depends_returns_none():
    """Unresolvable type + Query → None (actual type needed for Query)."""
    ns = {"Annotated": Annotated, "Query": Query}
    result = _try_resolve_annotated("Annotated[MissingClass, Query()]", ns)
    assert result is None


# -- _try_resolve_annotated: both paths fail --------------------------------


def test_try_resolve_completely_invalid():
    """Completely invalid expression returns None."""
    result = _try_resolve_annotated("Annotated[", {})
    assert result is None


def test_try_resolve_strict_exception_lenient_exception():
    """Both strict and lenient raise → returns None."""
    result = _try_resolve_annotated("Annotated[{bad syntax", {})
    assert result is None


# -- get_typed_annotation passthrough tests ----------------------------------


def test_get_typed_annotation_non_annotated_string():
    """Plain string annotation falls through to default ForwardRef path."""
    ns: dict[str, Any] = {"str": str}
    result = get_typed_annotation("str", ns)
    assert result is str


def test_get_typed_annotation_non_string():
    """Non-string annotation is returned as-is."""
    result = get_typed_annotation(int, {})
    assert result is int


def test_get_typed_annotation_annotated_with_result():
    """Annotated string that resolves via _try_resolve_annotated."""

    def dep() -> str:
        return "ok"  # pragma: no cover

    ns = {"Annotated": Annotated, "str": str, "Depends": Depends, "dep": dep}
    result = get_typed_annotation("Annotated[str, Depends(dep)]", ns)
    assert get_origin(result) is Annotated


def test_get_typed_annotation_annotated_no_result_falls_through():
    """Annotated string with non-Depends metadata falls through to default."""
    ns: dict[str, Any] = {"Annotated": Annotated, "str": str, "Query": Query}
    result = get_typed_annotation("Annotated[str, Query()]", ns)
    assert get_origin(result) is Annotated
