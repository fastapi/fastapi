# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives._serialization import PBES as PBES
from cryptography.hazmat.primitives.asymmetric import (
    dsa,
    ec,
    ed448,
    ed25519,
    rsa,
)
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes

__all__ = [
    "PBES",
    "PKCS12PrivateKeyTypes",
    "PKCS12Certificate",
    "PKCS12KeyAndCertificates",
    "load_key_and_certificates",
    "load_pkcs12",
    "serialize_key_and_certificates",
]

PKCS12PrivateKeyTypes = typing.Union[
    rsa.RSAPrivateKey,
    dsa.DSAPrivateKey,
    ec.EllipticCurvePrivateKey,
    ed25519.Ed25519PrivateKey,
    ed448.Ed448PrivateKey,
]


class PKCS12Certificate:
    def __init__(
        self,
        cert: x509.Certificate,
        friendly_name: typing.Optional[bytes],
    ):
        if not isinstance(cert, x509.Certificate):
            raise TypeError("Expecting x509.Certificate object")
        if friendly_name is not None and not isinstance(friendly_name, bytes):
            raise TypeError("friendly_name must be bytes or None")
        self._cert = cert
        self._friendly_name = friendly_name

    @property
    def friendly_name(self) -> typing.Optional[bytes]:
        return self._friendly_name

    @property
    def certificate(self) -> x509.Certificate:
        return self._cert

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PKCS12Certificate):
            return NotImplemented

        return (
            self.certificate == other.certificate
            and self.friendly_name == other.friendly_name
        )

    def __hash__(self) -> int:
        return hash((self.certificate, self.friendly_name))

    def __repr__(self) -> str:
        return "<PKCS12Certificate({}, friendly_name={!r})>".format(
            self.certificate, self.friendly_name
        )


class PKCS12KeyAndCertificates:
    def __init__(
        self,
        key: typing.Optional[PrivateKeyTypes],
        cert: typing.Optional[PKCS12Certificate],
        additional_certs: typing.List[PKCS12Certificate],
    ):
        if key is not None and not isinstance(
            key,
            (
                rsa.RSAPrivateKey,
                dsa.DSAPrivateKey,
                ec.EllipticCurvePrivateKey,
                ed25519.Ed25519PrivateKey,
                ed448.Ed448PrivateKey,
            ),
        ):
            raise TypeError(
                "Key must be RSA, DSA, EllipticCurve, ED25519, or ED448"
                " private key, or None."
            )
        if cert is not None and not isinstance(cert, PKCS12Certificate):
            raise TypeError("cert must be a PKCS12Certificate object or None")
        if not all(
            isinstance(add_cert, PKCS12Certificate) for add_cert in additional_certs
        ):
            raise TypeError(
                "all values in additional_certs must be PKCS12Certificate" " objects"
            )
        self._key = key
        self._cert = cert
        self._additional_certs = additional_certs

    @property
    def key(self) -> typing.Optional[PrivateKeyTypes]:
        return self._key

    @property
    def cert(self) -> typing.Optional[PKCS12Certificate]:
        return self._cert

    @property
    def additional_certs(self) -> typing.List[PKCS12Certificate]:
        return self._additional_certs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PKCS12KeyAndCertificates):
            return NotImplemented

        return (
            self.key == other.key
            and self.cert == other.cert
            and self.additional_certs == other.additional_certs
        )

    def __hash__(self) -> int:
        return hash((self.key, self.cert, tuple(self.additional_certs)))

    def __repr__(self) -> str:
        fmt = "<PKCS12KeyAndCertificates(key={}, cert={}, additional_certs={})>"
        return fmt.format(self.key, self.cert, self.additional_certs)


def load_key_and_certificates(
    data: bytes,
    password: typing.Optional[bytes],
    backend: typing.Any = None,
) -> typing.Tuple[
    typing.Optional[PrivateKeyTypes],
    typing.Optional[x509.Certificate],
    typing.List[x509.Certificate],
]:
    from cryptography.hazmat.backends.openssl.backend import backend as ossl

    return ossl.load_key_and_certificates_from_pkcs12(data, password)


def load_pkcs12(
    data: bytes,
    password: typing.Optional[bytes],
    backend: typing.Any = None,
) -> PKCS12KeyAndCertificates:
    from cryptography.hazmat.backends.openssl.backend import backend as ossl

    return ossl.load_pkcs12(data, password)


_PKCS12CATypes = typing.Union[
    x509.Certificate,
    PKCS12Certificate,
]


def serialize_key_and_certificates(
    name: typing.Optional[bytes],
    key: typing.Optional[PKCS12PrivateKeyTypes],
    cert: typing.Optional[x509.Certificate],
    cas: typing.Optional[typing.Iterable[_PKCS12CATypes]],
    encryption_algorithm: serialization.KeySerializationEncryption,
) -> bytes:
    if key is not None and not isinstance(
        key,
        (
            rsa.RSAPrivateKey,
            dsa.DSAPrivateKey,
            ec.EllipticCurvePrivateKey,
            ed25519.Ed25519PrivateKey,
            ed448.Ed448PrivateKey,
        ),
    ):
        raise TypeError(
            "Key must be RSA, DSA, EllipticCurve, ED25519, or ED448"
            " private key, or None."
        )
    if cert is not None and not isinstance(cert, x509.Certificate):
        raise TypeError("cert must be a certificate or None")

    if cas is not None:
        cas = list(cas)
        if not all(
            isinstance(
                val,
                (
                    x509.Certificate,
                    PKCS12Certificate,
                ),
            )
            for val in cas
        ):
            raise TypeError("all values in cas must be certificates")

    if not isinstance(encryption_algorithm, serialization.KeySerializationEncryption):
        raise TypeError(
            "Key encryption algorithm must be a " "KeySerializationEncryption instance"
        )

    if key is None and cert is None and not cas:
        raise ValueError("You must supply at least one of key, cert, or cas")

    from cryptography.hazmat.backends.openssl.backend import backend

    return backend.serialize_key_and_certificates_to_pkcs12(
        name, key, cert, cas, encryption_algorithm
    )
