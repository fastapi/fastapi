from __future__ import annotations

import logging
import os


class TypeData:
    def __init__(self, default_type, as_type) -> None:
        self.default_type = default_type
        self.as_type = as_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base={self.default_type}, as={self.as_type})"

    def convert(self, value):
        return self.default_type(value)


class BoolType(TypeData):
    BOOLEAN_STATES = {
        "1": True,
        "yes": True,
        "true": True,
        "on": True,
        "0": False,
        "no": False,
        "false": False,
        "off": False,
    }

    def convert(self, value):
        if value.lower() not in self.BOOLEAN_STATES:
            msg = f"Not a boolean: {value}"
            raise ValueError(msg)
        return self.BOOLEAN_STATES[value.lower()]


class NoneType(TypeData):
    def convert(self, value):
        if not value:
            return None
        return str(value)


class ListType(TypeData):
    def _validate(self):
        """no op."""

    def convert(self, value, flatten=True):  # noqa: ARG002, FBT002
        values = self.split_values(value)
        result = []
        for value in values:
            sub_values = value.split(os.pathsep)
            result.extend(sub_values)
        return [self.as_type(i) for i in result]

    def split_values(self, value):
        """
        Split the provided value into a list.

        First this is done by newlines. If there were no newlines in the text,
        then we next try to split by comma.
        """
        if isinstance(value, (str, bytes)):
            # Use `splitlines` rather than a custom check for whether there is
            # more than one line. This ensures that the full `splitlines()`
            # logic is supported here.
            values = value.splitlines()
            if len(values) <= 1:
                values = value.split(",")
            values = filter(None, [x.strip() for x in values])
        else:
            values = list(value)

        return values


def convert(value, as_type, source):
    """Convert the value as a given type where the value comes from the given source."""
    try:
        return as_type.convert(value)
    except Exception as exception:
        logging.warning(
            "%s failed to convert %r as %r because %r",
            source,
            value,
            as_type,
            exception,
        )
        raise


_CONVERT = {bool: BoolType, type(None): NoneType, list: ListType}


def get_type(action):
    default_type = type(action.default)
    as_type = default_type if action.type is None else action.type
    return _CONVERT.get(default_type, TypeData)(default_type, as_type)


__all__ = [
    "convert",
    "get_type",
]
