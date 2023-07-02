# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography.exceptions import InvalidTag

if typing.TYPE_CHECKING:
    from cryptography.hazmat.backends.openssl.backend import Backend
    from cryptography.hazmat.primitives.ciphers.aead import (
        AESCCM,
        AESGCM,
        AESOCB3,
        AESSIV,
        ChaCha20Poly1305,
    )

    _AEADTypes = typing.Union[AESCCM, AESGCM, AESOCB3, AESSIV, ChaCha20Poly1305]


def _is_evp_aead_supported_cipher(backend: Backend, cipher: _AEADTypes) -> bool:
    """
    Checks whether the given cipher is supported through
    EVP_AEAD rather than the normal OpenSSL EVP_CIPHER API.
    """
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

    return backend._lib.Cryptography_HAS_EVP_AEAD and isinstance(
        cipher, ChaCha20Poly1305
    )


def _aead_cipher_supported(backend: Backend, cipher: _AEADTypes) -> bool:
    if _is_evp_aead_supported_cipher(backend, cipher):
        return True
    else:
        cipher_name = _evp_cipher_cipher_name(cipher)
        if backend._fips_enabled and cipher_name not in backend._fips_aead:
            return False
        # SIV isn't loaded through get_cipherbyname but instead a new fetch API
        # only available in 3.0+. But if we know we're on 3.0+ then we know
        # it's supported.
        if cipher_name.endswith(b"-siv"):
            return backend._lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER == 1
        else:
            return backend._lib.EVP_get_cipherbyname(cipher_name) != backend._ffi.NULL


def _aead_create_ctx(
    backend: Backend,
    cipher: _AEADTypes,
    key: bytes,
):
    if _is_evp_aead_supported_cipher(backend, cipher):
        return _evp_aead_create_ctx(backend, cipher, key)
    else:
        return _evp_cipher_create_ctx(backend, cipher, key)


def _encrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any = None,
) -> bytes:
    if _is_evp_aead_supported_cipher(backend, cipher):
        return _evp_aead_encrypt(
            backend, cipher, nonce, data, associated_data, tag_length, ctx
        )
    else:
        return _evp_cipher_encrypt(
            backend, cipher, nonce, data, associated_data, tag_length, ctx
        )


def _decrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any = None,
) -> bytes:
    if _is_evp_aead_supported_cipher(backend, cipher):
        return _evp_aead_decrypt(
            backend, cipher, nonce, data, associated_data, tag_length, ctx
        )
    else:
        return _evp_cipher_decrypt(
            backend, cipher, nonce, data, associated_data, tag_length, ctx
        )


def _evp_aead_create_ctx(
    backend: Backend,
    cipher: _AEADTypes,
    key: bytes,
    tag_len: typing.Optional[int] = None,
):
    aead_cipher = _evp_aead_get_cipher(backend, cipher)
    assert aead_cipher is not None
    key_ptr = backend._ffi.from_buffer(key)
    tag_len = backend._lib.EVP_AEAD_DEFAULT_TAG_LENGTH if tag_len is None else tag_len
    ctx = backend._lib.Cryptography_EVP_AEAD_CTX_new(
        aead_cipher, key_ptr, len(key), tag_len
    )
    backend.openssl_assert(ctx != backend._ffi.NULL)
    ctx = backend._ffi.gc(ctx, backend._lib.EVP_AEAD_CTX_free)
    return ctx


def _evp_aead_get_cipher(backend: Backend, cipher: _AEADTypes):
    from cryptography.hazmat.primitives.ciphers.aead import (
        ChaCha20Poly1305,
    )

    # Currently only ChaCha20-Poly1305 is supported using this API
    assert isinstance(cipher, ChaCha20Poly1305)
    return backend._lib.EVP_aead_chacha20_poly1305()


