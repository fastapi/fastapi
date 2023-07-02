# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import typing

from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.primitives import _serialization


def generate_parameters(
    generator: int, key_size: int, backend: typing.Any = None
) -> DHParameters:
    from cryptography.hazmat.backends.openssl.backend import backend as ossl

    return ossl.generate_dh_parameters(generator, key_size)


class DHParameterNumbers:
    def __init__(self, p: int, g: int, q: typing.Optional[int] = None) -> None:
        if not isinstance(p, int) or not isinstance(g, int):
            raise TypeError("p and g must be integers")
        if q is not None and not isinstance(q, int):
            raise TypeError("q must be integer or None")

        if g < 2:
            raise ValueError("DH generator must be 2 or greater")

        if p.bit_length() < rust_openssl.dh.MIN_MODULUS_SIZE:
            raise ValueError(
                f"p (modulus) must be at least "
                f"{rust_openssl.dh.MIN_MODULUS_SIZE}-bit"
            )

        self._p = p
        self._g = g
        self._q = q

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DHParameterNumbers):
            return NotImplemented

        return self._p == other._p and self._g == other._g and self._q == other._q

    def parameters(self, backend: typing.Any = None) -> DHParameters:
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        return ossl.load_dh_parameter_numbers(self)

    @property
    def p(self) -> int:
        return self._p

    @property
    def g(self) -> int:
        return self._g

    @property
    def q(self) -> typing.Optional[int]:
        return self._q


class DHPublicNumbers:
    def __init__(self, y: int, parameter_numbers: DHParameterNumbers) -> None:
        if not isinstance(y, int):
            raise TypeError("y must be an integer.")

        if not isinstance(parameter_numbers, DHParameterNumbers):
            raise TypeError("parameters must be an instance of DHParameterNumbers.")

        self._y = y
        self._parameter_numbers = parameter_numbers

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DHPublicNumbers):
            return NotImplemented

        return (
            self._y == other._y and self._parameter_numbers == other._parameter_numbers
        )

    def public_key(self, backend: typing.Any = None) -> DHPublicKey:
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        return ossl.load_dh_public_numbers(self)

    @property
    def y(self) -> int:
        return self._y

    @property
    def parameter_numbers(self) -> DHParameterNumbers:
        return self._parameter_numbers


class DHPrivateNumbers:
    def __init__(self, x: int, public_numbers: DHPublicNumbers) -> None:
        if not isinstance(x, int):
            raise TypeError("x must be an integer.")

        if not isinstance(public_numbers, DHPublicNumbers):
            raise TypeError("public_numbers must be an instance of " "DHPublicNumbers.")

        self._x = x
        self._public_numbers = public_numbers

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DHPrivateNumbers):
            return NotImplemented

        return self._x == other._x and self._public_numbers == other._public_numbers

    def private_key(self, backend: typing.Any = None) -> DHPrivateKey:
        from cryptography.hazmat.backends.openssl.backend import (
            backend as ossl,
        )

        return ossl.load_dh_private_numbers(self)

    @property
    def public_numbers(self) -> DHPublicNumbers:
        return self._public_numbers

    @property
    def x(self) -> int:
        return self._x


class DHParameters(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_private_key(self) -> DHPrivateKey:
        """
        Generates and returns a DHPrivateKey.
        """

    @abc.abstractmethod
    def parameter_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.ParameterFormat,
    ) -> bytes:
        """
        Returns the parameters serialized as bytes.
        """

    @abc.abstractmethod
    def parameter_numbers(self) -> DHParameterNumbers:
        """
        Returns a DHParameterNumbers.
        """


DHParametersWithSerialization = DHParameters
DHParameters.register(rust_openssl.dh.DHParameters)


class DHPublicKey(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this public key.
        """

    @abc.abstractmethod
    def public_numbers(self) -> DHPublicNumbers:
        """
        Returns a DHPublicNumbers.
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
    def __eq__(self, other: object) -> bool:
        """
        Checks equality.
        """


DHPublicKeyWithSerialization = DHPublicKey
DHPublicKey.register(rust_openssl.dh.DHPublicKey)


class DHPrivateKey(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def key_size(self) -> int:
        """
        The bit length of the prime modulus.
        """

    @abc.abstractmethod
    def public_key(self) -> DHPublicKey:
        """
        The DHPublicKey associated with this private key.
        """

    @abc.abstractmethod
    def parameters(self) -> DHParameters:
        """
        The DHParameters object associated with this private key.
        """

    @abc.abstractmethod
    def exchange(self, peer_public_key: DHPublicKey) -> bytes:
        """
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """

    @abc.abstractmethod
    def private_numbers(self) -> DHPrivateNumbers:
        """
        Returns a DHPrivateNumbers.
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


DHPrivateKeyWithSerialization = DHPrivateKey
DHPrivateKey.register(rust_openssl.dh.DHPrivateKey)
