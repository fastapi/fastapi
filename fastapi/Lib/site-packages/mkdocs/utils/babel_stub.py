from __future__ import annotations

from string import ascii_letters
from typing import NamedTuple


class UnknownLocaleError(Exception):
    pass


class Locale(NamedTuple):
    language: str
    territory: str = ""

    def __str__(self):
        if self.territory:
            return f"{self.language}_{self.territory}"
        return self.language

    @classmethod
    def parse(cls, identifier, sep):
        if not isinstance(identifier, str):
            raise TypeError(f"Unexpected value for identifier: '{identifier}'")
        locale = cls(*identifier.split(sep, 1))
        if not all(x in ascii_letters for x in locale.language):
            raise ValueError(f"expected only letters, got '{locale.language}'")
        if len(locale.language) != 2:
            raise UnknownLocaleError(f"unknown locale '{locale.language}'")
        return locale
