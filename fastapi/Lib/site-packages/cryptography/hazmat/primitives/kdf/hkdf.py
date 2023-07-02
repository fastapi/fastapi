# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey
from cryptography.hazmat.primitives import constant_time, hashes, hmac
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction


class HKDF(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        salt: typing.Optional[bytes],
        info: typing.Optional[bytes],
        backend: typing.Any = None,
    ):
        self._algorithm = algorithm

        if salt is None:
            salt = b"\x00" * self._algorithm.digest_size
        else:
            utils._check_bytes("salt", salt)

        self._salt = salt

        self._hkdf_expand = HKDFExpand(self._algorithm, length, info)

    def _extract(self, key_material: bytes) -> bytes:
        h = hmac.HMAC(self._salt, self._algorithm)
        h.update(key_material)
        return h.finalize()

    def derive(self, key_material: bytes) -> bytes:
        utils._check_byteslike("key_material", key_material)
        return self._hkdf_expand.derive(self._extract(key_material))

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey


class HKDFExpand(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        info: typing.Optional[bytes],
        backend: typing.Any = None,
    ):
        self._algorithm = algorithm

        max_length = 255 * algorithm.digest_size

        if length > max_length:
            raise ValueError(f"Cannot derive keys larger than {max_length} octets.")

        self._length = length

        if info is None:
            info = b""
        else:
            utils._check_bytes("info", info)

        self._info = info

        self._used = False

    def _expand(self, key_material: bytes) -> bytes:
        output = [b""]
        counter = 1

        while self._algorithm.digest_size * (len(output) - 1) < self._length:
            h = hmac.HMAC(key_material, self._algorithm)
            h.update(output[-1])
            h.update(self._info)
            h.update(bytes([counter]))
            output.append(h.finalize())
            counter += 1

        return b"".join(output)[: self._length]

    def derive(self, key_material: bytes) -> bytes:
        utils._check_byteslike("key_material", key_material)
        if self._used:
            raise AlreadyFinalized

        self._used = True
        return self._expand(key_material)

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey
