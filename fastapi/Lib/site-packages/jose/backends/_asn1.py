"""ASN1 encoding helpers for converting between PKCS1 and PKCS8.

Required by rsa_backend but not cryptography_backend.
"""
from pyasn1.codec.der import decoder, encoder
from pyasn1.type import namedtype, univ

RSA_ENCRYPTION_ASN1_OID = "1.2.840.113549.1.1.1"


class RsaAlgorithmIdentifier(univ.Sequence):
    """ASN1 structure for recording RSA PrivateKeyAlgorithm identifiers."""

    componentType = namedtype.NamedTypes(
        namedtype.NamedType("rsaEncryption", univ.ObjectIdentifier()),
        namedtype.NamedType("parameters", univ.Null()),
    )


class PKCS8PrivateKey(univ.Sequence):
    """ASN1 structure for recording PKCS8 private keys."""

    componentType = namedtype.NamedTypes(
        namedtype.NamedType("version", univ.Integer()),
        namedtype.NamedType("privateKeyAlgorithm", RsaAlgorithmIdentifier()),
        namedtype.NamedType("privateKey", univ.OctetString()),
    )


class PublicKeyInfo(univ.Sequence):
    """ASN1 structure for recording PKCS8 public keys."""

    componentType = namedtype.NamedTypes(
        namedtype.NamedType("algorithm", RsaAlgorithmIdentifier()),
        namedtype.NamedType("publicKey", univ.BitString()),
    )


def rsa_private_key_pkcs8_to_pkcs1(pkcs8_key):
    """Convert a PKCS8-encoded RSA private key to PKCS1."""
    decoded_values = decoder.decode(pkcs8_key, asn1Spec=PKCS8PrivateKey())

    try:
        decoded_key = decoded_values[0]
    except IndexError:
        raise ValueError("Invalid private key encoding")

    return decoded_key["privateKey"]


def rsa_private_key_pkcs1_to_pkcs8(pkcs1_key):
    """Convert a PKCS1-encoded RSA private key to PKCS8."""
    algorithm = RsaAlgorithmIdentifier()
    algorithm["rsaEncryption"] = RSA_ENCRYPTION_ASN1_OID

    pkcs8_key = PKCS8PrivateKey()
    pkcs8_key["version"] = 0
    pkcs8_key["privateKeyAlgorithm"] = algorithm
    pkcs8_key["privateKey"] = pkcs1_key

    return encoder.encode(pkcs8_key)


def rsa_public_key_pkcs1_to_pkcs8(pkcs1_key):
    """Convert a PKCS1-encoded RSA private key to PKCS8."""
    algorithm = RsaAlgorithmIdentifier()
    algorithm["rsaEncryption"] = RSA_ENCRYPTION_ASN1_OID

    pkcs8_key = PublicKeyInfo()
    pkcs8_key["algorithm"] = algorithm
    pkcs8_key["publicKey"] = univ.BitString.fromOctetString(pkcs1_key)

    return encoder.encode(pkcs8_key)


def rsa_public_key_pkcs8_to_pkcs1(pkcs8_key):
    """Convert a PKCS8-encoded RSA private key to PKCS1."""
    decoded_values = decoder.decode(pkcs8_key, asn1Spec=PublicKeyInfo())

    try:
        decoded_key = decoded_values[0]
    except IndexError:
        raise ValueError("Invalid public key encoding.")

    return decoded_key["publicKey"].asOctets()
