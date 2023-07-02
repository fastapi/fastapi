# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import (
    HOTP,
    HOTPHashTypes,
    _generate_uri,
)


class TOTP:
    def __init__(
        self,
        key: bytes,
        length: int,
        algorithm: HOTPHashTypes,
        time_step: int,
        backend: typing.Any = None,
        enforce_key_length: bool = True,
    ):
        self._time_step = time_step
        self._hotp = HOTP(key, length, algorithm, enforce_key_length=enforce_key_length)

    def generate(self, time: typing.Union[int, float]) -> bytes:
        counter = int(time / self._time_step)
        return self._hotp.generate(counter)

    def verify(self, totp: bytes, time: int) -> None:
        if not constant_time.bytes_eq(self.generate(time), totp):
            raise InvalidToken("Supplied TOTP value does not match.")

    def get_provisioning_uri(
        self, account_name: str, issuer: typing.Optional[str]
    ) -> str:
        return _generate_uri(
            self._hotp,
            "totp",
            account_name,
            issuer,
            [("period", int(self._time_step))],
        )
