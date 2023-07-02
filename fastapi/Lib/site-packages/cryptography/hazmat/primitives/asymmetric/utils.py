# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from cryptography.hazmat.bindings._rust import asn1
from cryptography.hazmat.primitives import hashes

decode_dss_signature = asn1.decode_dss_signature
encode_dss_signature = asn1.encode_dss_signature


class Prehashed:
    def __init__(self, algorithm: hashes.HashAlgorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError("Expected instance of HashAlgorithm.")

        self._algorithm = algorithm
        self._digest_size = algorithm.digest_size

    @property
    def digest_size(self) -> int:
        return self._digest_size
