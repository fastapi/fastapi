# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc

from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization


class Ed25519PublicKey(metaclass=abc.ABCMeta):
    @classmethod
    def from_public_bytes(cls, data: bytes) -> Ed25519PublicKey:
        from cryptography.hazmat.backends.openssl.backend import backend

        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm(
                "ed25519 is not supported by this version of OpenSSL.",
                _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM,
            )

        return backend.ed25519_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PublicFormat,
    ) -> bytes:
        """
        The serialized bytes of the public key.
        """

    @abc.abstractmethod
    def public_bytes_raw(self) -> bytes:
        """
        The raw bytes of the public key.
        Equivalent to public_bytes(Raw, Raw).
        """

    @abc.abstractmethod
    def verify(self, signature: bytes, data: bytes) -> None:
        """
        Verify the signature.
        """

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """


if hasattr(rust_openssl, "ed25519"):
    Ed25519PublicKey.register(rust_openssl.ed25519.Ed25519PublicKey)


class Ed25519PrivateKey(metaclass=abc.ABCMeta):
    @classmethod
    def generate(cls) -> Ed25519PrivateKey:
        from cryptography.hazmat.backends.openssl.backend import backend

        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm(
                "ed25519 is not supported by this version of OpenSSL.",
                _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM,
            )

        return backend.ed25519_generate_key()

    @classmethod
    def from_private_bytes(cls, data: bytes) -> Ed25519PrivateKey:
        from cryptography.hazmat.backends.openssl.backend import backend

        if not backend.ed25519_supported():
            raise UnsupportedAlgorithm(
                "ed25519 is not supported by this version of OpenSSL.",
                _Reasons.UNSUPPORTED_PUBLIC_KEY_ALGORITHM,
            )

        return backend.ed25519_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self) -> Ed25519PublicKey:
        """
        The Ed25519PublicKey derived from the private key.
        """

    @abc.abstractmethod
    def private_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PrivateFormat,
        encryption_algorithm: _serialization.KeySerializationEncryption,
    ) -> bytes:
        """
        The serialized bytes of the private key.
        """

    @abc.abstractmethod
    def private_bytes_raw(self) -> bytes:
        """
        The raw bytes of the private key.
        Equivalent to private_bytes(Raw, Raw, NoEncryption()).
        """

    @abc.abstractmethod
    def sign(self, data: bytes) -> bytes:
        """
        Signs the data.
        """


if hasattr(rust_openssl, "x25519"):
    Ed25519PrivateKey.register(rust_openssl.ed25519.Ed25519PrivateKey)
