# mypy: disable-error-code=no-untyped-def,no-untyped-call,arg-type,call-arg,attr-defined,valid-type
# path: fastapi/_compat/_v1_params.py

"""
Internal v1-params shim. Will be removed when v1 is dropped.

This module provides compatibility shims for Pydantic v1 FieldInfo/Param types
to support isinstance() checks without importing pydantic.v1 at import-time.
Used internally by FastAPI for backward compatibility.
"""

from __future__ import annotations

from typing import Any

_SENTINEL = object()


def _v1() -> Any:
    """Lazy import of v1 module to avoid warnings."""
    from . import v1  # lazy proxy; só avisa/erra se realmente usar v1

    return v1


class _BaseParam:
    """Wrapper mínimo que delega para v1.FieldInfo sem importar v1 no import-time."""

    def __init__(self, default: Any = _SENTINEL, **kwargs: Any):
        v1 = _v1()
        if default is _SENTINEL:
            default = getattr(v1, "Undefined", None)
        self._fi = v1.FieldInfo(default=default, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._fi, name)


# Tipos usados nos isinstance() do core
class Param(_BaseParam): ...


class Body(_BaseParam): ...


class Form(Body): ...


class File(Form): ...


class Path(Param): ...


class Query(Param): ...


class Header(Param): ...


class Cookie(Param): ...
