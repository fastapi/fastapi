# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import base64
import typing
from urllib.parse import quote, urlencode

from cryptography.hazmat.primitives import constant_time, hmac
from cryptography.hazmat.primitives.hashes import SHA1, SHA256, SHA512
from cryptography.hazmat.primitives.twofactor import InvalidToken

HOTPHashTypes = typing.Union[SHA1, SHA256, SHA512]


def _generate_uri(
    hotp: HOTP,
    type_name: str,
    account_name: str,
    issuer: typing.Optional[str],
    extra_parameters: typing.List[typing.Tuple[str, int]],
) -> str:
    parameters = [
        ("digits", hotp._length),
        ("secret", base64.b32encode(hotp._key)),
        ("algorithm", hotp._algorithm.name.upper()),
    ]

    if issuer is not None:
        parameters.append(("issuer", issuer))

    parameters.extend(extra_parameters)

    label = f"{quote(issuer)}:{quote(account_name)}" if issuer else quote(account_name)
    return f"otpauth://{type_name}/{label}?{urlencode(parameters)}"


class HOTP:
    def __init__(
        self,
        key: bytes,
        length: int,
        algorithm: HOTPHashTypes,
        backend: typing.Any = None,
        enforce_key_length: bool = True,
    ) -> None:
        if len(key) < 16 and enforce_key_length is True:
            raise ValueError("Key length has to be at least 128 bits.")

        if not isinstance(length, int):
            raise TypeError("Length parameter must be an integer type.")

        if length < 6 or length > 8:
            raise ValueError("Length of HOTP has to be between 6 and 8.")

        if not isinstance(algorithm, (SHA1, SHA256, SHA512)):
            raise TypeError("Algorithm must be SHA1, SHA256 or SHA512.")

        self._key = key
        self._length = length
        self._algorithm = algorithm

    def generate(self, counter: int) -> bytes:
        truncated_value = self._dynamic_truncate(counter)
        hotp = truncated_value % (10**self._length)
        return "{0:0{1}}".format(hotp, self._length).encode()

    def verify(self, hotp: bytes, counter: int) -> None:
        if not constant_time.bytes_eq(self.generate(counter), hotp):
            raise InvalidToken("Supplied HOTP value does not match.")

    def _dynamic_truncate(self, counter: int) -> int:
        ctx = hmac.HMAC(self._key, self._algorithm)
        ctx.update(counter.to_bytes(length=8, byteorder="big"))
        hmac_value = ctx.finalize()

        offset = hmac_value[len(hmac_value) - 1] & 0b1111
        p = hmac_value[offset : offset + 4]
        return int.from_bytes(p, byteorder="big") & 0x7FFFFFFF

    def get_provisioning_uri(
        self, account_name: str, counter: int, issuer: typing.Optional[str]
    ) -> str:
        return _generate_uri(
            self, "hotp", account_name, issuer, [("counter", int(counter))]
        )
