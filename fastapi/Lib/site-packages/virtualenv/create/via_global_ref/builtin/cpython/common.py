from __future__ import annotations

from abc import ABCMeta
from collections import OrderedDict
from pathlib import Path

from virtualenv.create.describe import PosixSupports, WindowsSupports
from virtualenv.create.via_global_ref.builtin.ref import RefMust, RefWhen
from virtualenv.create.via_global_ref.builtin.via_global_self_do import (
    ViaGlobalRefVirtualenvBuiltin,
)


class CPython(ViaGlobalRefVirtualenvBuiltin, metaclass=ABCMeta):
    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.implementation == "CPython" and super().can_describe(
            interpreter
        )

    @classmethod
    def exe_stem(cls):
        return "python"


class CPythonPosix(CPython, PosixSupports, metaclass=ABCMeta):
    """Create a CPython virtual environment on POSIX platforms."""

    @classmethod
    def _executables(cls, interpreter):
        host_exe = Path(interpreter.system_executable)
        major, minor = interpreter.version_info.major, interpreter.version_info.minor
        targets = OrderedDict(
            (i, None)
            for i in [
                "python",
                f"python{major}",
                f"python{major}.{minor}",
                host_exe.name,
            ]
        )
        yield host_exe, list(targets.keys()), RefMust.NA, RefWhen.ANY


class CPythonWindows(CPython, WindowsSupports, metaclass=ABCMeta):
    @classmethod
    def _executables(cls, interpreter):
        # symlink of the python executables does not work reliably, copy always instead
        # - https://bugs.python.org/issue42013
        # - venv
        host = cls.host_python(interpreter)
        for path in (
            host.parent / n for n in {"python.exe", host.name}
        ):  # noqa: PLC0208
            yield host, [path.name], RefMust.COPY, RefWhen.ANY
        # for more info on pythonw.exe see https://stackoverflow.com/a/30313091
        python_w = host.parent / "pythonw.exe"
        yield python_w, [python_w.name], RefMust.COPY, RefWhen.ANY

    @classmethod
    def host_python(cls, interpreter):
        return Path(interpreter.system_executable)


def is_mac_os_framework(interpreter):
    if interpreter.platform == "darwin":
        return interpreter.sysconfig_vars.get("PYTHONFRAMEWORK") == "Python3"
    return False


__all__ = [
    "CPython",
    "CPythonPosix",
    "CPythonWindows",
    "is_mac_os_framework",
]
