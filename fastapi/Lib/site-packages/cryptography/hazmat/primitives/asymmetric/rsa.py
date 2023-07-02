# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import typing
from math import gcd

from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils


class RSAPrivateKey(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def decrypt(self, ciphertext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Decrypts the provided ciphertext.
        """

    @property
    @abc.abstractmethod
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """

    @abc.abstractmethod
    def public_key(self) -> RSAPublicKey:
        """
        The RSAPublicKey associated with this private key.
        """

    @abc.abstractmethod
    def sign(
        self,
        data: bytes,
        padding: AsymmetricPadding,
        algorithm: typing.Union[asym_utils.Prehashed, hashes.HashAlgorithm],
    ) -> bytes:
        """
        Signs the data.
        """

    @abc.abstractmethod
    def private_numbers(self) -> RSAPrivateNumbers:
        """
        Returns an RSAPrivateNumbers.
        """

    @abc.abstractmethod
    def private_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PrivateFormat,
        encryption_algorithm: _serialization.KeySerializationEncryption,
    ) -> bytes:
        """
        Returns the key serialized as bytes.
        """


RSAPrivateKeyWithSerialization = RSAPrivateKey


class RSAPublicKey(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encrypt(self, plaintext: bytes, padding: AsymmetricPadding) -> bytes:
        """
        Encrypts the given plaintext.
        """

    @property
    @abc.abstractmethod
    def key_size(self) -> int:
        """
        The bit length of the public modulus.
        """

    @abc.abstractmethod
    def public_numbers(self) -> RSAPublicNumbers:
        """
        Returns an RSAPublicNumbers
        """

    @abc.abstractmethod
    def public_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PublicFormat,
    ) -> bytes:
        """
        Returns the key serialized as bytes.
        """

    @abc.abstractmethod
    def verify(
        self,
        signature: bytes,
        data: bytes,
        padding: AsymmetricPadding,
        algorithm: typing.Union[asym_utils.Prehashed, hashes.HashAlgorithm],
    ) -> None:
        """
        Verifies the signature of the data.
        """

    @abc.abstractmethod
    def recover_data_from_signature(
        self,
        signature: bytes,
        padding: AsymmetricPadding,
        algorithm: typing.Optional[hashes.HashAlgorithm],
    ) -> bytes:
        """
        Recovers the original data from the signature.
        """

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """


RSAPublicKeyWithSerialization = RSAPublicKey


def generate_private_key(
    public_exponent: int,
    key_size: int,
    backend: typing.Any = None,
) -> RSAPrivateKey:
    from cryptography.hazmat.backends.openssl.backend import backend as ossl

    _verify_rsa_parameters(public_exponent, key_size)
    return ossl.generate_rsa_private_key(public_exponent, key_size)


def _verify_rsa_parameters(public_exponent: int, key_size: int) -> None:
    if public_exponent not in (3, 65537):
        raise ValueError(
            "public_exponent must be either 3 (for legacy compatibility) or "
            "65537. Almost everyone should choose 65537 here!"
        )

    if key_size < 512:
        raise ValueError("key_size must be at least 512-bits.")


def _check_private_key_components(
    p: int,
    q: int,
    private_exponent: int,
    dmp1: int,
    dmq1: int,
    iqmp: int,
    public_exponent: int,
    modulus: int,
) -> None:
    if modulus < 3:
        raise ValueError("modulus must be >= 3.")

    if p >= modulus:
        raise ValueError("p must be < modulus.")

    if q >= modulus:
        raise ValueError("q must be < modulus.")

    if dmp1 >= modulus:
        raise ValueError("dmp1 must be < modulus.")

    if dmq1 >= modulus:
        raise ValueError("dmq1 must be < modulus.")

    if iqmp >= modulus:
        raise ValueError("iqmp must be < modulus.")

    if private_exponent >= modulus:
        raise ValueError("private_exponent must be < modulus.")

    if public_exponent < 3 or public_exponent >= modulus:
        raise ValueError("public_exponent must be >= 3 and < modulus.")

    if public_exponent & 1 == 0:
        raise ValueError("public_exponent must be odd.")

    if dmp1 & 1 == 0:
        raise ValueError("dmp1 must be odd.")

    if dmq1 & 1 == 0:
        raise ValueError("dmq1 must be odd.")

    if p * q != modulus:
        raise ValueError("p*q must equal modulus.")


def _check_public_key_components(e: int, n: int) -> None:
    if n < 3:
        raise ValueError("n must be >= 3.")

    if e < 3 or e >= n:
        raise ValueError("e must be >= 3 and < n.")

    if e & 1 == 0:
        raise ValueError("e must be odd.")


def _modinv(e: int, m: int) -> int:
    """
    Modular Multiplicative Inverse. Returns x such that: (x*e) mod m == 1
    """
    x1, x2 = 1, 0
    a, b = e, m
    while b > 0:
        q, r = divmod(a, b)
        xn = x1 - q * x2
        a, b, x1, x2 = b, r, x2, xn
    return x1 % m


def rsa_crt_iqmp(p: int, q: int) -> int:
    """
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    """
    return _modinv(q, p)


def rsa_crt_dmp1(private_exponent: int, p: int) -> int:
    """
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    """
    return private_exponent % (p - 1)


def rsa_crt_dmq1(private_exponent: int, q: int) -> int:
    """
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    """
    return private_exponent % (q - 1)


# Controls the number of iterations rsa_recover_prime_factors will perform
# to obtain the prime factors. Each iteration increments by 2 so the actual
# maximum attempts is half this number.
_MAX_RECOVERY_ATTEMPTS = 1000


def rsa_recover_prime_factors(n: int, e: int, d: int) -> typing.Tuple[int, int]:
    """
    Compute factors p and q from the private exponent d. We assume that n has
    no more than two factors. This function is adapted from code in PyCrypto.
    """
    # See 8.2.2(i) in Handbook of Applied Cryptography.
    ktot = d * e - 1
    # The quantity d*e-1 is a multiple of phi(n), even,
    # and can be represented as t*2^s.
    t = ktot
    while t % 2 == 0:
        t = t // 2
    # Cycle through all multiplicative inverses in Zn.
    # The algorithm is non-deterministic, but there is a 50% chance
    # any candidate a leads to successful factoring.
    # See "Digitalized Signatures and Public Key Functions as Intractable
    # as Factorization", M. Rabin, 1979
    spotted = False
    a = 2
    while not spotted and a < _MAX_RECOVERY_ATTEMPTS:
        k = t
        # Cycle through all values a^{t*2^i}=a^k
        while k < ktot:
            cand = pow(a, k, n)
            # Check if a^k is a non-trivial root of unity (mod n)
            if cand != 1 and cand != (n - 1) and pow(cand, 2, n) == 1:
                # We have found a number such that (cand-1)(cand+1)=0 (mod n).
                # Either of the terms divides n.
                p = gcd(cand + 1, n)
                spotted = True
                break
            k *= 2
        # This value was not any good... let's try another!
        a += 2
    if not spotted:
        raise ValueError("Unable to compute factors p and q from exponent d.")
    # Found !
    q, r = divmod(n, p)
    assert r == 0
    p, q = sorted((p, q), reverse=True)
    return (p, q)


class RSAPrivateNumbers:
    def __init__(
        self,
        p: int,
        q: int,
        d: int,
        dmp1: int,
        dmq1: int,
        iqmp: int,
        public_numbers: RSAPublicNumbers,
    ):
        if (
            not isinstance(p, int)
            or not isinstance(q, int)
            or not isinstance(d, int)
            or not isinstance(dmp1, int)
            or not isinstance(dmq1, int)
            or not isinstance(iqmp, int)
        ):
            raise TypeError(
                "RSAPrivateNumbers p, q, d, dmp1, dmq1, iqmp arguments must"
                " all be an integers."
            )

        if not isinstance(public_numbers, RSAPublicNumbers):
            raise TypeError(
                "RSAPrivateNumbers public_numbers must be an RSAPublicNumbers"
                " instance."
            )

        self._p = p
        self._q = q
        self._d = d
        self._dmp1 = dmp1
        self._dmq1 = dmq1
        self._iqmp = iqmp
        self._public_numbers = public_numbers

    @property
    def p(self) -> int:
        return self._p

    @property
    def q(self) -> int:
        return self._q

    @property
    def d(self) -> int:
        return self._d

    @property
    def dmp1(self) -> int:
        return self._dmp1

    @property
    def dmq1(self) -> int:
        return self._dmq1

    @property
    def iqmp(self) -> int:
        return self._iqmp

    @property
    def public_numbers(self) -> RSAPublicNumbers:
        return self._public_numbers

    def private_key(
        self,
        backend: typing.Any = None,
        *,
        unsafe_skip_rsa_key_validation: bool = False,
    ) -> RSAPrivateKey:
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        return ossl.load_rsa_private_numbers(self, unsafe_skip_rsa_key_validation)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RSAPrivateNumbers):
            return NotImplemented

        return (
            self.p == other.p
            and self.q == other.q
            and self.d == other.d
            and self.dmp1 == other.dmp1
            and self.dmq1 == other.dmq1
            and self.iqmp == other.iqmp
            and self.public_numbers == other.public_numbers
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.p,
                self.q,
                self.d,
                self.dmp1,
                self.dmq1,
                self.iqmp,
                self.public_numbers,
            )
        )


class RSAPublicNumbers:
    def __init__(self, e: int, n: int):
        if not isinstance(e, int) or not isinstance(n, int):
            raise TypeError("RSAPublicNumbers arguments must be integers.")

        self._e = e
        self._n = n

    @property
    def e(self) -> int:
        return self._e

    @property
    def n(self) -> int:
        return self._n

    def public_key(self, backend: typing.Any = None) -> RSAPublicKey:
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        return ossl.load_rsa_public_numbers(self)

    def __repr__(self) -> str:
        return "<RSAPublicNumbers(e={0.e}, n={0.n})>".format(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RSAPublicNumbers):
            return NotImplemented

        return self.e == other.e and self.n == other.n

    def __hash__(self) -> int:
        return hash((self.e, self.n))
