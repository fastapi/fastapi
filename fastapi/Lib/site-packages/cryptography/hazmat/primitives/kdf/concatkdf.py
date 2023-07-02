# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey
from cryptography.hazmat.primitives import constant_time, hashes, hmac
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction


def _int_to_u32be(n: int) -> bytes:
    return n.to_bytes(length=4, byteorder="big")


def _common_args_checks(
    algorithm: hashes.HashAlgorithm,
    length: int,
    otherinfo: typing.Optional[bytes],
) -> None:
    max_length = algorithm.digest_size * (2**32 - 1)
    if length > max_length:
        raise ValueError(f"Cannot derive keys larger than {max_length} bits.")
    if otherinfo is not None:
        utils._check_bytes("otherinfo", otherinfo)


def _concatkdf_derive(
    key_material: bytes,
    length: int,
    auxfn: typing.Callable[[], hashes.HashContext],
    otherinfo: bytes,
) -> bytes:
    utils._check_byteslike("key_material", key_material)
    output = [b""]
    outlen = 0
    counter = 1

    while length > outlen:
        h = auxfn()
        h.update(_int_to_u32be(counter))
        h.update(key_material)
        h.update(otherinfo)
        output.append(h.finalize())
        outlen += len(output[-1])
        counter += 1

    return b"".join(output)[:length]


class ConcatKDFHash(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        otherinfo: typing.Optional[bytes],
        backend: typing.Any = None,
    ):
        _common_args_checks(algorithm, length, otherinfo)
        self._algorithm = algorithm
        self._length = length
        self._otherinfo: bytes = otherinfo if otherinfo is not None else b""

        self._used = False

    def _hash(self) -> hashes.Hash:
        return hashes.Hash(self._algorithm)

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized
        self._used = True
        return _concatkdf_derive(
            key_material, self._length, self._hash, self._otherinfo
        )

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey


class ConcatKDFHMAC(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        length: int,
        salt: typing.Optional[bytes],
        otherinfo: typing.Optional[bytes],
        backend: typing.Any = None,
    ):
        _common_args_checks(algorithm, length, otherinfo)
        self._algorithm = algorithm
        self._length = length
        self._otherinfo: bytes = otherinfo if otherinfo is not None else b""

        if algorithm.block_size is None:
            raise TypeError(f"{algorithm.name} is unsupported for ConcatKDF")

        if salt is None:
            salt = b"\x00" * algorithm.block_size
        else:
            utils._check_bytes("salt", salt)

        self._salt = salt

        self._used = False

    def _hmac(self) -> hmac.HMAC:
        return hmac.HMAC(self._salt, self._algorithm)

    def derive(self, key_material: bytes) -> bytes:
        if self._used:
            raise AlreadyFinalized
        self._used = True
        return _concatkdf_derive(
            key_material, self._length, self._hmac, self._otherinfo
        )

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey
