# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import typing

class TestCertificate:
    not_after_tag: int
    not_before_tag: int
    issuer_value_tags: typing.List[int]
    subject_value_tags: typing.List[int]

def decode_dss_signature(signature: bytes) -> typing.Tuple[int, int]: ...
def encode_dss_signature(r: int, s: int) -> bytes: ...
def parse_spki_for_data(data: bytes) -> bytes: ...
def test_parse_certificate(data: bytes) -> TestCertificate: ...
