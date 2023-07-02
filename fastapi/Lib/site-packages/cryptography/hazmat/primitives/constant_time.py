# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import hmac


def bytes_eq(a: bytes, b: bytes) -> bool:
    if not isinstance(a, bytes) or not isinstance(b, bytes):
        raise TypeError("a and b must be bytes.")

    return hmac.compare_digest(a, b)