def _evp_aead_encrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any,
) -> bytes:
    assert ctx is not None

    aead_cipher = _evp_aead_get_cipher(backend, cipher)
    assert aead_cipher is not None

    out_len = backend._ffi.new("size_t *")
    # max_out_len should be in_len plus the result of
    # EVP_AEAD_max_overhead.
    max_out_len = len(data) + backend._lib.EVP_AEAD_max_overhead(aead_cipher)
    out_buf = backend._ffi.new("uint8_t[]", max_out_len)
    data_ptr = backend._ffi.from_buffer(data)
    nonce_ptr = backend._ffi.from_buffer(nonce)
    aad = b"".join(associated_data)
    aad_ptr = backend._ffi.from_buffer(aad)

    res = backend._lib.EVP_AEAD_CTX_seal(
        ctx,
        out_buf,
        out_len,
        max_out_len,
        nonce_ptr,
        len(nonce),
        data_ptr,
        len(data),
        aad_ptr,
        len(aad),
    )
    backend.openssl_assert(res == 1)
    encrypted_data = backend._ffi.buffer(out_buf, out_len[0])[:]
    return encrypted_data


def _evp_aead_decrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any,
) -> bytes:
    if len(data) < tag_length:
        raise InvalidTag

    assert ctx is not None

    out_len = backend._ffi.new("size_t *")
    #  max_out_len should at least in_len
    max_out_len = len(data)
    out_buf = backend._ffi.new("uint8_t[]", max_out_len)
    data_ptr = backend._ffi.from_buffer(data)
    nonce_ptr = backend._ffi.from_buffer(nonce)
    aad = b"".join(associated_data)
    aad_ptr = backend._ffi.from_buffer(aad)

    res = backend._lib.EVP_AEAD_CTX_open(
        ctx,
        out_buf,
        out_len,
        max_out_len,
        nonce_ptr,
        len(nonce),
        data_ptr,
        len(data),
        aad_ptr,
        len(aad),
    )

    if res == 0:
        backend._consume_errors()
        raise InvalidTag

    decrypted_data = backend._ffi.buffer(out_buf, out_len[0])[:]
    return decrypted_data


_ENCRYPT = 1
_DECRYPT = 0


