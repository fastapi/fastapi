# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import hashes

__all__ = ["HMAC"]

HMAC = rust_openssl.hmac.HMAC
hashes.HashContext.register(HMAC)
