# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import abc
import ipaddress
import typing
from email.utils import parseaddr

from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier

_IPAddressTypes = typing.Union[
    ipaddress.IPv4Address,
    ipaddress.IPv6Address,
    ipaddress.IPv4Network,
    ipaddress.IPv6Network,
]


class UnsupportedGeneralNameType(Exception):
    pass


class GeneralName(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def value(self) -> typing.Any:
        """
        Return the value of the object
        """


class RFC822Name(GeneralName):
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            try:
                value.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError(
                    "RFC822Name values should be passed as an A-label string. "
                    "This means unicode characters should be encoded via "
                    "a library like idna."
                )
        else:
            raise TypeError("value must be string")

        name, address = parseaddr(value)
        if name or not address:
            # parseaddr has found a name (e.g. Name <email>) or the entire
            # value is an empty string.
            raise ValueError("Invalid rfc822name value")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def _init_without_validation(cls, value: str) -> RFC822Name:
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self) -> str:
        return f"<RFC822Name(value={self.value!r})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RFC822Name):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class DNSName(GeneralName):
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            try:
                value.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError(
                    "DNSName values should be passed as an A-label string. "
                    "This means unicode characters should be encoded via "
                    "a library like idna."
                )
        else:
            raise TypeError("value must be string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def _init_without_validation(cls, value: str) -> DNSName:
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self) -> str:
        return f"<DNSName(value={self.value!r})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DNSName):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class UniformResourceIdentifier(GeneralName):
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            try:
                value.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError(
                    "URI values should be passed as an A-label string. "
                    "This means unicode characters should be encoded via "
                    "a library like idna."
                )
        else:
            raise TypeError("value must be string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def _init_without_validation(cls, value: str) -> UniformResourceIdentifier:
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self) -> str:
        return f"<UniformResourceIdentifier(value={self.value!r})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UniformResourceIdentifier):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class DirectoryName(GeneralName):
    def __init__(self, value: Name) -> None:
        if not isinstance(value, Name):
            raise TypeError("value must be a Name")

        self._value = value

    @property
    def value(self) -> Name:
        return self._value

    def __repr__(self) -> str:
        return f"<DirectoryName(value={self.value})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectoryName):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class RegisteredID(GeneralName):
    def __init__(self, value: ObjectIdentifier) -> None:
        if not isinstance(value, ObjectIdentifier):
            raise TypeError("value must be an ObjectIdentifier")

        self._value = value

    @property
    def value(self) -> ObjectIdentifier:
        return self._value

    def __repr__(self) -> str:
        return f"<RegisteredID(value={self.value})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RegisteredID):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class IPAddress(GeneralName):
    def __init__(self, value: _IPAddressTypes) -> None:
        if not isinstance(
            value,
            (
                ipaddress.IPv4Address,
                ipaddress.IPv6Address,
                ipaddress.IPv4Network,
                ipaddress.IPv6Network,
            ),
        ):
            raise TypeError(
                "value must be an instance of ipaddress.IPv4Address, "
                "ipaddress.IPv6Address, ipaddress.IPv4Network, or "
                "ipaddress.IPv6Network"
            )

        self._value = value

    @property
    def value(self) -> _IPAddressTypes:
        return self._value

    def _packed(self) -> bytes:
        if isinstance(self.value, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return self.value.packed
        else:
            return self.value.network_address.packed + self.value.netmask.packed

    def __repr__(self) -> str:
        return f"<IPAddress(value={self.value})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPAddress):
            return NotImplemented

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class OtherName(GeneralName):
    def __init__(self, type_id: ObjectIdentifier, value: bytes) -> None:
        if not isinstance(type_id, ObjectIdentifier):
            raise TypeError("type_id must be an ObjectIdentifier")
        if not isinstance(value, bytes):
            raise TypeError("value must be a binary string")

        self._type_id = type_id
        self._value = value

    @property
    def type_id(self) -> ObjectIdentifier:
        return self._type_id

    @property
    def value(self) -> bytes:
        return self._value

    def __repr__(self) -> str:
        return "<OtherName(type_id={}, value={!r})>".format(self.type_id, self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OtherName):
            return NotImplemented

        return self.type_id == other.type_id and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.type_id, self.value))