def _evp_cipher_cipher_name(cipher: _AEADTypes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import (
        AESCCM,
        AESGCM,
        AESOCB3,
        AESSIV,
        ChaCha20Poly1305,
    )

    if isinstance(cipher, ChaCha20Poly1305):
        return b"chacha20-poly1305"
    elif isinstance(cipher, AESCCM):
        return f"aes-{len(cipher._key) * 8}-ccm".encode("ascii")
    elif isinstance(cipher, AESOCB3):
        return f"aes-{len(cipher._key) * 8}-ocb".encode("ascii")
    elif isinstance(cipher, AESSIV):
        return f"aes-{len(cipher._key) * 8 // 2}-siv".encode("ascii")
    else:
        assert isinstance(cipher, AESGCM)
        return f"aes-{len(cipher._key) * 8}-gcm".encode("ascii")


def _evp_cipher(cipher_name: bytes, backend: Backend):
    if cipher_name.endswith(b"-siv"):
        evp_cipher = backend._lib.EVP_CIPHER_fetch(
            backend._ffi.NULL,
            cipher_name,
            backend._ffi.NULL,
        )
        backend.openssl_assert(evp_cipher != backend._ffi.NULL)
        evp_cipher = backend._ffi.gc(evp_cipher, backend._lib.EVP_CIPHER_free)
    else:
        evp_cipher = backend._lib.EVP_get_cipherbyname(cipher_name)
        backend.openssl_assert(evp_cipher != backend._ffi.NULL)

    return evp_cipher


def _evp_cipher_create_ctx(
    backend: Backend,
    cipher: _AEADTypes,
    key: bytes,
):
    ctx = backend._lib.EVP_CIPHER_CTX_new()
    backend.openssl_assert(ctx != backend._ffi.NULL)
    ctx = backend._ffi.gc(ctx, backend._lib.EVP_CIPHER_CTX_free)
    cipher_name = _evp_cipher_cipher_name(cipher)
    evp_cipher = _evp_cipher(cipher_name, backend)
    key_ptr = backend._ffi.from_buffer(key)
    res = backend._lib.EVP_CipherInit_ex(
        ctx,
        evp_cipher,
        backend._ffi.NULL,
        key_ptr,
        backend._ffi.NULL,
        0,
    )
    backend.openssl_assert(res != 0)
    return ctx


def _evp_cipher_aead_setup(
    backend: Backend,
    cipher_name: bytes,
    key: bytes,
    nonce: bytes,
    tag: typing.Optional[bytes],
    tag_len: int,
    operation: int,
):
    evp_cipher = _evp_cipher(cipher_name, backend)
    ctx = backend._lib.EVP_CIPHER_CTX_new()
    ctx = backend._ffi.gc(ctx, backend._lib.EVP_CIPHER_CTX_free)
    res = backend._lib.EVP_CipherInit_ex(
        ctx,
        evp_cipher,
        backend._ffi.NULL,
        backend._ffi.NULL,
        backend._ffi.NULL,
        int(operation == _ENCRYPT),
    )
    backend.openssl_assert(res != 0)
    # CCM requires the IVLEN to be set before calling SET_TAG on decrypt
    res = backend._lib.EVP_CIPHER_CTX_ctrl(
        ctx,
        backend._lib.EVP_CTRL_AEAD_SET_IVLEN,
        len(nonce),
        backend._ffi.NULL,
    )
    backend.openssl_assert(res != 0)
    if operation == _DECRYPT:
        assert tag is not None
        _evp_cipher_set_tag(backend, ctx, tag)
    elif cipher_name.endswith(b"-ccm"):
        res = backend._lib.EVP_CIPHER_CTX_ctrl(
            ctx,
            backend._lib.EVP_CTRL_AEAD_SET_TAG,
            tag_len,
            backend._ffi.NULL,
        )
        backend.openssl_assert(res != 0)

    nonce_ptr = backend._ffi.from_buffer(nonce)
    key_ptr = backend._ffi.from_buffer(key)
    res = backend._lib.EVP_CipherInit_ex(
        ctx,
        backend._ffi.NULL,
        backend._ffi.NULL,
        key_ptr,
        nonce_ptr,
        int(operation == _ENCRYPT),
    )
    backend.openssl_assert(res != 0)
    return ctx


def _evp_cipher_set_tag(backend, ctx, tag: bytes) -> None:
    tag_ptr = backend._ffi.from_buffer(tag)
    res = backend._lib.EVP_CIPHER_CTX_ctrl(
        ctx, backend._lib.EVP_CTRL_AEAD_SET_TAG, len(tag), tag_ptr
    )
    backend.openssl_assert(res != 0)


def _evp_cipher_set_nonce_operation(backend, ctx, nonce: bytes, operation: int) -> None:
    nonce_ptr = backend._ffi.from_buffer(nonce)
    res = backend._lib.EVP_CipherInit_ex(
        ctx,
        backend._ffi.NULL,
        backend._ffi.NULL,
        backend._ffi.NULL,
        nonce_ptr,
        int(operation == _ENCRYPT),
    )
    backend.openssl_assert(res != 0)


def _evp_cipher_set_length(backend: Backend, ctx, data_len: int) -> None:
    intptr = backend._ffi.new("int *")
    res = backend._lib.EVP_CipherUpdate(
        ctx, backend._ffi.NULL, intptr, backend._ffi.NULL, data_len
    )
    backend.openssl_assert(res != 0)


def _evp_cipher_process_aad(backend: Backend, ctx, associated_data: bytes) -> None:
    outlen = backend._ffi.new("int *")
    a_data_ptr = backend._ffi.from_buffer(associated_data)
    res = backend._lib.EVP_CipherUpdate(
        ctx, backend._ffi.NULL, outlen, a_data_ptr, len(associated_data)
    )
    backend.openssl_assert(res != 0)


def _evp_cipher_process_data(backend: Backend, ctx, data: bytes) -> bytes:
    outlen = backend._ffi.new("int *")
    buf = backend._ffi.new("unsigned char[]", len(data))
    data_ptr = backend._ffi.from_buffer(data)
    res = backend._lib.EVP_CipherUpdate(ctx, buf, outlen, data_ptr, len(data))
    if res == 0:
        # AES SIV can error here if the data is invalid on decrypt
        backend._consume_errors()
        raise InvalidTag
    return backend._ffi.buffer(buf, outlen[0])[:]


def _evp_cipher_encrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any = None,
) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESCCM, AESSIV

    if ctx is None:
        cipher_name = _evp_cipher_cipher_name(cipher)
        ctx = _evp_cipher_aead_setup(
            backend,
            cipher_name,
            cipher._key,
            nonce,
            None,
            tag_length,
            _ENCRYPT,
        )
    else:
        _evp_cipher_set_nonce_operation(backend, ctx, nonce, _ENCRYPT)

    # CCM requires us to pass the length of the data before processing
    # anything.
    # However calling this with any other AEAD results in an error
    if isinstance(cipher, AESCCM):
        _evp_cipher_set_length(backend, ctx, len(data))

    for ad in associated_data:
        _evp_cipher_process_aad(backend, ctx, ad)
    processed_data = _evp_cipher_process_data(backend, ctx, data)
    outlen = backend._ffi.new("int *")
    # All AEADs we support besides OCB are streaming so they return nothing
    # in finalization. OCB can return up to (16 byte block - 1) bytes so
    # we need a buffer here too.
    buf = backend._ffi.new("unsigned char[]", 16)
    res = backend._lib.EVP_CipherFinal_ex(ctx, buf, outlen)
    backend.openssl_assert(res != 0)
    processed_data += backend._ffi.buffer(buf, outlen[0])[:]
    tag_buf = backend._ffi.new("unsigned char[]", tag_length)
    res = backend._lib.EVP_CIPHER_CTX_ctrl(
        ctx, backend._lib.EVP_CTRL_AEAD_GET_TAG, tag_length, tag_buf
    )
    backend.openssl_assert(res != 0)
    tag = backend._ffi.buffer(tag_buf)[:]

    if isinstance(cipher, AESSIV):
        # RFC 5297 defines the output as IV || C, where the tag we generate
        # is the "IV" and C is the ciphertext. This is the opposite of our
        # other AEADs, which are Ciphertext || Tag
        backend.openssl_assert(len(tag) == 16)
        return tag + processed_data
    else:
        return processed_data + tag


