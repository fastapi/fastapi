# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography.hazmat.bindings._rust import exceptions as rust_exceptions

if typing.TYPE_CHECKING:
    from cryptography.hazmat.bindings._rust import openssl as rust_openssl

_Reasons = rust_exceptions._Reasons


class UnsupportedAlgorithm(Exception):
    def __init__(self, message: str, reason: typing.Optional[_Reasons] = None) -> None:
        super().__init__(message)
        self._reason = reason


class AlreadyFinalized(Exception):
    pass


class AlreadyUpdated(Exception):
    pass


class NotYetFinalized(Exception):
    pass


class InvalidTag(Exception):
    pass


class InvalidSignature(Exception):
    pass


class InternalError(Exception):
    def __init__(
        self, msg: str, err_code: typing.List[rust_openssl.OpenSSLError]
    ) -> None:
        super().__init__(msg)
        self.err_code = err_code


class InvalidKey(Exception):
    pass
