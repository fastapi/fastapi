# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import os
import typing

from cryptography import exceptions, utils
from cryptography.hazmat.backends.openssl import aead
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.bindings._rust import FixedPool


class ChaCha20Poly1305:
    _MAX_SIZE = 2**31 - 1

    def __init__(self, key: bytes):
        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm(
                "ChaCha20Poly1305 is not supported by this version of OpenSSL",
                exceptions._Reasons.UNSUPPORTED_CIPHER,
            )
        utils._check_byteslike("key", key)

        if len(key) != 32:
            raise ValueError("ChaCha20Poly1305 key must be 32 bytes.")

        self._key = key
        self._pool = FixedPool(self._create_fn)

    @classmethod
    def generate_key(cls) -> bytes:
        return os.urandom(32)

    def _create_fn(self):
        return aead._aead_create_ctx(backend, self, self._key)

    def encrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        if len(data) > self._MAX_SIZE or len(associated_data) > self._MAX_SIZE:
            # This is OverflowError to match what cffi would raise
            raise OverflowError("Data or associated data too long. Max 2**31 - 1 bytes")

        self._check_params(nonce, data, associated_data)
        with self._pool.acquire() as ctx:
            return aead._encrypt(backend, self, nonce, data, [associated_data], 16, ctx)

    def decrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        with self._pool.acquire() as ctx:
            return aead._decrypt(backend, self, nonce, data, [associated_data], 16, ctx)

    def _check_params(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: bytes,
    ) -> None:
        utils._check_byteslike("nonce", nonce)
        utils._check_byteslike("data", data)
        utils._check_byteslike("associated_data", associated_data)
        if len(nonce) != 12:
            raise ValueError("Nonce must be 12 bytes")


