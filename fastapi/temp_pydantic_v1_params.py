"""
Compatibility proxy for Pydantic v1 params.

NOTE: This module re-exports the private shim from fastapi._compat._v1_params.
It exists to keep backward compatibility for imports in tests/docs:
    from fastapi.temp_pydantic_v1_params import Body, Query, Form, ...

Internally, _v1_params is lazy and will only touch pydantic.v1 if v1 is actually used.
"""

from __future__ import annotations

# Re-export shim classes so isinstance(...) keeps working
from ._compat._v1_params import (  # noqa: F401
    Body,
    Cookie,
    File,
    Form,
    Header,
    Param,
    Path,
    Query,
)

__all__ = [
    "Param",
    "Body",
    "Form",
    "File",
    "Query",
    "Header",
    "Cookie",
    "Path",
]
