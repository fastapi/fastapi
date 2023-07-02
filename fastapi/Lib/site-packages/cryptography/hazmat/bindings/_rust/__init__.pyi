# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import types
import typing

def check_pkcs7_padding(data: bytes) -> bool: ...
def check_ansix923_padding(data: bytes) -> bool: ...

class ObjectIdentifier:
    def __init__(self, val: str) -> None: ...
    @property
    def dotted_string(self) -> str: ...
    @property
    def _name(self) -> str: ...

T = typing.TypeVar("T")

class FixedPool(typing.Generic[T]):
    def __init__(
        self,
        create: typing.Callable[[], T],
    ) -> None: ...
    def acquire(self) -> PoolAcquisition[T]: ...

class PoolAcquisition(typing.Generic[T]):
    def __enter__(self) -> T: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None: ...
