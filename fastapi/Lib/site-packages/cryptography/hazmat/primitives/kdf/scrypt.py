# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import sys
import typing

from cryptography import utils
from cryptography.exceptions import (
    AlreadyFinalized,
    InvalidKey,
    UnsupportedAlgorithm,
)
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction

# This is used by the scrypt tests to skip tests that require more memory
# than the MEM_LIMIT
_MEM_LIMIT = sys.maxsize // 2


class Scrypt(KeyDerivationFunction):
    def __init__(
        self,
        salt: bytes,
        length: int,
        n: int,
        r: int,
        p: int,
        backend: typing.Any = None,
    ):
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        if not ossl.scrypt_supported():
            raise UnsupportedAlgorithm(
                "This version of OpenSSL does not support scrypt"
            )
        self._length = length
        utils._check_bytes("salt", salt)
        if n < 2 or (n & (n - 1)) != 0:
            raise ValueError("n must be greater than 1 and be a power of 2.")

        if r < 1:
            raise ValueError("r must be greater than or equal to 1.")

        if p < 1:
            raise ValueError("p must be greater than or equal to 1.")

        self._used = False
        self._salt = salt
        self._n = n
        self._r = r
        self._p = p

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized("Scrypt instances can only be used once.")
        self._used = True

        utils._check_byteslike("key_material", key_material)

        return rust_openssl.kdf.derive_scrypt(
            key_material,
            self._salt,
            self._n,
            self._r,
            self._p,
            _MEM_LIMIT,
            self._length,
        )

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        derived_key = self.derive(key_material)
        if not constant_time.bytes_eq(derived_key, expected_key):
            raise InvalidKey("Keys do not match.")
