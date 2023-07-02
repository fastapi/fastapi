"""AST triggers that are used for fine-grained dependency handling."""

from __future__ import annotations

from typing_extensions import Final

# Used as a suffix for triggers to handle "from m import *" dependencies (see also
# make_wildcard_trigger)

WILDCARD_TAG: Final = "[wildcard]"


def make_trigger(name: str) -> str:
    return f"<{name}>"


def make_wildcard_trigger(module: str) -> str:
    """Special trigger fired when any top-level name is changed in a module.

    Note that this is different from a module trigger, as module triggers are only
    fired if the module is created, deleted, or replaced with a non-module, whereas
    a wildcard trigger is triggered for namespace changes.

    This is used for "from m import *" dependencies.
    """
    return f"<{module}{WILDCARD_TAG}>"
