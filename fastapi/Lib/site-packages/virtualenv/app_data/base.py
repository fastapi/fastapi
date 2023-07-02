"""Application data stored by virtualenv."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from virtualenv.info import IS_ZIPAPP


class AppData(metaclass=ABCMeta):
    """Abstract storage interface for the virtualenv application."""

    @abstractmethod
    def close(self):
        """Called before virtualenv exits."""

    @abstractmethod
    def reset(self):
        """Called when the user passes in the reset app data."""

    @abstractmethod
    def py_info(self, path):
        raise NotImplementedError

    @abstractmethod
    def py_info_clear(self):
        raise NotImplementedError

    @property
    def can_update(self):
        raise NotImplementedError

    @abstractmethod
    def embed_update_log(self, distribution, for_py_version):
        raise NotImplementedError

    @property
    def house(self):
        raise NotImplementedError

    @property
    def transient(self):
        raise NotImplementedError

    @abstractmethod
    def wheel_image(self, for_py_version, name):
        raise NotImplementedError

    @contextmanager
    def ensure_extracted(self, path, to_folder=None):
        """Some paths might be within the zipapp, unzip these to a path on the disk."""
        if IS_ZIPAPP:
            with self.extract(path, to_folder) as result:
                yield result
        else:
            yield path

    @abstractmethod
    @contextmanager
    def extract(self, path, to_folder):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def locked(self, path):
        raise NotImplementedError


class ContentStore(metaclass=ABCMeta):
    @abstractmethod
    def exists(self):
        raise NotImplementedError

    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def write(self, content):
        raise NotImplementedError

    @abstractmethod
    def remove(self):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def locked(self):
        pass


__all__ = [
    "ContentStore",
    "AppData",
]
