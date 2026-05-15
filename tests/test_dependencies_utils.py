# NOTE: Do NOT add `from __future__ import annotations` here.
# That future import would turn the string subscripts in Annotated[...] bodies
# into deferred references and break isinstance() checks in this file.

from typing import Annotated, ForwardRef, get_args, get_origin

from fastapi import params
from fastapi.dependencies.utils import get_typed_annotation

# ---------------------------------------------------------------------------
# Existing coverage test
# ---------------------------------------------------------------------------


def test_get_typed_annotation_none_string() -> None:
    # A bare "None" string should resolve to Python's NoneType (returned as None)
    typed_annotation = get_typed_annotation("None", globals())
    assert typed_annotation is None


# ---------------------------------------------------------------------------
# Issue #13056 – ForwardRef inside Annotated
# ---------------------------------------------------------------------------


class _Potato:
    """Stand-in model used by the tests below."""


def _get_potato() -> "_Potato":
    return _Potato()


def test_annotated_with_string_base_type() -> None:
    """Annotated["_Potato", Depends(...)] must resolve the base type."""
    dep = params.Depends(_get_potato)
    annotation = Annotated["_Potato", dep]
    resolved = get_typed_annotation(annotation, globals())

    assert get_origin(resolved) is Annotated
    args = get_args(resolved)
    assert args[0] is _Potato, f"Expected _Potato, got {args[0]}"
    assert isinstance(args[1], params.Depends)


def test_annotated_with_forwardref_base_type() -> None:
    """Annotated[ForwardRef("_Potato"), Depends(...)] must also resolve."""
    dep = params.Depends(_get_potato)
    annotation = Annotated[ForwardRef("_Potato"), dep]
    resolved = get_typed_annotation(annotation, globals())

    assert get_origin(resolved) is Annotated
    args = get_args(resolved)
    assert args[0] is _Potato, f"Expected _Potato, got {args[0]}"
    assert isinstance(args[1], params.Depends)


def test_annotated_with_already_resolved_type() -> None:
    """Annotated[_Potato, Depends(...)] (already resolved) must pass through unchanged."""
    dep = params.Depends(_get_potato)
    annotation = Annotated[_Potato, dep]
    resolved = get_typed_annotation(annotation, globals())

    assert get_origin(resolved) is Annotated
    args = get_args(resolved)
    assert args[0] is _Potato
    assert isinstance(args[1], params.Depends)


def test_bare_string_annotation() -> None:
    """A bare string annotation (non-Annotated) must still resolve correctly."""
    resolved = get_typed_annotation("_Potato", globals())
    assert resolved is _Potato
