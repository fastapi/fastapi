from __future__ import annotations

import logging
from tempfile import mkdtemp

from virtualenv.util.path import safe_delete

from .via_disk_folder import AppDataDiskFolder


class TempAppData(AppDataDiskFolder):
    transient = True
    can_update = False

    def __init__(self) -> None:
        super().__init__(folder=mkdtemp())
        logging.debug("created temporary app data folder %s", self.lock.path)

    def reset(self):
        """This is a temporary folder, is already empty to start with."""

    def close(self):
        logging.debug("remove temporary app data folder %s", self.lock.path)
        safe_delete(self.lock.path)

    def embed_update_log(self, distribution, for_py_version):
        raise NotImplementedError


__all__ = [
    "TempAppData",
]
