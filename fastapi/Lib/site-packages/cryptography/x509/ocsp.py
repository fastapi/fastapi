# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import datetime
import typing

from cryptography import utils, x509
from cryptography.hazmat.bindings._rust import ocsp
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    CertificateIssuerPrivateKeyTypes,
)
from cryptography.x509.base import (
    _EARLIEST_UTC_TIME,
    _convert_to_naive_utc_time,
    _reject_duplicate_extension,
)


class OCSPResponderEncoding(utils.Enum):
    HASH = "By Hash"
    NAME = "By Name"


class OCSPResponseStatus(utils.Enum):
    SUCCESSFUL = 0
    MALFORMED_REQUEST = 1
    INTERNAL_ERROR = 2
    TRY_LATER = 3
    SIG_REQUIRED = 5
    UNAUTHORIZED = 6


_ALLOWED_HASHES = (
    hashes.SHA1,
    hashes.SHA224,
    hashes.SHA256,
    hashes.SHA384,
    hashes.SHA512,
)


def _verify_algorithm(algorithm: hashes.HashAlgorithm) -> None:
    if not isinstance(algorithm, _ALLOWED_HASHES):
        raise ValueError("Algorithm must be SHA1, SHA224, SHA256, SHA384, or SHA512")


class OCSPCertStatus(utils.Enum):
    GOOD = 0
    REVOKED = 1
    UNKNOWN = 2


class _SingleResponse:
    def __init__(
        self,
        cert: x509.Certificate,
        issuer: x509.Certificate,
        algorithm: hashes.HashAlgorithm,
        cert_status: OCSPCertStatus,
        this_update: datetime.datetime,
        next_update: typing.Optional[datetime.datetime],
        revocation_time: typing.Optional[datetime.datetime],
        revocation_reason: typing.Optional[x509.ReasonFlags],
    ):
        if not isinstance(cert, x509.Certificate) or not isinstance(
            issuer, x509.Certificate
        ):
            raise TypeError("cert and issuer must be a Certificate")

        _verify_algorithm(algorithm)
        if not isinstance(this_update, datetime.datetime):
            raise TypeError("this_update must be a datetime object")
        if next_update is not None and not isinstance(next_update, datetime.datetime):
            raise TypeError("next_update must be a datetime object or None")

        self._cert = cert
        self._issuer = issuer
        self._algorithm = algorithm
        self._this_update = this_update
        self._next_update = next_update

        if not isinstance(cert_status, OCSPCertStatus):
            raise TypeError("cert_status must be an item from the OCSPCertStatus enum")
        if cert_status is not OCSPCertStatus.REVOKED:
            if revocation_time is not None:
                raise ValueError(
                    "revocation_time can only be provided if the certificate "
                    "is revoked"
                )
            if revocation_reason is not None:
                raise ValueError(
                    "revocation_reason can only be provided if the certificate"
                    " is revoked"
                )
        else:
            if not isinstance(revocation_time, datetime.datetime):
                raise TypeError("revocation_time must be a datetime object")

            revocation_time = _convert_to_naive_utc_time(revocation_time)
            if revocation_time < _EARLIEST_UTC_TIME:
                raise ValueError(
                    "The revocation_time must be on or after" " 1950 January 1."
                )

            if revocation_reason is not None and not isinstance(
                revocation_reason, x509.ReasonFlags
            ):
                raise TypeError(
                    "revocation_reason must be an item from the ReasonFlags "
                    "enum or None"
                )

        self._cert_status = cert_status
        self._revocation_time = revocation_time
        self._revocation_reason = revocation_reason


