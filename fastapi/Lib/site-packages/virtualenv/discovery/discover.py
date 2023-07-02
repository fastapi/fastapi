from __future__ import annotations

from abc import ABCMeta, abstractmethod


class Discover(metaclass=ABCMeta):
    """Discover and provide the requested Python interpreter."""

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        Add CLI arguments for this discovery mechanisms.

        :param parser: the CLI parser
        """
        raise NotImplementedError

    def __init__(self, options) -> None:
        """
        Create a new discovery mechanism.

        :param options: the parsed options as defined within :meth:`add_parser_arguments`
        """
        self._has_run = False
        self._interpreter = None
        self._env = options.env

    @abstractmethod
    def run(self):
        """
        Discovers an interpreter.

        :return: the interpreter ready to use for virtual environment creation
        """
        raise NotImplementedError

    @property
    def interpreter(self):
        """:return: the interpreter as returned by :meth:`run`, cached"""
        if self._has_run is False:
            self._interpreter = self.run()
            self._has_run = True
        return self._interpreter


__all__ = [
    "Discover",
]
