"""holds locking functionality that works across processes."""

from __future__ import annotations

import logging
import os
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager, suppress
from pathlib import Path
from threading import Lock, RLock

from filelock import FileLock, Timeout


class _CountedFileLock(FileLock):
    def __init__(self, lock_file) -> None:
        parent = os.path.dirname(lock_file)
        if not os.path.isdir(parent):
            with suppress(OSError):
                os.makedirs(parent)

        super().__init__(lock_file)
        self.count = 0
        self.thread_safe = RLock()

    def acquire(self, timeout=None, poll_interval=0.05):
        if not self.thread_safe.acquire(timeout=-1 if timeout is None else timeout):
            raise Timeout(self.lock_file)
        if self.count == 0:
            super().acquire(timeout, poll_interval)
        self.count += 1

    def release(self, force=False):  # noqa: FBT002
        with self.thread_safe:
            if self.count > 0:
                self.thread_safe.release()
            if self.count == 1:
                super().release(force=force)
            self.count = max(self.count - 1, 0)


_lock_store = {}
_store_lock = Lock()


class PathLockBase(metaclass=ABCMeta):
    def __init__(self, folder) -> None:
        path = Path(folder)
        self.path = path.resolve() if path.exists() else path

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"

    def __div__(self, other):
        return type(self)(self.path / other)

    def __truediv__(self, other):
        return self.__div__(other)

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def lock_for_key(self, name, no_block=False):  # noqa: FBT002
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def non_reentrant_lock_for_key(self, name):
        raise NotImplementedError


class ReentrantFileLock(PathLockBase):
    def __init__(self, folder) -> None:
        super().__init__(folder)
        self._lock = None

    def _create_lock(self, name=""):
        lock_file = str(self.path / f"{name}.lock")
        with _store_lock:
            if lock_file not in _lock_store:
                _lock_store[lock_file] = _CountedFileLock(lock_file)
            return _lock_store[lock_file]

    @staticmethod
    def _del_lock(lock):
        if lock is not None:
            with _store_lock, lock.thread_safe:
                if lock.count == 0:
                    _lock_store.pop(lock.lock_file, None)

    def __del__(self) -> None:
        self._del_lock(self._lock)

    def __enter__(self):
        self._lock = self._create_lock()
        self._lock_file(self._lock)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release(self._lock)
        self._del_lock(self._lock)
        self._lock = None

    def _lock_file(self, lock, no_block=False):  # noqa: FBT002
        # multiple processes might be trying to get a first lock... so we cannot check if this directory exist without
        # a lock, but that lock might then become expensive, and it's not clear where that lock should live.
        # Instead here we just ignore if we fail to create the directory.
        with suppress(OSError):
            os.makedirs(str(self.path))

        try:
            lock.acquire(0.0001)
        except Timeout:
            if no_block:
                raise
            logging.debug(
                "lock file %s present, will block until released", lock.lock_file
            )
            lock.release()  # release the acquire try from above
            lock.acquire()

    @staticmethod
    def _release(lock):
        lock.release()

    @contextmanager
    def lock_for_key(self, name, no_block=False):  # noqa: FBT002
        lock = self._create_lock(name)
        try:
            try:
                self._lock_file(lock, no_block)
                yield
            finally:
                self._release(lock)
        finally:
            self._del_lock(lock)
            lock = None

    @contextmanager
    def non_reentrant_lock_for_key(self, name):
        with _CountedFileLock(str(self.path / f"{name}.lock")):
            yield


class NoOpFileLock(PathLockBase):
    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @contextmanager
    def lock_for_key(self, name, no_block=False):  # noqa: ARG002, FBT002
        yield

    @contextmanager
    def non_reentrant_lock_for_key(self, name):  # noqa: ARG002
        yield


__all__ = [
    "NoOpFileLock",
    "ReentrantFileLock",
    "Timeout",
]
