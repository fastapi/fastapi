# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing

from cryptography import utils
from cryptography.hazmat.primitives.asymmetric import (
    dh,
    dsa,
    ec,
    ed448,
    ed25519,
    rsa,
    x448,
    x25519,
)

# Every asymmetric key type
PublicKeyTypes = typing.Union[
    dh.DHPublicKey,
    dsa.DSAPublicKey,
    rsa.RSAPublicKey,
    ec.EllipticCurvePublicKey,
    ed25519.Ed25519PublicKey,
    ed448.Ed448PublicKey,
    x25519.X25519PublicKey,
    x448.X448PublicKey,
]
PUBLIC_KEY_TYPES = PublicKeyTypes
utils.deprecated(
    PUBLIC_KEY_TYPES,
    __name__,
    "Use PublicKeyTypes instead",
    utils.DeprecatedIn40,
    name="PUBLIC_KEY_TYPES",
)
# Every asymmetric key type
PrivateKeyTypes = typing.Union[
    dh.DHPrivateKey,
    ed25519.Ed25519PrivateKey,
    ed448.Ed448PrivateKey,
    rsa.RSAPrivateKey,
    dsa.DSAPrivateKey,
    ec.EllipticCurvePrivateKey,
    x25519.X25519PrivateKey,
    x448.X448PrivateKey,
]
PRIVATE_KEY_TYPES = PrivateKeyTypes
utils.deprecated(
    PRIVATE_KEY_TYPES,
    __name__,
    "Use PrivateKeyTypes instead",
    utils.DeprecatedIn40,
    name="PRIVATE_KEY_TYPES",
)
# Just the key types we allow to be used for x509 signing. This mirrors
# the certificate public key types
CertificateIssuerPrivateKeyTypes = typing.Union[
    ed25519.Ed25519PrivateKey,
    ed448.Ed448PrivateKey,
    rsa.RSAPrivateKey,
    dsa.DSAPrivateKey,
    ec.EllipticCurvePrivateKey,
]
CERTIFICATE_PRIVATE_KEY_TYPES = CertificateIssuerPrivateKeyTypes
utils.deprecated(
    CERTIFICATE_PRIVATE_KEY_TYPES,
    __name__,
    "Use CertificateIssuerPrivateKeyTypes instead",
    utils.DeprecatedIn40,
    name="CERTIFICATE_PRIVATE_KEY_TYPES",
)
# Just the key types we allow to be used for x509 signing. This mirrors
# the certificate private key types
CertificateIssuerPublicKeyTypes = typing.Union[
    dsa.DSAPublicKey,
    rsa.RSAPublicKey,
    ec.EllipticCurvePublicKey,
    ed25519.Ed25519PublicKey,
    ed448.Ed448PublicKey,
]
CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES = CertificateIssuerPublicKeyTypes
utils.deprecated(
    CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES,
    __name__,
    "Use CertificateIssuerPublicKeyTypes instead",
    utils.DeprecatedIn40,
    name="CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES",
)
# This type removes DHPublicKey. x448/x25519 can be a public key
# but cannot be used in signing so they are allowed here.
CertificatePublicKeyTypes = typing.Union[
    dsa.DSAPublicKey,
    rsa.RSAPublicKey,
    ec.EllipticCurvePublicKey,
    ed25519.Ed25519PublicKey,
    ed448.Ed448PublicKey,
    x25519.X25519PublicKey,
    x448.X448PublicKey,
]
CERTIFICATE_PUBLIC_KEY_TYPES = CertificatePublicKeyTypes
utils.deprecated(
    CERTIFICATE_PUBLIC_KEY_TYPES,
    __name__,
    "Use CertificatePublicKeyTypes instead",
    utils.DeprecatedIn40,
    name="CERTIFICATE_PUBLIC_KEY_TYPES",
)
