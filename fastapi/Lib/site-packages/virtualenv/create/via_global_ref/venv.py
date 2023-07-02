from __future__ import annotations

import logging
from copy import copy

from virtualenv.create.via_global_ref.store import handle_store_python
from virtualenv.discovery.py_info import PythonInfo
from virtualenv.util.error import ProcessCallFailedError
from virtualenv.util.path import ensure_dir
from virtualenv.util.subprocess import run_cmd

from .api import ViaGlobalRefApi, ViaGlobalRefMeta
from .builtin.pypy.pypy3 import Pypy3Windows


class Venv(ViaGlobalRefApi):
    def __init__(self, options, interpreter) -> None:
        self.describe = options.describe
        super().__init__(options, interpreter)
        current = PythonInfo.current()
        self.can_be_inline = (
            interpreter is current
            and interpreter.executable == interpreter.system_executable
        )
        self._context = None

    def _args(self):
        return super()._args() + (
            [("describe", self.describe.__class__.__name__)] if self.describe else []
        )

    @classmethod
    def can_create(cls, interpreter):
        if interpreter.has_venv:
            meta = ViaGlobalRefMeta()
            if interpreter.platform == "win32":
                meta = handle_store_python(meta, interpreter)
            return meta
        return None

    def create(self):
        if self.can_be_inline:
            self.create_inline()
        else:
            self.create_via_sub_process()
        for lib in self.libs:
            ensure_dir(lib)
        super().create()
        self.executables_for_win_pypy_less_v37()

    def executables_for_win_pypy_less_v37(self):
        """
        PyPy <= 3.6 (v7.3.3) for Windows contains only pypy3.exe and pypy3w.exe
        Venv does not handle non-existing exe sources, e.g. python.exe, so this
        patch does it.
        """  # noqa: D205
        creator = self.describe
        if isinstance(creator, Pypy3Windows) and creator.less_v37:
            for exe in creator.executables(self.interpreter):
                exe.run(creator, self.symlinks)

    def create_inline(self):
        from venv import EnvBuilder

        builder = EnvBuilder(
            system_site_packages=self.enable_system_site_package,
            clear=False,
            symlinks=self.symlinks,
            with_pip=False,
        )
        builder.create(str(self.dest))

    def create_via_sub_process(self):
        cmd = self.get_host_create_cmd()
        logging.info("using host built-in venv to create via %s", " ".join(cmd))
        code, out, err = run_cmd(cmd)
        if code != 0:
            raise ProcessCallFailedError(code, out, err, cmd)

    def get_host_create_cmd(self):
        cmd = [self.interpreter.system_executable, "-m", "venv", "--without-pip"]
        if self.enable_system_site_package:
            cmd.append("--system-site-packages")
        cmd.append("--symlinks" if self.symlinks else "--copies")
        cmd.append(str(self.dest))
        return cmd

    def set_pyenv_cfg(self):
        # prefer venv options over ours, but keep our extra
        venv_content = copy(self.pyenv_cfg.refresh())
        super().set_pyenv_cfg()
        self.pyenv_cfg.update(venv_content)

    def __getattribute__(self, item):
        describe = object.__getattribute__(self, "describe")
        if describe is not None and hasattr(describe, item):
            element = getattr(describe, item)
            if not callable(element) or item in ("script",):
                return element
        return object.__getattribute__(self, item)


__all__ = [
    "Venv",
]
