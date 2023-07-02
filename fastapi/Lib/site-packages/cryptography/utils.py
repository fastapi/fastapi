# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import enum
import sys
import types
import typing
import warnings


# We use a UserWarning subclass, instead of DeprecationWarning, because CPython
# decided deprecation warnings should be invisble by default.
class CryptographyDeprecationWarning(UserWarning):
    pass


# Several APIs were deprecated with no specific end-of-life date because of the
# ubiquity of their use. They should not be removed until we agree on when that
# cycle ends.
DeprecatedIn36 = CryptographyDeprecationWarning
DeprecatedIn37 = CryptographyDeprecationWarning
DeprecatedIn40 = CryptographyDeprecationWarning
DeprecatedIn41 = CryptographyDeprecationWarning


def _check_bytes(name: str, value: bytes) -> None:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes")


def _check_byteslike(name: str, value: bytes) -> None:
    try:
        memoryview(value)
    except TypeError:
        raise TypeError(f"{name} must be bytes-like")


def int_to_bytes(integer: int, length: typing.Optional[int] = None) -> bytes:
    return integer.to_bytes(length or (integer.bit_length() + 7) // 8 or 1, "big")


def _extract_buffer_length(obj: typing.Any) -> typing.Tuple[typing.Any, int]:
    from cryptography.hazmat.bindings._rust import _openssl

    buf = _openssl.ffi.from_buffer(obj)
    return buf, int(_openssl.ffi.cast("uintptr_t", buf))


class InterfaceNotImplemented(Exception):
    pass


class _DeprecatedValue:
    def __init__(self, value: object, message: str, warning_class):
        self.value = value
        self.message = message
        self.warning_class = warning_class


class _ModuleWithDeprecations(types.ModuleType):
    def __init__(self, module: types.ModuleType):
        super().__init__(module.__name__)
        self.__dict__["_module"] = module

    def __getattr__(self, attr: str) -> object:
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, stacklevel=2)
            obj = obj.value
        return obj

    def __setattr__(self, attr: str, value: object) -> None:
        setattr(self._module, attr, value)

    def __delattr__(self, attr: str) -> None:
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, stacklevel=2)

        delattr(self._module, attr)

    def __dir__(self) -> typing.Sequence[str]:
        return ["_module"] + dir(self._module)


def deprecated(
    value: object,
    module_name: str,
    message: str,
    warning_class: typing.Type[Warning],
    name: typing.Optional[str] = None,
) -> _DeprecatedValue:
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = module = _ModuleWithDeprecations(module)
    dv = _DeprecatedValue(value, message, warning_class)
    # Maintain backwards compatibility with `name is None` for pyOpenSSL.
    if name is not None:
        setattr(module, name, dv)
    return dv


def cached_property(func: typing.Callable) -> property:
    cached_name = f"_cached_{func}"
    sentinel = object()

    def inner(instance: object):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        result = func(instance)
        setattr(instance, cached_name, result)
        return result

    return property(inner)


# Python 3.10 changed representation of enums. We use well-defined object
# representation and string representation from Python 3.9.
class Enum(enum.Enum):
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}: {self._value_!r}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}.{self._name_}"
