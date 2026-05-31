"""
Internal type aliases for FastAPI.

Provides shared type definitions used throughout the framework, including
the decorated callable type variable, union type compatibility shim, and
Pydantic model name mapping types.
"""

import types
from collections.abc import Callable
from enum import Enum
from typing import Any, TypeVar, Union

from pydantic import BaseModel
from pydantic.main import IncEx as IncEx

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = dict[type[BaseModel] | type[Enum], str]
DependencyCacheKey = tuple[Callable[..., Any] | None, tuple[str, ...], str]
