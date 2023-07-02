from __future__ import annotations

import asyncio
import inspect
import sys
import typing as t
from functools import partial
from weakref import ref

from blinker._saferef import BoundMethodWeakref

IdentityType = t.Union[t.Tuple[int, int], str, int]


class _symbol:
    def __init__(self, name):
        """Construct a new named symbol."""
        self.__name__ = self.name = name

    def __reduce__(self):
        return symbol, (self.name,)

    def __repr__(self):
        return self.name


_symbol.__name__ = "symbol"


class symbol:
    """A constant symbol.

    >>> symbol('foo') is symbol('foo')
    True
    >>> symbol('foo')
    foo

    A slight refinement of the MAGICCOOKIE=object() pattern.  The primary
    advantage of symbol() is its repr().  They are also singletons.

    Repeated calls of symbol('name') will all return the same instance.

    """

    symbols = {}  # type: ignore[var-annotated]

    def __new__(cls, name):
        try:
            return cls.symbols[name]
        except KeyError:
            return cls.symbols.setdefault(name, _symbol(name))


def hashable_identity(obj: object) -> IdentityType:
    if hasattr(obj, "__func__"):
        return (id(obj.__func__), id(obj.__self__))  # type: ignore[attr-defined]
    elif hasattr(obj, "im_func"):
        return (id(obj.im_func), id(obj.im_self))  # type: ignore[attr-defined]
    elif isinstance(obj, (int, str)):
        return obj
    else:
        return id(obj)


WeakTypes = (ref, BoundMethodWeakref)


class annotatable_weakref(ref):
    """A weakref.ref that supports custom instance attributes."""

    receiver_id: t.Optional[IdentityType]
    sender_id: t.Optional[IdentityType]


def reference(  # type: ignore[no-untyped-def]
    object, callback=None, **annotations
) -> annotatable_weakref:
    """Return an annotated weak ref."""
    if callable(object):
        weak = callable_reference(object, callback)
    else:
        weak = annotatable_weakref(object, callback)
    for key, value in annotations.items():
        setattr(weak, key, value)
    return weak  # type: ignore[no-any-return]


def callable_reference(object, callback=None):
    """Return an annotated weak ref, supporting bound instance methods."""
    if hasattr(object, "im_self") and object.im_self is not None:
        return BoundMethodWeakref(target=object, on_delete=callback)
    elif hasattr(object, "__self__") and object.__self__ is not None:
        return BoundMethodWeakref(target=object, on_delete=callback)
    return annotatable_weakref(object, callback)


class lazy_property:
    """A @property that is only evaluated once."""

    def __init__(self, deferred):
        self._deferred = deferred
        self.__doc__ = deferred.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self._deferred(obj)
        setattr(obj, self._deferred.__name__, value)
        return value


def is_coroutine_function(func: t.Any) -> bool:
    # Python < 3.8 does not correctly determine partially wrapped
    # coroutine functions are coroutine functions, hence the need for
    # this to exist. Code taken from CPython.
    if sys.version_info >= (3, 8):
        return asyncio.iscoroutinefunction(func)
    else:
        # Note that there is something special about the AsyncMock
        # such that it isn't determined as a coroutine function
        # without an explicit check.
        try:
            from unittest.mock import AsyncMock  # type: ignore[attr-defined]

            if isinstance(func, AsyncMock):
                return True
        except ImportError:
            # Not testing, no asynctest to import
            pass

        while inspect.ismethod(func):
            func = func.__func__
        while isinstance(func, partial):
            func = func.func
        if not inspect.isfunction(func):
            return False

        if func.__code__.co_flags & inspect.CO_COROUTINE:
            return True

        acic = asyncio.coroutines._is_coroutine  # type: ignore[attr-defined]
        return getattr(func, "_is_coroutine", None) is acic
