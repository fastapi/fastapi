# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

if typing.TYPE_CHECKING:
    from cryptography.hazmat.backends.openssl.backend import Backend


def _evp_pkey_derive(backend: Backend, evp_pkey, peer_public_key) -> bytes:
    ctx = backend._lib.EVP_PKEY_CTX_new(evp_pkey, backend._ffi.NULL)
    backend.openssl_assert(ctx != backend._ffi.NULL)
    ctx = backend._ffi.gc(ctx, backend._lib.EVP_PKEY_CTX_free)
    res = backend._lib.EVP_PKEY_derive_init(ctx)
    backend.openssl_assert(res == 1)

    if backend._lib.Cryptography_HAS_EVP_PKEY_SET_PEER_EX:
        res = backend._lib.EVP_PKEY_derive_set_peer_ex(
            ctx, peer_public_key._evp_pkey, 0
        )
    else:
        res = backend._lib.EVP_PKEY_derive_set_peer(ctx, peer_public_key._evp_pkey)
    backend.openssl_assert(res == 1)

    keylen = backend._ffi.new("size_t *")
    res = backend._lib.EVP_PKEY_derive(ctx, backend._ffi.NULL, keylen)
    backend.openssl_assert(res == 1)
    backend.openssl_assert(keylen[0] > 0)
    buf = backend._ffi.new("unsigned char[]", keylen[0])
    res = backend._lib.EVP_PKEY_derive(ctx, buf, keylen)
    if res != 1:
        errors = backend._consume_errors()
        raise ValueError("Error computing shared key.", errors)

    return backend._ffi.buffer(buf, keylen[0])[:]


def _calculate_digest_and_algorithm(
    data: bytes,
    algorithm: typing.Union[Prehashed, hashes.HashAlgorithm],
) -> typing.Tuple[bytes, hashes.HashAlgorithm]:
    if not isinstance(algorithm, Prehashed):
        hash_ctx = hashes.Hash(algorithm)
        hash_ctx.update(data)
        data = hash_ctx.finalize()
    else:
        algorithm = algorithm._algorithm

    if len(data) != algorithm.digest_size:
        raise ValueError(
            "The provided data must be the same length as the hash "
            "algorithm's digest size."
        )

    return (data, algorithm)
