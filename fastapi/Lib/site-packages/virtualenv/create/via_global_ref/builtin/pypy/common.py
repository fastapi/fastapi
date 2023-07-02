from __future__ import annotations

import abc
from pathlib import Path

from virtualenv.create.via_global_ref.builtin.ref import PathRefToDest, RefMust, RefWhen
from virtualenv.create.via_global_ref.builtin.via_global_self_do import (
    ViaGlobalRefVirtualenvBuiltin,
)


class PyPy(ViaGlobalRefVirtualenvBuiltin, metaclass=abc.ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.implementation == "PyPy" and super().can_describe(
            interpreter
        )

    @classmethod
    def _executables(cls, interpreter):
        host = Path(interpreter.system_executable)
        targets = sorted(f"{name}{PyPy.suffix}" for name in cls.exe_names(interpreter))
        yield host, targets, RefMust.NA, RefWhen.ANY

    @classmethod
    def executables(cls, interpreter):
        yield from super().sources(interpreter)

    @classmethod
    def exe_names(cls, interpreter):
        return {
            cls.exe_stem(),
            "python",
            f"python{interpreter.version_info.major}",
            f"python{interpreter.version_info.major}.{interpreter.version_info.minor}",
        }

    @classmethod
    def sources(cls, interpreter):
        yield from cls.executables(interpreter)
        for host in cls._add_shared_libs(interpreter):
            yield PathRefToDest(host, dest=lambda self, s: self.bin_dir / s.name)

    @classmethod
    def _add_shared_libs(cls, interpreter):
        # https://bitbucket.org/pypy/pypy/issue/1922/future-proofing-virtualenv
        python_dir = Path(interpreter.system_executable).resolve().parent
        yield from cls._shared_libs(python_dir)

    @classmethod
    def _shared_libs(cls, python_dir):
        raise NotImplementedError


__all__ = [
    "PyPy",
]
