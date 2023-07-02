# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import typing

from cryptography import utils
from cryptography.exceptions import AlreadyFinalized
from cryptography.hazmat.bindings._rust import (
    check_ansix923_padding,
    check_pkcs7_padding,
)


class PaddingContext(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, data: bytes) -> bytes:
        """
        Pads the provided bytes and returns any available data as bytes.
        """

    @abc.abstractmethod
    def finalize(self) -> bytes:
        """
        Finalize the padding, returns bytes.
        """


def _byte_padding_check(block_size: int) -> None:
    if not (0 <= block_size <= 2040):
        raise ValueError("block_size must be in range(0, 2041).")

    if block_size % 8 != 0:
        raise ValueError("block_size must be a multiple of 8.")


def _byte_padding_update(
    buffer_: typing.Optional[bytes], data: bytes, block_size: int
) -> typing.Tuple[bytes, bytes]:
    if buffer_ is None:
        raise AlreadyFinalized("Context was already finalized.")

    utils._check_byteslike("data", data)

    buffer_ += bytes(data)

    finished_blocks = len(buffer_) // (block_size // 8)

    result = buffer_[: finished_blocks * (block_size // 8)]
    buffer_ = buffer_[finished_blocks * (block_size // 8) :]

    return buffer_, result


def _byte_padding_pad(
    buffer_: typing.Optional[bytes],
    block_size: int,
    paddingfn: typing.Callable[[int], bytes],
) -> bytes:
    if buffer_ is None:
        raise AlreadyFinalized("Context was already finalized.")

    pad_size = block_size // 8 - len(buffer_)
    return buffer_ + paddingfn(pad_size)


def _byte_unpadding_update(
    buffer_: typing.Optional[bytes], data: bytes, block_size: int
) -> typing.Tuple[bytes, bytes]:
    if buffer_ is None:
        raise AlreadyFinalized("Context was already finalized.")

    utils._check_byteslike("data", data)

    buffer_ += bytes(data)

    finished_blocks = max(len(buffer_) // (block_size // 8) - 1, 0)

    result = buffer_[: finished_blocks * (block_size // 8)]
    buffer_ = buffer_[finished_blocks * (block_size // 8) :]

    return buffer_, result


def _byte_unpadding_check(
    buffer_: typing.Optional[bytes],
    block_size: int,
    checkfn: typing.Callable[[bytes], int],
) -> bytes:
    if buffer_ is None:
        raise AlreadyFinalized("Context was already finalized.")

    if len(buffer_) != block_size // 8:
        raise ValueError("Invalid padding bytes.")

    valid = checkfn(buffer_)

    if not valid:
        raise ValueError("Invalid padding bytes.")

    pad_size = buffer_[-1]
    return buffer_[:-pad_size]


class PKCS7:
    def __init__(self, block_size: int):
        _byte_padding_check(block_size)
        self.block_size = block_size

    def padder(self) -> PaddingContext:
        return _PKCS7PaddingContext(self.block_size)

    def unpadder(self) -> PaddingContext:
        return _PKCS7UnpaddingContext(self.block_size)


class _PKCS7PaddingContext(PaddingContext):
    _buffer: typing.Optional[bytes]

    def __init__(self, block_size: int):
        self.block_size = block_size
        # TODO: more copies than necessary, we should use zero-buffer (#193)
        self._buffer = b""

    def update(self, data: bytes) -> bytes:
        self._buffer, result = _byte_padding_update(self._buffer, data, self.block_size)
        return result

    def _padding(self, size: int) -> bytes:
        return bytes([size]) * size

    def finalize(self) -> bytes:
        result = _byte_padding_pad(self._buffer, self.block_size, self._padding)
        self._buffer = None
        return result


class _PKCS7UnpaddingContext(PaddingContext):
    _buffer: typing.Optional[bytes]

    def __init__(self, block_size: int):
        self.block_size = block_size
        # TODO: more copies than necessary, we should use zero-buffer (#193)
        self._buffer = b""

    def update(self, data: bytes) -> bytes:
        self._buffer, result = _byte_unpadding_update(
            self._buffer, data, self.block_size
        )
        return result

    def finalize(self) -> bytes:
        result = _byte_unpadding_check(
            self._buffer, self.block_size, check_pkcs7_padding
        )
        self._buffer = None
        return result


class ANSIX923:
    def __init__(self, block_size: int):
        _byte_padding_check(block_size)
        self.block_size = block_size

    def padder(self) -> PaddingContext:
        return _ANSIX923PaddingContext(self.block_size)

    def unpadder(self) -> PaddingContext:
        return _ANSIX923UnpaddingContext(self.block_size)


class _ANSIX923PaddingContext(PaddingContext):
    _buffer: typing.Optional[bytes]

    def __init__(self, block_size: int):
        self.block_size = block_size
        # TODO: more copies than necessary, we should use zero-buffer (#193)
        self._buffer = b""

    def update(self, data: bytes) -> bytes:
        self._buffer, result = _byte_padding_update(self._buffer, data, self.block_size)
        return result

    def _padding(self, size: int) -> bytes:
        return bytes([0]) * (size - 1) + bytes([size])

    def finalize(self) -> bytes:
        result = _byte_padding_pad(self._buffer, self.block_size, self._padding)
        self._buffer = None
        return result


class _ANSIX923UnpaddingContext(PaddingContext):
    _buffer: typing.Optional[bytes]

    def __init__(self, block_size: int):
        self.block_size = block_size
        # TODO: more copies than necessary, we should use zero-buffer (#193)
        self._buffer = b""

    def update(self, data: bytes) -> bytes:
        self._buffer, result = _byte_unpadding_update(
            self._buffer, data, self.block_size
        )
        return result

    def finalize(self) -> bytes:
        result = _byte_unpadding_check(
            self._buffer,
            self.block_size,
            check_ansix923_padding,
        )
        self._buffer = None
        return result
