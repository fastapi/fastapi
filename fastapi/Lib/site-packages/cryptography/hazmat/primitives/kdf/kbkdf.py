# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.exceptions import (
    AlreadyFinalized,
    InvalidKey,
    UnsupportedAlgorithm,
    _Reasons,
)
from cryptography.hazmat.primitives import (
    ciphers,
    cmac,
    constant_time,
    hashes,
    hmac,
)
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction


class Mode(utils.Enum):
    CounterMode = "ctr"


class CounterLocation(utils.Enum):
    BeforeFixed = "before_fixed"
    AfterFixed = "after_fixed"
    MiddleFixed = "middle_fixed"


class _KBKDFDeriver:
    def __init__(
        self,
        prf: typing.Callable,
        mode: Mode,
        length: int,
        rlen: int,
        llen: typing.Optional[int],
        location: CounterLocation,
        break_location: typing.Optional[int],
        label: typing.Optional[bytes],
        context: typing.Optional[bytes],
        fixed: typing.Optional[bytes],
    ):
        assert callable(prf)

        if not isinstance(mode, Mode):
            raise TypeError("mode must be of type Mode")

        if not isinstance(location, CounterLocation):
            raise TypeError("location must be of type CounterLocation")

        if break_location is None and location is CounterLocation.MiddleFixed:
            raise ValueError("Please specify a break_location")

        if break_location is not None and location != CounterLocation.MiddleFixed:
            raise ValueError(
                "break_location is ignored when location is not"
                " CounterLocation.MiddleFixed"
            )

        if break_location is not None and not isinstance(break_location, int):
            raise TypeError("break_location must be an integer")

        if break_location is not None and break_location < 0:
            raise ValueError("break_location must be a positive integer")

        if (label or context) and fixed:
            raise ValueError(
                "When supplying fixed data, " "label and context are ignored."
            )

        if rlen is None or not self._valid_byte_length(rlen):
            raise ValueError("rlen must be between 1 and 4")

        if llen is None and fixed is None:
            raise ValueError("Please specify an llen")

        if llen is not None and not isinstance(llen, int):
            raise TypeError("llen must be an integer")

        if label is None:
            label = b""

        if context is None:
            context = b""

        utils._check_bytes("label", label)
        utils._check_bytes("context", context)
        self._prf = prf
        self._mode = mode
        self._length = length
        self._rlen = rlen
        self._llen = llen
        self._location = location
        self._break_location = break_location
        self._label = label
        self._context = context
        self._used = False
        self._fixed_data = fixed

    @staticmethod
    def _valid_byte_length(value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError("value must be of type int")

        value_bin = utils.int_to_bytes(1, value)
        if not 1 <= len(value_bin) <= 4:
            return False
        return True

    def derive(self, key_material: bytes, prf_output_size: int) -> bytes:
        if self._used:
            raise AlreadyFinalized

        utils._check_byteslike("key_material", key_material)
        self._used = True

        # inverse floor division (equivalent to ceiling)
        rounds = -(-self._length // prf_output_size)

        output = [b""]

        # For counter mode, the number of iterations shall not be
        # larger than 2^r-1, where r <= 32 is the binary length of the counter
        # This ensures that the counter values used as an input to the
        # PRF will not repeat during a particular call to the KDF function.
        r_bin = utils.int_to_bytes(1, self._rlen)
        if rounds > pow(2, len(r_bin) * 8) - 1:
            raise ValueError("There are too many iterations.")

        fixed = self._generate_fixed_input()

        if self._location == CounterLocation.BeforeFixed:
            data_before_ctr = b""
            data_after_ctr = fixed
        elif self._location == CounterLocation.AfterFixed:
            data_before_ctr = fixed
            data_after_ctr = b""
        else:
            if isinstance(self._break_location, int) and self._break_location > len(
                fixed
            ):
                raise ValueError("break_location offset > len(fixed)")
            data_before_ctr = fixed[: self._break_location]
            data_after_ctr = fixed[self._break_location :]

        for i in range(1, rounds + 1):
            h = self._prf(key_material)

            counter = utils.int_to_bytes(i, self._rlen)
            input_data = data_before_ctr + counter + data_after_ctr

            h.update(input_data)

            output.append(h.finalize())

        return b"".join(output)[: self._length]

    def _generate_fixed_input(self) -> bytes:
        if self._fixed_data and isinstance(self._fixed_data, bytes):
            return self._fixed_data

        l_val = utils.int_to_bytes(self._length * 8, self._llen)

        return b"".join([self._label, b"\x00", self._context, l_val])


class KBKDFHMAC(KeyDerivationFunction):
    def __init__(
        self,
        algorithm: hashes.HashAlgorithm,
        mode: Mode,
        length: int,
        rlen: int,
        llen: typing.Optional[int],
        location: CounterLocation,
        label: typing.Optional[bytes],
        context: typing.Optional[bytes],
        fixed: typing.Optional[bytes],
        backend: typing.Any = None,
        *,
        break_location: typing.Optional[int] = None,
    ):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise UnsupportedAlgorithm(
                "Algorithm supplied is not a supported hash algorithm.",
                _Reasons.UNSUPPORTED_HASH,
            )

        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        if not ossl.hmac_supported(algorithm):
            raise UnsupportedAlgorithm(
                "Algorithm supplied is not a supported hmac algorithm.",
                _Reasons.UNSUPPORTED_HASH,
            )

        self._algorithm = algorithm

        self._deriver = _KBKDFDeriver(
            self._prf,
            mode,
            length,
            rlen,
            llen,
            location,
            break_location,
            label,
            context,
            fixed,
        )

    def _prf(self, key_material: bytes) -> hmac.HMAC:
        return hmac.HMAC(key_material, self._algorithm)

    def derive(self, key_material: bytes) -> bytes:
        return self._deriver.derive(key_material, self._algorithm.digest_size)

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey


class KBKDFCMAC(KeyDerivationFunction):
    def __init__(
        self,
        algorithm,
        mode: Mode,
        length: int,
        rlen: int,
        llen: typing.Optional[int],
        location: CounterLocation,
        label: typing.Optional[bytes],
        context: typing.Optional[bytes],
        fixed: typing.Optional[bytes],
        backend: typing.Any = None,
        *,
        break_location: typing.Optional[int] = None,
    ):
        if not issubclass(algorithm, ciphers.BlockCipherAlgorithm) or not issubclass(
            algorithm, ciphers.CipherAlgorithm
        ):
            raise UnsupportedAlgorithm(
                "Algorithm supplied is not a supported cipher algorithm.",
                _Reasons.UNSUPPORTED_CIPHER,
            )

        self._algorithm = algorithm
        self._cipher: typing.Optional[ciphers.BlockCipherAlgorithm] = None

        self._deriver = _KBKDFDeriver(
            self._prf,
            mode,
            length,
            rlen,
            llen,
            location,
            break_location,
            label,
            context,
            fixed,
        )

    def _prf(self, _: bytes) -> cmac.CMAC:
        assert self._cipher is not None

        return cmac.CMAC(self._cipher)

    def derive(self, key_material: bytes) -> bytes:
        self._cipher = self._algorithm(key_material)

        assert self._cipher is not None

        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        if not ossl.cmac_algorithm_supported(self._cipher):
            raise UnsupportedAlgorithm(
                "Algorithm supplied is not a supported cipher algorithm.",
                _Reasons.UNSUPPORTED_CIPHER,
            )

        return self._deriver.derive(key_material, self._cipher.block_size // 8)

    def verify(self, key_material: bytes, expected_key: bytes) -> None:
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey
