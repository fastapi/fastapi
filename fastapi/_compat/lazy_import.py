# path: fastapi/_compat/import.py
"""
Centralized lazy import helpers for v1 compatibility.
"""

from __future__ import annotations

import sys
from typing import Any, Optional, TypeVar

T = TypeVar("T")


def get_v1_if_loaded() -> Optional[Any]:
    """
    Get pydantic.v1 module only if it's already loaded.
    Returns None if not loaded, avoiding any warnings.
    """
    if "pydantic.v1" in sys.modules:
        import pydantic.v1

        return pydantic.v1
    return None


def with_v1_guard(func: Any) -> Any:
    """
    Decorator that only executes function if pydantic.v1 is loaded.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        v1 = get_v1_if_loaded()
        if v1 is not None:
            return func(v1, *args, **kwargs)
        return None

    return wrapper


def v1_isinstance(obj: Any, v1_class: str) -> bool:
    """
    Check isinstance with v1 class only if v1 is loaded.
    """
    v1 = get_v1_if_loaded()
    if v1 is not None:
        cls = getattr(v1, v1_class, None)
        if cls is not None:
            return isinstance(obj, cls)
    return False


def v1_lenient_issubclass(cls: Any, v1_class: str) -> bool:
    """
    Check lenient_issubclass with v1 class only if v1 is loaded.
    """
    v1 = get_v1_if_loaded()
    if v1 is not None:
        v1_cls = getattr(v1, v1_class, None)
        if v1_cls is not None:
            from .shared import lenient_issubclass

            return lenient_issubclass(cls, v1_cls)
    return False


def v1_call_method(method_name: str, *args: Any, **kwargs: Any) -> Any:
    """
    Call a v1 method only if v1 is loaded.
    """
    v1 = get_v1_if_loaded()
    if v1 is not None:
        method = getattr(v1, method_name, None)
        if method is not None:
            return method(*args, **kwargs)
    return None


def v1_get_attr(attr_name: str) -> Any:
    """
    Get v1 attribute only if v1 is loaded.
    """
    v1 = get_v1_if_loaded()
    if v1 is not None:
        return getattr(v1, attr_name, None)
    return None
