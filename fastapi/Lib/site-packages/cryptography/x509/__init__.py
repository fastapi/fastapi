# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

from cryptography.x509 import certificate_transparency
from cryptography.x509.base import (
    Attribute,
    AttributeNotFound,
    Attributes,
    Certificate,
    CertificateBuilder,
    CertificateRevocationList,
    CertificateRevocationListBuilder,
    CertificateSigningRequest,
    CertificateSigningRequestBuilder,
    InvalidVersion,
    RevokedCertificate,
    RevokedCertificateBuilder,
    Version,
    load_der_x509_certificate,
    load_der_x509_crl,
    load_der_x509_csr,
    load_pem_x509_certificate,
    load_pem_x509_certificates,
    load_pem_x509_crl,
    load_pem_x509_csr,
    random_serial_number,
)
from cryptography.x509.extensions import (
    AccessDescription,
    AuthorityInformationAccess,
    AuthorityKeyIdentifier,
    BasicConstraints,
    CertificateIssuer,
    CertificatePolicies,
    CRLDistributionPoints,
    CRLNumber,
    CRLReason,
    DeltaCRLIndicator,
    DistributionPoint,
    DuplicateExtension,
    ExtendedKeyUsage,
    Extension,
    ExtensionNotFound,
    Extensions,
    ExtensionType,
    FreshestCRL,
    GeneralNames,
    InhibitAnyPolicy,
    InvalidityDate,
    IssuerAlternativeName,
    IssuingDistributionPoint,
    KeyUsage,
    MSCertificateTemplate,
    NameConstraints,
    NoticeReference,
    OCSPAcceptableResponses,
    OCSPNoCheck,
    OCSPNonce,
    PolicyConstraints,
    PolicyInformation,
    PrecertificateSignedCertificateTimestamps,
    PrecertPoison,
    ReasonFlags,
    SignedCertificateTimestamps,
    SubjectAlternativeName,
    SubjectInformationAccess,
    SubjectKeyIdentifier,
    TLSFeature,
    TLSFeatureType,
    UnrecognizedExtension,
    UserNotice,
)
from cryptography.x509.general_name import (
    DirectoryName,
    DNSName,
    GeneralName,
    IPAddress,
    OtherName,
    RegisteredID,
    RFC822Name,
    UniformResourceIdentifier,
    UnsupportedGeneralNameType,
)
from cryptography.x509.name import (
    Name,
    NameAttribute,
    RelativeDistinguishedName,
)
from cryptography.x509.oid import (
    AuthorityInformationAccessOID,
    CertificatePoliciesOID,
    CRLEntryExtensionOID,
    ExtendedKeyUsageOID,
    ExtensionOID,
    NameOID,
    ObjectIdentifier,
    SignatureAlgorithmOID,
)

OID_AUTHORITY_INFORMATION_ACCESS = ExtensionOID.AUTHORITY_INFORMATION_ACCESS
OID_AUTHORITY_KEY_IDENTIFIER = ExtensionOID.AUTHORITY_KEY_IDENTIFIER
OID_BASIC_CONSTRAINTS = ExtensionOID.BASIC_CONSTRAINTS
OID_CERTIFICATE_POLICIES = ExtensionOID.CERTIFICATE_POLICIES
OID_CRL_DISTRIBUTION_POINTS = ExtensionOID.CRL_DISTRIBUTION_POINTS
OID_EXTENDED_KEY_USAGE = ExtensionOID.EXTENDED_KEY_USAGE
OID_FRESHEST_CRL = ExtensionOID.FRESHEST_CRL
OID_INHIBIT_ANY_POLICY = ExtensionOID.INHIBIT_ANY_POLICY
OID_ISSUER_ALTERNATIVE_NAME = ExtensionOID.ISSUER_ALTERNATIVE_NAME
OID_KEY_USAGE = ExtensionOID.KEY_USAGE
OID_NAME_CONSTRAINTS = ExtensionOID.NAME_CONSTRAINTS
OID_OCSP_NO_CHECK = ExtensionOID.OCSP_NO_CHECK
OID_POLICY_CONSTRAINTS = ExtensionOID.POLICY_CONSTRAINTS
OID_POLICY_MAPPINGS = ExtensionOID.POLICY_MAPPINGS
OID_SUBJECT_ALTERNATIVE_NAME = ExtensionOID.SUBJECT_ALTERNATIVE_NAME
OID_SUBJECT_DIRECTORY_ATTRIBUTES = ExtensionOID.SUBJECT_DIRECTORY_ATTRIBUTES
OID_SUBJECT_INFORMATION_ACCESS = ExtensionOID.SUBJECT_INFORMATION_ACCESS
OID_SUBJECT_KEY_IDENTIFIER = ExtensionOID.SUBJECT_KEY_IDENTIFIER

OID_DSA_WITH_SHA1 = SignatureAlgorithmOID.DSA_WITH_SHA1
OID_DSA_WITH_SHA224 = SignatureAlgorithmOID.DSA_WITH_SHA224
OID_DSA_WITH_SHA256 = SignatureAlgorithmOID.DSA_WITH_SHA256
OID_ECDSA_WITH_SHA1 = SignatureAlgorithmOID.ECDSA_WITH_SHA1
OID_ECDSA_WITH_SHA224 = SignatureAlgorithmOID.ECDSA_WITH_SHA224
OID_ECDSA_WITH_SHA256 = SignatureAlgorithmOID.ECDSA_WITH_SHA256
OID_ECDSA_WITH_SHA384 = SignatureAlgorithmOID.ECDSA_WITH_SHA384
OID_ECDSA_WITH_SHA512 = SignatureAlgorithmOID.ECDSA_WITH_SHA512
OID_RSA_WITH_MD5 = SignatureAlgorithmOID.RSA_WITH_MD5
OID_RSA_WITH_SHA1 = SignatureAlgorithmOID.RSA_WITH_SHA1
OID_RSA_WITH_SHA224 = SignatureAlgorithmOID.RSA_WITH_SHA224
OID_RSA_WITH_SHA256 = SignatureAlgorithmOID.RSA_WITH_SHA256
OID_RSA_WITH_SHA384 = SignatureAlgorithmOID.RSA_WITH_SHA384
OID_RSA_WITH_SHA512 = SignatureAlgorithmOID.RSA_WITH_SHA512
OID_RSASSA_PSS = SignatureAlgorithmOID.RSASSA_PSS