class AESCCM:
    _MAX_SIZE = 2**31 - 1

    def __init__(self, key: bytes, tag_length: int = 16):
        utils._check_byteslike("key", key)
        if len(key) not in (16, 24, 32):
            raise ValueError("AESCCM key must be 128, 192, or 256 bits.")

        self._key = key
        if not isinstance(tag_length, int):
            raise TypeError("tag_length must be an integer")

        if tag_length not in (4, 6, 8, 10, 12, 14, 16):
            raise ValueError("Invalid tag_length")

        self._tag_length = tag_length

        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm(
                "AESCCM is not supported by this version of OpenSSL",
                exceptions._Reasons.UNSUPPORTED_CIPHER,
            )

    @classmethod
    def generate_key(cls, bit_length: int) -> bytes:
        if not isinstance(bit_length, int):
            raise TypeError("bit_length must be an integer")

        if bit_length not in (128, 192, 256):
            raise ValueError("bit_length must be 128, 192, or 256")

        return os.urandom(bit_length // 8)

    def encrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        if len(data) > self._MAX_SIZE or len(associated_data) > self._MAX_SIZE:
            # This is OverflowError to match what cffi would raise
            raise OverflowError("Data or associated data too long. Max 2**31 - 1 bytes")

        self._check_params(nonce, data, associated_data)
        self._validate_lengths(nonce, len(data))
        return aead._encrypt(
            backend, self, nonce, data, [associated_data], self._tag_length
        )

    def decrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        return aead._decrypt(
            backend, self, nonce, data, [associated_data], self._tag_length
        )

    def _validate_lengths(self, nonce: bytes, data_len: int) -> None:
        # For information about computing this, see
        # https://tools.ietf.org/html/rfc3610#section-2.1
        l_val = 15 - len(nonce)
        if 2 ** (8 * l_val) < data_len:
            raise ValueError("Data too long for nonce")

    def _check_params(self, nonce: bytes, data: bytes, associated_data: bytes) -> None:
        utils._check_byteslike("nonce", nonce)
        utils._check_byteslike("data", data)
        utils._check_byteslike("associated_data", associated_data)
        if not 7 <= len(nonce) <= 13:
            raise ValueError("Nonce must be between 7 and 13 bytes")


class AESGCM:
    _MAX_SIZE = 2**31 - 1

    def __init__(self, key: bytes):
        utils._check_byteslike("key", key)
        if len(key) not in (16, 24, 32):
            raise ValueError("AESGCM key must be 128, 192, or 256 bits.")

        self._key = key

    @classmethod
    def generate_key(cls, bit_length: int) -> bytes:
        if not isinstance(bit_length, int):
            raise TypeError("bit_length must be an integer")

        if bit_length not in (128, 192, 256):
            raise ValueError("bit_length must be 128, 192, or 256")

        return os.urandom(bit_length // 8)

    def encrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        if len(data) > self._MAX_SIZE or len(associated_data) > self._MAX_SIZE:
            # This is OverflowError to match what cffi would raise
            raise OverflowError("Data or associated data too long. Max 2**31 - 1 bytes")

        self._check_params(nonce, data, associated_data)
        return aead._encrypt(backend, self, nonce, data, [associated_data], 16)

    def decrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        return aead._decrypt(backend, self, nonce, data, [associated_data], 16)

    def _check_params(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: bytes,
    ) -> None:
        utils._check_byteslike("nonce", nonce)
        utils._check_byteslike("data", data)
        utils._check_byteslike("associated_data", associated_data)
        if len(nonce) < 8 or len(nonce) > 128:
            raise ValueError("Nonce must be between 8 and 128 bytes")


class AESOCB3:
    _MAX_SIZE = 2**31 - 1

    def __init__(self, key: bytes):
        utils._check_byteslike("key", key)
        if len(key) not in (16, 24, 32):
            raise ValueError("AESOCB3 key must be 128, 192, or 256 bits.")

        self._key = key

        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm(
                "OCB3 is not supported by this version of OpenSSL",
                exceptions._Reasons.UNSUPPORTED_CIPHER,
            )

    @classmethod
    def generate_key(cls, bit_length: int) -> bytes:
        if not isinstance(bit_length, int):
            raise TypeError("bit_length must be an integer")

        if bit_length not in (128, 192, 256):
            raise ValueError("bit_length must be 128, 192, or 256")

        return os.urandom(bit_length // 8)

    def encrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        if len(data) > self._MAX_SIZE or len(associated_data) > self._MAX_SIZE:
            # This is OverflowError to match what cffi would raise
            raise OverflowError("Data or associated data too long. Max 2**31 - 1 bytes")

        self._check_params(nonce, data, associated_data)
        return aead._encrypt(backend, self, nonce, data, [associated_data], 16)

    def decrypt(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: typing.Optional[bytes],
    ) -> bytes:
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        return aead._decrypt(backend, self, nonce, data, [associated_data], 16)

    def _check_params(
        self,
        nonce: bytes,
        data: bytes,
        associated_data: bytes,
    ) -> None:
        utils._check_byteslike("nonce", nonce)
        utils._check_byteslike("data", data)
        utils._check_byteslike("associated_data", associated_data)
        if len(nonce) < 12 or len(nonce) > 15:
            raise ValueError("Nonce must be between 12 and 15 bytes")


class AESSIV:
    _MAX_SIZE = 2**31 - 1

    def __init__(self, key: bytes):
        utils._check_byteslike("key", key)
        if len(key) not in (32, 48, 64):
            raise ValueError("AESSIV key must be 256, 384, or 512 bits.")

        self._key = key

        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm(
                "AES-SIV is not supported by this version of OpenSSL",
                exceptions._Reasons.UNSUPPORTED_CIPHER,
            )

    @classmethod
    def generate_key(cls, bit_length: int) -> bytes:
        if not isinstance(bit_length, int):
            raise TypeError("bit_length must be an integer")

        if bit_length not in (256, 384, 512):
            raise ValueError("bit_length must be 256, 384, or 512")

        return os.urandom(bit_length // 8)

    def encrypt(
        self,
        data: bytes,
        associated_data: typing.Optional[typing.List[bytes]],
    ) -> bytes:
        if associated_data is None:
            associated_data = []

        self._check_params(data, associated_data)

        if len(data) > self._MAX_SIZE or any(
            len(ad) > self._MAX_SIZE for ad in associated_data
        ):
            # This is OverflowError to match what cffi would raise
            raise OverflowError("Data or associated data too long. Max 2**31 - 1 bytes")

        return aead._encrypt(backend, self, b"", data, associated_data, 16)

    def decrypt(
        self,
        data: bytes,
        associated_data: typing.Optional[typing.List[bytes]],
    ) -> bytes:
        if associated_data is None:
            associated_data = []

        self._check_params(data, associated_data)

        return aead._decrypt(backend, self, b"", data, associated_data, 16)

    def _check_params(
        self,
        data: bytes,
        associated_data: typing.List[bytes],
    ) -> None:
        utils._check_byteslike("data", data)
        if len(data) == 0:
            raise ValueError("data must not be zero length")

        if not isinstance(associated_data, list):
            raise TypeError(
                "associated_data must be a list of bytes-like objects or None"
            )
        for x in associated_data:
            utils._check_byteslike("associated_data elements", x)
