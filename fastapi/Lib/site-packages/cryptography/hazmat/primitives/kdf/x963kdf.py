# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey
from cryptography.hazmat.primitives import constant_time, hashes
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction


def _int_to_u32be(n: int) -> bytes:
    return n.to_bytes(length=4, byteorder="big")


class X963KDF(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        sharedinfo: typing.Optional[bytes],
        backend: typing.Any = None,
    ):
        max_len = algorithm.digest_size * (2**32 - 1)
        if length > max_len:
            raise ValueError(f"Cannot derive keys larger than {max_len} bits.")
        if sharedinfo is not None:
            utils._check_bytes("sharedinfo", sharedinfo)

        self._algorithm = algorithm
        self._length = length
        self._sharedinfo = sharedinfo
        self._used = False

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized
        self._used = True
        utils._check_byteslike("key_material", key_material)
        output = [b""]
        outlen = 0
        counter = 1

        while self._length > outlen:
            h = hashes.Hash(self._algorithm)
            h.update(key_material)
            h.update(_int_to_u32be(counter))
            if self._sharedinfo is not None:
                h.update(self._sharedinfo)
            output.append(h.finalize())
            outlen += len(output[-1])
            counter += 1

        return b"".join(output)[: self._length]

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey
