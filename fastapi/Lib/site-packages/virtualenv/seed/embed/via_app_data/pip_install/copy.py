from __future__ import annotations

import os
from pathlib import Path

from virtualenv.util.path import copy

from .base import PipInstall


class CopyPipInstall(PipInstall):
    def _sync(self, src, dst):
        copy(src, dst)

    def _generate_new_files(self):
        # create the pyc files
        new_files = super()._generate_new_files()
        new_files.update(self._cache_files())
        return new_files

    def _cache_files(self):
        version = self._creator.interpreter.version_info
        py_c_ext = f".{self._creator.interpreter.implementation.lower()}-{version.major}{version.minor}.pyc"
        for root, dirs, files in os.walk(str(self._image_dir), topdown=True):
            root_path = Path(root)
            for name in files:
                if name.endswith(".py"):
                    yield root_path / f"{name[:-3]}{py_c_ext}"
            for name in dirs:
                yield root_path / name / "__pycache__"

    def _fix_records(self, new_files):
        extra_record_data_str = self._records_text(new_files)
        with (self._dist_info / "RECORD").open("ab") as file_handler:
            file_handler.write(extra_record_data_str.encode("utf-8"))


__all__ = [
    "CopyPipInstall",
]
