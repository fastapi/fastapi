from __future__ import annotations

import json
import logging


class Session:
    """Represents a virtual environment creation session."""

    def __init__(
        self, verbosity, app_data, interpreter, creator, seeder, activators
    ) -> None:  # noqa: PLR0913
        self._verbosity = verbosity
        self._app_data = app_data
        self._interpreter = interpreter
        self._creator = creator
        self._seeder = seeder
        self._activators = activators

    @property
    def verbosity(self):
        """The verbosity of the run."""
        return self._verbosity

    @property
    def interpreter(self):
        """Create a virtual environment based on this reference interpreter."""
        return self._interpreter

    @property
    def creator(self):
        """The creator used to build the virtual environment (must be compatible with the interpreter)."""
        return self._creator

    @property
    def seeder(self):
        """The mechanism used to provide the seed packages (pip, setuptools, wheel)."""
        return self._seeder

    @property
    def activators(self):
        """Activators used to generate activations scripts."""
        return self._activators

    def run(self):
        self._create()
        self._seed()
        self._activate()
        self.creator.pyenv_cfg.write()

    def _create(self):
        logging.info("create virtual environment via %s", self.creator)
        self.creator.run()
        logging.debug(_DEBUG_MARKER)
        logging.debug("%s", _Debug(self.creator))

    def _seed(self):
        if self.seeder is not None and self.seeder.enabled:
            logging.info("add seed packages via %s", self.seeder)
            self.seeder.run(self.creator)

    def _activate(self):
        if self.activators:
            active = ", ".join(
                type(i).__name__.replace("Activator", "") for i in self.activators
            )
            logging.info("add activators for %s", active)
            for activator in self.activators:
                activator.generate(self.creator)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._app_data.close()


_DEBUG_MARKER = "=" * 30 + " target debug " + "=" * 30


class _Debug:
    """lazily populate debug."""

    def __init__(self, creator) -> None:
        self.creator = creator

    def __repr__(self) -> str:
        return json.dumps(self.creator.debug, indent=2)


__all__ = [
    "Session",
]