def _evp_cipher_decrypt(
    backend: Backend,
    cipher: _AEADTypes,
    nonce: bytes,
    data: bytes,
    associated_data: typing.List[bytes],
    tag_length: int,
    ctx: typing.Any = None,
) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESCCM, AESSIV

    if len(data) < tag_length:
        raise InvalidTag

    if isinstance(cipher, AESSIV):
        # RFC 5297 defines the output as IV || C, where the tag we generate
        # is the "IV" and C is the ciphertext. This is the opposite of our
        # other AEADs, which are Ciphertext || Tag
        tag = data[:tag_length]
        data = data[tag_length:]
    else:
        tag = data[-tag_length:]
        data = data[:-tag_length]
    if ctx is None:
        cipher_name = _evp_cipher_cipher_name(cipher)
        ctx = _evp_cipher_aead_setup(
            backend,
            cipher_name,
            cipher._key,
            nonce,
            tag,
            tag_length,
            _DECRYPT,
        )
    else:
        _evp_cipher_set_nonce_operation(backend, ctx, nonce, _DECRYPT)
        _evp_cipher_set_tag(backend, ctx, tag)

    # CCM requires us to pass the length of the data before processing
    # anything.
    # However calling this with any other AEAD results in an error
    if isinstance(cipher, AESCCM):
        _evp_cipher_set_length(backend, ctx, len(data))

    for ad in associated_data:
        _evp_cipher_process_aad(backend, ctx, ad)
    # CCM has a different error path if the tag doesn't match. Errors are
    # raised in Update and Final is irrelevant.
    if isinstance(cipher, AESCCM):
        outlen = backend._ffi.new("int *")
        buf = backend._ffi.new("unsigned char[]", len(data))
        d_ptr = backend._ffi.from_buffer(data)
        res = backend._lib.EVP_CipherUpdate(ctx, buf, outlen, d_ptr, len(data))
        if res != 1:
            backend._consume_errors()
            raise InvalidTag

        processed_data = backend._ffi.buffer(buf, outlen[0])[:]
    else:
        processed_data = _evp_cipher_process_data(backend, ctx, data)
        outlen = backend._ffi.new("int *")
        # OCB can return up to 15 bytes (16 byte block - 1) in finalization
        buf = backend._ffi.new("unsigned char[]", 16)
        res = backend._lib.EVP_CipherFinal_ex(ctx, buf, outlen)
        processed_data += backend._ffi.buffer(buf, outlen[0])[:]
        if res == 0:
            backend._consume_errors()
            raise InvalidTag

    return processed_data