OID_COMMON_NAME = NameOID.COMMON_NAME
OID_COUNTRY_NAME = NameOID.COUNTRY_NAME
OID_DOMAIN_COMPONENT = NameOID.DOMAIN_COMPONENT
OID_DN_QUALIFIER = NameOID.DN_QUALIFIER
OID_EMAIL_ADDRESS = NameOID.EMAIL_ADDRESS
OID_GENERATION_QUALIFIER = NameOID.GENERATION_QUALIFIER
OID_GIVEN_NAME = NameOID.GIVEN_NAME
OID_LOCALITY_NAME = NameOID.LOCALITY_NAME
OID_ORGANIZATIONAL_UNIT_NAME = NameOID.ORGANIZATIONAL_UNIT_NAME
OID_ORGANIZATION_NAME = NameOID.ORGANIZATION_NAME
OID_PSEUDONYM = NameOID.PSEUDONYM
OID_SERIAL_NUMBER = NameOID.SERIAL_NUMBER
OID_STATE_OR_PROVINCE_NAME = NameOID.STATE_OR_PROVINCE_NAME
OID_SURNAME = NameOID.SURNAME
OID_TITLE = NameOID.TITLE

OID_CLIENT_AUTH = ExtendedKeyUsageOID.CLIENT_AUTH
OID_CODE_SIGNING = ExtendedKeyUsageOID.CODE_SIGNING
OID_EMAIL_PROTECTION = ExtendedKeyUsageOID.EMAIL_PROTECTION
OID_OCSP_SIGNING = ExtendedKeyUsageOID.OCSP_SIGNING
OID_SERVER_AUTH = ExtendedKeyUsageOID.SERVER_AUTH
OID_TIME_STAMPING = ExtendedKeyUsageOID.TIME_STAMPING

OID_ANY_POLICY = CertificatePoliciesOID.ANY_POLICY
OID_CPS_QUALIFIER = CertificatePoliciesOID.CPS_QUALIFIER
OID_CPS_USER_NOTICE = CertificatePoliciesOID.CPS_USER_NOTICE

OID_CERTIFICATE_ISSUER = CRLEntryExtensionOID.CERTIFICATE_ISSUER
OID_CRL_REASON = CRLEntryExtensionOID.CRL_REASON
OID_INVALIDITY_DATE = CRLEntryExtensionOID.INVALIDITY_DATE

OID_CA_ISSUERS = AuthorityInformationAccessOID.CA_ISSUERS
OID_OCSP = AuthorityInformationAccessOID.OCSP

__all__ = [
    "certificate_transparency",
    "load_pem_x509_certificate",
    "load_pem_x509_certificates",
    "load_der_x509_certificate",
    "load_pem_x509_csr",
    "load_der_x509_csr",
    "load_pem_x509_crl",
    "load_der_x509_crl",
    "random_serial_number",
    "Attribute",
    "AttributeNotFound",
    "Attributes",
    "InvalidVersion",
    "DeltaCRLIndicator",
    "DuplicateExtension",
    "ExtensionNotFound",
    "UnsupportedGeneralNameType",
    "NameAttribute",
    "Name",
    "RelativeDistinguishedName",
    "ObjectIdentifier",
    "ExtensionType",
    "Extensions",
    "Extension",
    "ExtendedKeyUsage",
    "FreshestCRL",
    "IssuingDistributionPoint",
    "TLSFeature",
    "TLSFeatureType",
    "OCSPAcceptableResponses",
    "OCSPNoCheck",
    "BasicConstraints",
    "CRLNumber",
    "KeyUsage",
    "AuthorityInformationAccess",
    "SubjectInformationAccess",
    "AccessDescription",
    "CertificatePolicies",
    "PolicyInformation",
    "UserNotice",
    "NoticeReference",
    "SubjectKeyIdentifier",
    "NameConstraints",
    "CRLDistributionPoints",
    "DistributionPoint",
    "ReasonFlags",
    "InhibitAnyPolicy",
    "SubjectAlternativeName",
    "IssuerAlternativeName",
    "AuthorityKeyIdentifier",
    "GeneralNames",
    "GeneralName",
    "RFC822Name",
    "DNSName",
    "UniformResourceIdentifier",
    "RegisteredID",
    "DirectoryName",
    "IPAddress",
    "OtherName",
    "Certificate",
    "CertificateRevocationList",
    "CertificateRevocationListBuilder",
    "CertificateSigningRequest",
    "RevokedCertificate",
    "RevokedCertificateBuilder",
    "CertificateSigningRequestBuilder",
    "CertificateBuilder",
    "Version",
    "OID_CA_ISSUERS",
    "OID_OCSP",
    "CertificateIssuer",
    "CRLReason",
    "InvalidityDate",
    "UnrecognizedExtension",
    "PolicyConstraints",
    "PrecertificateSignedCertificateTimestamps",
    "PrecertPoison",
    "OCSPNonce",
    "SignedCertificateTimestamps",
    "SignatureAlgorithmOID",
    "NameOID",
    "MSCertificateTemplate",
]
