from __future__ import annotations

from abc import ABCMeta

from virtualenv.create.creator import Creator
from virtualenv.create.describe import Describe


class VirtualenvBuiltin(Creator, Describe, metaclass=ABCMeta):
    """A creator that does operations itself without delegation, if we can create it we can also describe it."""

    def __init__(self, options, interpreter) -> None:
        Creator.__init__(self, options, interpreter)
        Describe.__init__(self, self.dest, interpreter)


__all__ = [
    "VirtualenvBuiltin",
]
