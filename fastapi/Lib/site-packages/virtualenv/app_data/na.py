from __future__ import annotations

from contextlib import contextmanager

from .base import AppData, ContentStore


class AppDataDisabled(AppData):
    """No application cache available (most likely as we don't have write permissions)."""

    transient = True
    can_update = False

    def __init__(self) -> None:
        pass

    error = RuntimeError(
        "no app data folder available, probably no write access to the folder"
    )

    def close(self):
        """Do nothing."""

    def reset(self):
        """Do nothing."""

    def py_info(self, path):  # noqa: ARG002
        return ContentStoreNA()

    def embed_update_log(self, distribution, for_py_version):  # noqa: ARG002
        return ContentStoreNA()

    def extract(self, path, to_folder):  # noqa: ARG002
        raise self.error

    @contextmanager
    def locked(self, path):  # noqa: ARG002
        """Do nothing."""
        yield

    @property
    def house(self):
        raise self.error

    def wheel_image(self, for_py_version, name):  # noqa: ARG002
        raise self.error

    def py_info_clear(self):
        """Nothing to clear."""


class ContentStoreNA(ContentStore):
    def exists(self):
        return False

    def read(self):
        """Nothing to read."""
        return

    def write(self, content):
        """Nothing to write."""

    def remove(self):
        """Nothing to remove."""

    @contextmanager
    def locked(self):
        yield


__all__ = [
    "AppDataDisabled",
    "ContentStoreNA",
]