class OCSPRequest(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def issuer_key_hash(self) -> bytes:
        """
        The hash of the issuer public key
        """

    @property
    @abc.abstractmethod
    def issuer_name_hash(self) -> bytes:
        """
        The hash of the issuer name
        """

    @property
    @abc.abstractmethod
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        The hash algorithm used in the issuer name and key hashes
        """

    @property
    @abc.abstractmethod
    def serial_number(self) -> int:
        """
        The serial number of the cert whose status is being checked
        """

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the request to DER
        """

    @property
    @abc.abstractmethod
    def extensions(self) -> x509.Extensions:
        """
        The list of request extensions. Not single request extensions.
        """


class OCSPSingleResponse(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def certificate_status(self) -> OCSPCertStatus:
        """
        The status of the certificate (an element from the OCSPCertStatus enum)
        """

    @property
    @abc.abstractmethod
    def revocation_time(self) -> typing.Optional[datetime.datetime]:
        """
        The date of when the certificate was revoked or None if not
        revoked.
        """

    @property
    @abc.abstractmethod
    def revocation_reason(self) -> typing.Optional[x509.ReasonFlags]:
        """
        The reason the certificate was revoked or None if not specified or
        not revoked.
        """

    @property
    @abc.abstractmethod
    def this_update(self) -> datetime.datetime:
        """
        The most recent time at which the status being indicated is known by
        the responder to have been correct
        """

    @property
    @abc.abstractmethod
    def next_update(self) -> typing.Optional[datetime.datetime]:
        """
        The time when newer information will be available
        """

    @property
    @abc.abstractmethod
    def issuer_key_hash(self) -> bytes:
        """
        The hash of the issuer public key
        """

    @property
    @abc.abstractmethod
    def issuer_name_hash(self) -> bytes:
        """
        The hash of the issuer name
        """

    @property
    @abc.abstractmethod
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        The hash algorithm used in the issuer name and key hashes
        """

    @property
    @abc.abstractmethod
    def serial_number(self) -> int:
        """
        The serial number of the cert whose status is being checked
        """


class OCSPResponse(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def responses(self) -> typing.Iterator[OCSPSingleResponse]:
        """
        An iterator over the individual SINGLERESP structures in the
        response
        """

    @property
    @abc.abstractmethod
    def response_status(self) -> OCSPResponseStatus:
        """
        The status of the response. This is a value from the OCSPResponseStatus
        enumeration
        """

    @property
    @abc.abstractmethod
    def signature_algorithm_oid(self) -> x509.ObjectIdentifier:
        """
        The ObjectIdentifier of the signature algorithm
        """

    @property
    @abc.abstractmethod
    def signature_hash_algorithm(
        self,
    ) -> typing.Optional[hashes.HashAlgorithm]:
        """
        Returns a HashAlgorithm corresponding to the type of the digest signed
        """

    @property
    @abc.abstractmethod
    def signature(self) -> bytes:
        """
        The signature bytes
        """

    @property
    @abc.abstractmethod
    def tbs_response_bytes(self) -> bytes:
        """
        The tbsResponseData bytes
        """

    @property
    @abc.abstractmethod
    def certificates(self) -> typing.List[x509.Certificate]:
        """
        A list of certificates used to help build a chain to verify the OCSP
        response. This situation occurs when the OCSP responder uses a delegate
        certificate.
        """

    @property
    @abc.abstractmethod
    def responder_key_hash(self) -> typing.Optional[bytes]:
        """
        The responder's key hash or None
        """

    @property
    @abc.abstractmethod
    def responder_name(self) -> typing.Optional[x509.Name]:
        """
        The responder's Name or None
        """

    @property
    @abc.abstractmethod
    def produced_at(self) -> datetime.datetime:
        """
        The time the response was produced
        """

    @property
    @abc.abstractmethod
    def certificate_status(self) -> OCSPCertStatus:
        """
        The status of the certificate (an element from the OCSPCertStatus enum)
        """

    @property
    @abc.abstractmethod
    def revocation_time(self) -> typing.Optional[datetime.datetime]:
        """
        The date of when the certificate was revoked or None if not
        revoked.
        """

    @property
    @abc.abstractmethod
    def revocation_reason(self) -> typing.Optional[x509.ReasonFlags]:
        """
        The reason the certificate was revoked or None if not specified or
        not revoked.
        """

    @property
    @abc.abstractmethod
    def this_update(self) -> datetime.datetime:
        """
        The most recent time at which the status being indicated is known by
        the responder to have been correct
        """

    @property
    @abc.abstractmethod
    def next_update(self) -> typing.Optional[datetime.datetime]:
        """
        The time when newer information will be available
        """

    @property
    @abc.abstractmethod
    def issuer_key_hash(self) -> bytes:
        """
        The hash of the issuer public key
        """

    @property
    @abc.abstractmethod
    def issuer_name_hash(self) -> bytes:
        """
        The hash of the issuer name
        """

    @property
    @abc.abstractmethod
    def hash_algorithm(self) -> hashes.HashAlgorithm:
        """
        The hash algorithm used in the issuer name and key hashes
        """

    @property
    @abc.abstractmethod
    def serial_number(self) -> int:
        """
        The serial number of the cert whose status is being checked
        """

    @property
    @abc.abstractmethod
    def extensions(self) -> x509.Extensions:
        """
        The list of response extensions. Not single response extensions.
        """

    @property
    @abc.abstractmethod
    def single_extensions(self) -> x509.Extensions:
        """
        The list of single response extensions. Not response extensions.
        """

    @abc.abstractmethod
    def public_bytes(self, encoding: serialization.Encoding) -> bytes:
        """
        Serializes the response to DER
        """


class OCSPRequestBuilder:
    def __init__(
        self,
        request: typing.Optional[
            typing.Tuple[x509.Certificate, x509.Certificate, hashes.HashAlgorithm]
        ] = None,
        request_hash: typing.Optional[
            typing.Tuple[bytes, bytes, int, hashes.HashAlgorithm]
        ] = None,
        extensions: typing.List[x509.Extension[x509.ExtensionType]] = [],
    ) -> None:
        self._request = request
        self._request_hash = request_hash
        self._extensions = extensions

    def add_certificate(
        self,
        cert: x509.Certificate,
        issuer: x509.Certificate,
        algorithm: hashes.HashAlgorithm,
    ) -> OCSPRequestBuilder:
        if self._request is not None or self._request_hash is not None:
            raise ValueError("Only one certificate can be added to a request")

        _verify_algorithm(algorithm)
        if not isinstance(cert, x509.Certificate) or not isinstance(
            issuer, x509.Certificate
        ):
            raise TypeError("cert and issuer must be a Certificate")

        return OCSPRequestBuilder(
            (cert, issuer, algorithm), self._request_hash, self._extensions
        )

    def add_certificate_by_hash(
        self,
        issuer_name_hash: bytes,
        issuer_key_hash: bytes,
        serial_number: int,
        algorithm: hashes.HashAlgorithm,
    ) -> OCSPRequestBuilder:
        if self._request is not None or self._request_hash is not None:
            raise ValueError("Only one certificate can be added to a request")

        if not isinstance(serial_number, int):
            raise TypeError("serial_number must be an integer")

        _verify_algorithm(algorithm)
        utils._check_bytes("issuer_name_hash", issuer_name_hash)
        utils._check_bytes("issuer_key_hash", issuer_key_hash)
        if algorithm.digest_size != len(
            issuer_name_hash
        ) or algorithm.digest_size != len(issuer_key_hash):
            raise ValueError(
                "issuer_name_hash and issuer_key_hash must be the same length "
                "as the digest size of the algorithm"
            )

        return OCSPRequestBuilder(
            self._request,
            (issuer_name_hash, issuer_key_hash, serial_number, algorithm),
            self._extensions,
        )

    def add_extension(
        self, extval: x509.ExtensionType, critical: bool
    ) -> OCSPRequestBuilder:
        if not isinstance(extval, x509.ExtensionType):
            raise TypeError("extension must be an ExtensionType")

        extension = x509.Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)

        return OCSPRequestBuilder(
            self._request, self._request_hash, self._extensions + [extension]
        )

    def build(self) -> OCSPRequest:
        if self._request is None and self._request_hash is None:
            raise ValueError("You must add a certificate before building")

        return ocsp.create_ocsp_request(self)


class OCSPResponseBuilder:
    def __init__(
        self,
        response: typing.Optional[_SingleResponse] = None,
        responder_id: typing.Optional[
            typing.Tuple[x509.Certificate, OCSPResponderEncoding]
        ] = None,
        certs: typing.Optional[typing.List[x509.Certificate]] = None,
        extensions: typing.List[x509.Extension[x509.ExtensionType]] = [],
    ):
        self._response = response
        self._responder_id = responder_id
        self._certs = certs
        self._extensions = extensions

    def add_response(
        self,
        cert: x509.Certificate,
        issuer: x509.Certificate,
        algorithm: hashes.HashAlgorithm,
        cert_status: OCSPCertStatus,
        this_update: datetime.datetime,
        next_update: typing.Optional[datetime.datetime],
        revocation_time: typing.Optional[datetime.datetime],
        revocation_reason: typing.Optional[x509.ReasonFlags],
    ) -> OCSPResponseBuilder:
        if self._response is not None:
            raise ValueError("Only one response per OCSPResponse.")

        singleresp = _SingleResponse(
            cert,
            issuer,
            algorithm,
            cert_status,
            this_update,
            next_update,
            revocation_time,
            revocation_reason,
        )
        return OCSPResponseBuilder(
            singleresp,
            self._responder_id,
            self._certs,
            self._extensions,
        )

    def responder_id(
        self, encoding: OCSPResponderEncoding, responder_cert: x509.Certificate
    ) -> OCSPResponseBuilder:
        if self._responder_id is not None:
            raise ValueError("responder_id can only be set once")
        if not isinstance(responder_cert, x509.Certificate):
            raise TypeError("responder_cert must be a Certificate")
        if not isinstance(encoding, OCSPResponderEncoding):
            raise TypeError("encoding must be an element from OCSPResponderEncoding")

        return OCSPResponseBuilder(
            self._response,
            (responder_cert, encoding),
            self._certs,
            self._extensions,
        )

    def certificates(
        self, certs: typing.Iterable[x509.Certificate]
    ) -> OCSPResponseBuilder:
        if self._certs is not None:
            raise ValueError("certificates may only be set once")
        certs = list(certs)
        if len(certs) == 0:
            raise ValueError("certs must not be an empty list")
        if not all(isinstance(x, x509.Certificate) for x in certs):
            raise TypeError("certs must be a list of Certificates")
        return OCSPResponseBuilder(
            self._response,
            self._responder_id,
            certs,
            self._extensions,
        )

    def add_extension(
        self, extval: x509.ExtensionType, critical: bool
    ) -> OCSPResponseBuilder:
        if not isinstance(extval, x509.ExtensionType):
            raise TypeError("extension must be an ExtensionType")

        extension = x509.Extension(extval.oid, critical, extval)
        _reject_duplicate_extension(extension, self._extensions)

        return OCSPResponseBuilder(
            self._response,
            self._responder_id,
            self._certs,
            self._extensions + [extension],
        )

    def sign(
        self,
        private_key: CertificateIssuerPrivateKeyTypes,
        algorithm: typing.Optional[hashes.HashAlgorithm],
    ) -> OCSPResponse:
        if self._response is None:
            raise ValueError("You must add a response before signing")
        if self._responder_id is None:
            raise ValueError("You must add a responder_id before signing")

        return ocsp.create_ocsp_response(
            OCSPResponseStatus.SUCCESSFUL, self, private_key, algorithm
        )

    @classmethod
    def build_unsuccessful(cls, response_status: OCSPResponseStatus) -> OCSPResponse:
        if not isinstance(response_status, OCSPResponseStatus):
            raise TypeError("response_status must be an item from OCSPResponseStatus")
        if response_status is OCSPResponseStatus.SUCCESSFUL:
            raise ValueError("response_status cannot be SUCCESSFUL")

        return ocsp.create_ocsp_response(response_status, None, None, None)


def load_der_ocsp_request(data: bytes) -> OCSPRequest:
    return ocsp.load_der_ocsp_request(data)


def load_der_ocsp_response(data: bytes) -> OCSPResponse:
    return ocsp.load_der_ocsp_response(data)
