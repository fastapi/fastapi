from __future__ import annotations

from abc import ABCMeta
from collections import OrderedDict
from pathlib import Path

from virtualenv.info import IS_WIN


class Describe(metaclass=ABCMeta):
    """Given a host interpreter tell us information about what the created interpreter might look like."""

    suffix = ".exe" if IS_WIN else ""

    def __init__(self, dest, interpreter) -> None:
        self.interpreter = interpreter
        self.dest = dest
        self._stdlib = None
        self._stdlib_platform = None
        self._system_stdlib = None
        self._conf_vars = None

    @property
    def bin_dir(self):
        return self.script_dir

    @property
    def script_dir(self):
        return self.dest / self.interpreter.install_path("scripts")

    @property
    def purelib(self):
        return self.dest / self.interpreter.install_path("purelib")

    @property
    def platlib(self):
        return self.dest / self.interpreter.install_path("platlib")

    @property
    def libs(self):
        return list(OrderedDict(((self.platlib, None), (self.purelib, None))).keys())

    @property
    def stdlib(self):
        if self._stdlib is None:
            self._stdlib = Path(
                self.interpreter.sysconfig_path("stdlib", config_var=self._config_vars)
            )
        return self._stdlib

    @property
    def stdlib_platform(self):
        if self._stdlib_platform is None:
            self._stdlib_platform = Path(
                self.interpreter.sysconfig_path(
                    "platstdlib", config_var=self._config_vars
                )
            )
        return self._stdlib_platform

    @property
    def _config_vars(self):
        if self._conf_vars is None:
            self._conf_vars = self._calc_config_vars(self.dest)
        return self._conf_vars

    def _calc_config_vars(self, to):
        sys_vars = self.interpreter.sysconfig_vars
        return {
            k: (to if v is not None and v.startswith(self.interpreter.prefix) else v)
            for k, v in sys_vars.items()
        }

    @classmethod
    def can_describe(cls, interpreter):  # noqa: ARG003
        """Knows means it knows how the output will look."""
        return True

    @property
    def env_name(self):
        return self.dest.parts[-1]

    @property
    def exe(self):
        return self.bin_dir / f"{self.exe_stem()}{self.suffix}"

    @classmethod
    def exe_stem(cls):
        """Executable name without suffix - there seems to be no standard way to get this without creating it."""
        raise NotImplementedError

    def script(self, name):
        return self.script_dir / f"{name}{self.suffix}"


class Python3Supports(Describe, metaclass=ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.version_info.major == 3 and super().can_describe(
            interpreter
        )  # noqa: PLR2004


class PosixSupports(Describe, metaclass=ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.os == "posix" and super().can_describe(interpreter)


class WindowsSupports(Describe, metaclass=ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.os == "nt" and super().can_describe(interpreter)


__all__ = [
    "Describe",
    "Python3Supports",
    "PosixSupports",
    "WindowsSupports",
]
