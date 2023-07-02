# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from cryptography import utils
from cryptography.hazmat.primitives.ciphers import (
    BlockCipherAlgorithm,
    CipherAlgorithm,
)


def _verify_key_size(algorithm: CipherAlgorithm, key: bytes) -> bytes:
    # Verify that the key is instance of bytes
    utils._check_byteslike("key", key)

    # Verify that the key size matches the expected key size
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError(
            "Invalid key size ({}) for {}.".format(len(key) * 8, algorithm.name)
        )
    return key


class AES(BlockCipherAlgorithm):
    name = "AES"
    block_size = 128
    # 512 added to support AES-256-XTS, which uses 512-bit keys
    key_sizes = frozenset([128, 192, 256, 512])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class AES128(BlockCipherAlgorithm):
    name = "AES"
    block_size = 128
    key_sizes = frozenset([128])
    key_size = 128

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)


class AES256(BlockCipherAlgorithm):
    name = "AES"
    block_size = 128
    key_sizes = frozenset([256])
    key_size = 256

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)


class Camellia(BlockCipherAlgorithm):
    name = "camellia"
    block_size = 128
    key_sizes = frozenset([128, 192, 256])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class TripleDES(BlockCipherAlgorithm):
    name = "3DES"
    block_size = 64
    key_sizes = frozenset([64, 128, 192])

    def __init__(self, key: bytes):
        if len(key) == 8:
            key += key + key
        elif len(key) == 16:
            key += key[:8]
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class Blowfish(BlockCipherAlgorithm):
    name = "Blowfish"
    block_size = 64
    key_sizes = frozenset(range(32, 449, 8))

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


_BlowfishInternal = Blowfish
utils.deprecated(
    Blowfish,
    __name__,
    "Blowfish has been deprecated",
    utils.DeprecatedIn37,
    name="Blowfish",
)


class CAST5(BlockCipherAlgorithm):
    name = "CAST5"
    block_size = 64
    key_sizes = frozenset(range(40, 129, 8))

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


_CAST5Internal = CAST5
utils.deprecated(
    CAST5,
    __name__,
    "CAST5 has been deprecated",
    utils.DeprecatedIn37,
    name="CAST5",
)


class ARC4(CipherAlgorithm):
    name = "RC4"
    key_sizes = frozenset([40, 56, 64, 80, 128, 160, 192, 256])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class IDEA(BlockCipherAlgorithm):
    name = "IDEA"
    block_size = 64
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


_IDEAInternal = IDEA
utils.deprecated(
    IDEA,
    __name__,
    "IDEA has been deprecated",
    utils.DeprecatedIn37,
    name="IDEA",
)


class SEED(BlockCipherAlgorithm):
    name = "SEED"
    block_size = 128
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


_SEEDInternal = SEED
utils.deprecated(
    SEED,
    __name__,
    "SEED has been deprecated",
    utils.DeprecatedIn37,
    name="SEED",
)


class ChaCha20(CipherAlgorithm):
    name = "ChaCha20"
    key_sizes = frozenset([256])

    def __init__(self, key: bytes, nonce: bytes):
        self.key = _verify_key_size(self, key)
        utils._check_byteslike("nonce", nonce)

        if len(nonce) != 16:
            raise ValueError("nonce must be 128-bits (16 bytes)")

        self._nonce = nonce

    @property
    def nonce(self) -> bytes:
        return self._nonce

    @property
    def key_size(self) -> int:
        return len(self.key) * 8


class SM4(BlockCipherAlgorithm):
    name = "SM4"
    block_size = 128
    key_sizes = frozenset([128])

    def __init__(self, key: bytes):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self) -> int:
        return len(self.key) * 8
