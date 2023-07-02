# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from cryptography.hazmat.primitives.hashes import HashAlgorithm

def derive_pbkdf2_hmac(
    key_material: bytes,
    algorithm: HashAlgorithm,
    salt: bytes,
    iterations: int,
    length: int,
) -> bytes: ...
def derive_scrypt(
    key_material: bytes,
    salt: bytes,
    n: int,
    r: int,
    p: int,
    max_mem: int,
    length: int,
) -> bytes: ...
