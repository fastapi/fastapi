# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import typing

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._asymmetric import (
    AsymmetricPadding as AsymmetricPadding,
)
from cryptography.hazmat.primitives.asymmetric import rsa


class PKCS1v15(AsymmetricPadding):
    name = "EMSA-PKCS1-v1_5"


class _MaxLength:
    "Sentinel value for `MAX_LENGTH`."


class _Auto:
    "Sentinel value for `AUTO`."


class _DigestLength:
    "Sentinel value for `DIGEST_LENGTH`."


class PSS(AsymmetricPadding):
    MAX_LENGTH = _MaxLength()
    AUTO = _Auto()
    DIGEST_LENGTH = _DigestLength()
    name = "EMSA-PSS"
    _salt_length: typing.Union[int, _MaxLength, _Auto, _DigestLength]

    def __init__(
        self,
        mgf: MGF,
        salt_length: typing.Union[int, _MaxLength, _Auto, _DigestLength],
    ) -> None:
        self._mgf = mgf

        if not isinstance(salt_length, (int, _MaxLength, _Auto, _DigestLength)):
            raise TypeError(
                "salt_length must be an integer, MAX_LENGTH, " "DIGEST_LENGTH, or AUTO"
            )

        if isinstance(salt_length, int) and salt_length < 0:
            raise ValueError("salt_length must be zero or greater.")

        self._salt_length = salt_length


class OAEP(AsymmetricPadding):
    name = "EME-OAEP"

    def __init__(
        self,
        mgf: MGF,
        algorithm: hashes.HashAlgorithm,
        label: typing.Optional[bytes],
    ):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError("Expected instance of hashes.HashAlgorithm.")

        self._mgf = mgf
        self._algorithm = algorithm
        self._label = label


class MGF(metaclass=abc.ABCMeta):
    _algorithm: hashes.HashAlgorithm


class MGF1(MGF):
    MAX_LENGTH = _MaxLength()

    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError("Expected instance of hashes.HashAlgorithm.")

        self._algorithm = algorithm


def calculate_max_pss_salt_length(
    key: typing.Union[rsa.RSAPrivateKey, rsa.RSAPublicKey],
    hash_algorithm: hashes.HashAlgorithm,
) -> int:
    if not isinstance(key, (rsa.RSAPrivateKey, rsa.RSAPublicKey)):
        raise TypeError("key must be an RSA public or private key")
    # bit length - 1 per RFC 3447
    emlen = (key.key_size + 6) // 8
    salt_length = emlen - hash_algorithm.digest_size - 2
    assert salt_length >= 0
    return salt_length
