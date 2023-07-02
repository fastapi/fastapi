# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from typing import Any


def default_backend() -> Any:
    from cryptography.hazmat.backends.openssl.backend import backend

    return backend
