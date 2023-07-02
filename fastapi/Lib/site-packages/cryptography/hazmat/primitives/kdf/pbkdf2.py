# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.exceptions import (
    AlreadyFinalized,
    InvalidKey,
    UnsupportedAlgorithm,
    _Reasons,
)
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import constant_time, hashes
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction


class PBKDF2HMAC(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        salt: bytes,
        iterations: int,
        backend: typing.Any = None,
    ):
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        if not ossl.pbkdf2_hmac_supported(algorithm):
            raise UnsupportedAlgorithm(
                "{} is not supported for PBKDF2 by this backend.".format(
                    algorithm.name
                ),
                _Reasons.UNSUPPORTED_HASH,
            )
        self._used = False
        self._algorithm = algorithm
        self._length = length
        utils._check_bytes("salt", salt)
        self._salt = salt
        self._iterations = iterations

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized("PBKDF2 instances can only be used once.")
        self._used = True

        return rust_openssl.kdf.derive_pbkdf2_hmac(
            key_material,
            self._algorithm,
            self._salt,
            self._iterations,
            self._length,
        )

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        derived_key = self.derive(key_material)
        if not constant_time.bytes_eq(derived_key, expected_key):
            raise InvalidKey("Keys do not match.")
