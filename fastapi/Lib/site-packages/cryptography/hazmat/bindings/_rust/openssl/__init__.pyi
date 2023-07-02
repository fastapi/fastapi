# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import typing

from cryptography.hazmat.bindings._rust.openssl import (
    dh,
    dsa,
    ed448,
    ed25519,
    hashes,
    hmac,
    kdf,
    poly1305,
    x448,
    x25519,
)

__all__ = [
    "openssl_version",
    "raise_openssl_error",
    "dh",
    "dsa",
    "hashes",
    "hmac",
    "kdf",
    "ed448",
    "ed25519",
    "poly1305",
    "x448",
    "x25519",
]

def openssl_version() -> int: ...
def raise_openssl_error() -> typing.NoReturn: ...
def capture_error_stack() -> typing.List[OpenSSLError]: ...
def is_fips_enabled() -> bool: ...

class OpenSSLError:
    @property
    def lib(self) -> int: ...
    @property
    def reason(self) -> int: ...
    @property
    def reason_text(self) -> bytes: ...
    def _lib_reason_match(self, lib: int, reason: int) -> bool: ...
