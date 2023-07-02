# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import datetime

from cryptography import utils
from cryptography.hazmat.bindings._rust import x509 as rust_x509
from cryptography.hazmat.primitives.hashes import HashAlgorithm


class LogEntryType(utils.Enum):
    X509_CERTIFICATE = 0
    PRE_CERTIFICATE = 1


class Version(utils.Enum):
    v1 = 0


class SignatureAlgorithm(utils.Enum):
    """
    Signature algorithms that are valid for SCTs.

    These are exactly the same as SignatureAlgorithm in RFC 5246 (TLS 1.2).

    See: <https://datatracker.ietf.org/doc/html/rfc5246#section-7.4.1.4.1>
    """

    ANONYMOUS = 0
    RSA = 1
    DSA = 2
    ECDSA = 3


class SignedCertificateTimestamp(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def version(self) -> Version:
        """
        Returns the SCT version.
        """

    @property
    @abc.abstractmethod
    def log_id(self) -> bytes:
        """
        Returns an identifier indicating which log this SCT is for.
        """

    @property
    @abc.abstractmethod
    def timestamp(self) -> datetime.datetime:
        """
        Returns the timestamp for this SCT.
        """

    @property
    @abc.abstractmethod
    def entry_type(self) -> LogEntryType:
        """
        Returns whether this is an SCT for a certificate or pre-certificate.
        """

    @property
    @abc.abstractmethod
    def signature_hash_algorithm(self) -> HashAlgorithm:
        """
        Returns the hash algorithm used for the SCT's signature.
        """

    @property
    @abc.abstractmethod
    def signature_algorithm(self) -> SignatureAlgorithm:
        """
        Returns the signing algorithm used for the SCT's signature.
        """

    @property
    @abc.abstractmethod
    def signature(self) -> bytes:
        """
        Returns the signature for this SCT.
        """

    @property
    @abc.abstractmethod
    def extension_bytes(self) -> bytes:
        """
        Returns the raw bytes of any extensions for this SCT.
        """


SignedCertificateTimestamp.register(rust_x509.Sct)
