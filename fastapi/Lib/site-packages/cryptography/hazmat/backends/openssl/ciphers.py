# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography.exceptions import InvalidTag, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms, modes

if typing.TYPE_CHECKING:
    from cryptography.hazmat.backends.openssl.backend import Backend


class _CipherContext:
    _ENCRYPT = 1
    _DECRYPT = 0
    _MAX_CHUNK_SIZE = 2**30 - 1

    def __init__(self, backend: Backend, cipher, mode, operation: int) -> None:
        self._backend = backend
        self._cipher = cipher
        self._mode = mode
        self._operation = operation
        self._tag: typing.Optional[bytes] = None

        if isinstance(self._cipher, ciphers.BlockCipherAlgorithm):
            self._block_size_bytes = self._cipher.block_size // 8
        else:
            self._block_size_bytes = 1

        ctx = self._backend._lib.EVP_CIPHER_CTX_new()
        ctx = self._backend._ffi.gc(ctx, self._backend._lib.EVP_CIPHER_CTX_free)

        registry = self._backend._cipher_registry
        try:
            adapter = registry[type(cipher), type(mode)]
        except KeyError:
            raise UnsupportedAlgorithm(
                "cipher {} in {} mode is not supported "
                "by this backend.".format(cipher.name, mode.name if mode else mode),
                _Reasons.UNSUPPORTED_CIPHER,
            )

        evp_cipher = adapter(self._backend, cipher, mode)
        if evp_cipher == self._backend._ffi.NULL:
            msg = f"cipher {cipher.name} "
            if mode is not None:
                msg += f"in {mode.name} mode "
            msg += (
                "is not supported by this backend (Your version of OpenSSL "
                "may be too old. Current version: {}.)"
            ).format(self._backend.openssl_version_text())
            raise UnsupportedAlgorithm(msg, _Reasons.UNSUPPORTED_CIPHER)

        if isinstance(mode, modes.ModeWithInitializationVector):
            iv_nonce = self._backend._ffi.from_buffer(mode.initialization_vector)
        elif isinstance(mode, modes.ModeWithTweak):
            iv_nonce = self._backend._ffi.from_buffer(mode.tweak)
        elif isinstance(mode, modes.ModeWithNonce):
            iv_nonce = self._backend._ffi.from_buffer(mode.nonce)
        elif isinstance(cipher, algorithms.ChaCha20):
            iv_nonce = self._backend._ffi.from_buffer(cipher.nonce)
        else:
            iv_nonce = self._backend._ffi.NULL
        # begin init with cipher and operation type
        res = self._backend._lib.EVP_CipherInit_ex(
            ctx,
            evp_cipher,
            self._backend._ffi.NULL,
            self._backend._ffi.NULL,
            self._backend._ffi.NULL,
            operation,
        )
        self._backend.openssl_assert(res != 0)
        # set the key length to handle variable key ciphers
        res = self._backend._lib.EVP_CIPHER_CTX_set_key_length(ctx, len(cipher.key))
        self._backend.openssl_assert(res != 0)
        if isinstance(mode, modes.GCM):
            res = self._backend._lib.EVP_CIPHER_CTX_ctrl(
                ctx,
                self._backend._lib.EVP_CTRL_AEAD_SET_IVLEN,
                len(iv_nonce),
                self._backend._ffi.NULL,
            )
            self._backend.openssl_assert(res != 0)
            if mode.tag is not None:
                res = self._backend._lib.EVP_CIPHER_CTX_ctrl(
                    ctx,
                    self._backend._lib.EVP_CTRL_AEAD_SET_TAG,
                    len(mode.tag),
                    mode.tag,
                )
                self._backend.openssl_assert(res != 0)
                self._tag = mode.tag

        # pass key/iv
        res = self._backend._lib.EVP_CipherInit_ex(
            ctx,
            self._backend._ffi.NULL,
            self._backend._ffi.NULL,
            self._backend._ffi.from_buffer(cipher.key),
            iv_nonce,
            operation,
        )

        # Check for XTS mode duplicate keys error
        errors = self._backend._consume_errors()
        lib = self._backend._lib
        if res == 0 and (
            (
                not lib.CRYPTOGRAPHY_IS_LIBRESSL
                and errors[0]._lib_reason_match(
                    lib.ERR_LIB_EVP, lib.EVP_R_XTS_DUPLICATED_KEYS
                )
            )
            or (
                lib.Cryptography_HAS_PROVIDERS
                and errors[0]._lib_reason_match(
                    lib.ERR_LIB_PROV, lib.PROV_R_XTS_DUPLICATED_KEYS
                )
            )
        ):
            raise ValueError("In XTS mode duplicated keys are not allowed")

        self._backend.openssl_assert(res != 0, errors=errors)

        # We purposely disable padding here as it's handled higher up in the
        # API.
        self._backend._lib.EVP_CIPHER_CTX_set_padding(ctx, 0)
        self._ctx = ctx

    def update(self, data: bytes) -> bytes:
        buf = bytearray(len(data) + self._block_size_bytes - 1)
        n = self.update_into(data, buf)
        return bytes(buf[:n])

    def update_into(self, data: bytes, buf: bytes) -> int:
        total_data_len = len(data)
        if len(buf) < (total_data_len + self._block_size_bytes - 1):
            raise ValueError(
                "buffer must be at least {} bytes for this "
                "payload".format(len(data) + self._block_size_bytes - 1)
            )

        data_processed = 0
        total_out = 0
        outlen = self._backend._ffi.new("int *")
        baseoutbuf = self._backend._ffi.from_buffer(buf, require_writable=True)
        baseinbuf = self._backend._ffi.from_buffer(data)

        while data_processed != total_data_len:
            outbuf = baseoutbuf + total_out
            inbuf = baseinbuf + data_processed
            inlen = min(self._MAX_CHUNK_SIZE, total_data_len - data_processed)

            res = self._backend._lib.EVP_CipherUpdate(
                self._ctx, outbuf, outlen, inbuf, inlen
            )
            if res == 0 and isinstance(self._mode, modes.XTS):
                self._backend._consume_errors()
                raise ValueError(
                    "In XTS mode you must supply at least a full block in the "
                    "first update call. For AES this is 16 bytes."
                )
            else:
                self._backend.openssl_assert(res != 0)
            data_processed += inlen
            total_out += outlen[0]

        return total_out

    def finalize(self) -> bytes:
        if (
            self._operation == self._DECRYPT
            and isinstance(self._mode, modes.ModeWithAuthenticationTag)
            and self.tag is None
        ):
            raise ValueError("Authentication tag must be provided when decrypting.")

        buf = self._backend._ffi.new("unsigned char[]", self._block_size_bytes)
        outlen = self._backend._ffi.new("int *")
        res = self._backend._lib.EVP_CipherFinal_ex(self._ctx, buf, outlen)
        if res == 0:
            errors = self._backend._consume_errors()

            if not errors and isinstance(self._mode, modes.GCM):
                raise InvalidTag

            lib = self._backend._lib
            self._backend.openssl_assert(
                errors[0]._lib_reason_match(
                    lib.ERR_LIB_EVP,
                    lib.EVP_R_DATA_NOT_MULTIPLE_OF_BLOCK_LENGTH,
                )
                or (
                    lib.Cryptography_HAS_PROVIDERS
                    and errors[0]._lib_reason_match(
                        lib.ERR_LIB_PROV,
                        lib.PROV_R_WRONG_FINAL_BLOCK_LENGTH,
                    )
                )
                or (
                    lib.CRYPTOGRAPHY_IS_BORINGSSL
                    and errors[0].reason
                    == lib.CIPHER_R_DATA_NOT_MULTIPLE_OF_BLOCK_LENGTH
                ),
                errors=errors,
            )
            raise ValueError(
                "The length of the provided data is not a multiple of "
                "the block length."
            )

        if isinstance(self._mode, modes.GCM) and self._operation == self._ENCRYPT:
            tag_buf = self._backend._ffi.new("unsigned char[]", self._block_size_bytes)
            res = self._backend._lib.EVP_CIPHER_CTX_ctrl(
                self._ctx,
                self._backend._lib.EVP_CTRL_AEAD_GET_TAG,
                self._block_size_bytes,
                tag_buf,
            )
            self._backend.openssl_assert(res != 0)
            self._tag = self._backend._ffi.buffer(tag_buf)[:]

        res = self._backend._lib.EVP_CIPHER_CTX_reset(self._ctx)
        self._backend.openssl_assert(res == 1)
        return self._backend._ffi.buffer(buf)[: outlen[0]]

    def finalize_with_tag(self, tag: bytes) -> bytes:
        tag_len = len(tag)
        if tag_len < self._mode._min_tag_length:
            raise ValueError(
                "Authentication tag must be {} bytes or longer.".format(
                    self._mode._min_tag_length
                )
            )
        elif tag_len > self._block_size_bytes:
            raise ValueError(
                "Authentication tag cannot be more than {} bytes.".format(
                    self._block_size_bytes
                )
            )
        res = self._backend._lib.EVP_CIPHER_CTX_ctrl(
            self._ctx, self._backend._lib.EVP_CTRL_AEAD_SET_TAG, len(tag), tag
        )
        self._backend.openssl_assert(res != 0)
        self._tag = tag
        return self.finalize()

    def authenticate_additional_data(self, data: bytes) -> None:
        outlen = self._backend._ffi.new("int *")
        res = self._backend._lib.EVP_CipherUpdate(
            self._ctx,
            self._backend._ffi.NULL,
            outlen,
            self._backend._ffi.from_buffer(data),
            len(data),
        )
        self._backend.openssl_assert(res != 0)

    @property
    def tag(self) -> typing.Optional[bytes]:
        return self._tag
