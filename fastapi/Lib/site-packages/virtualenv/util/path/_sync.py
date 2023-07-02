from __future__ import annotations

import logging
import os
import shutil
import sys
from stat import S_IWUSR


def ensure_dir(path):
    if not path.exists():
        logging.debug("create folder %s", str(path))
        os.makedirs(str(path))


def ensure_safe_to_do(src, dest):
    if src == dest:
        msg = f"source and destination is the same {src}"
        raise ValueError(msg)
    if not dest.exists():
        return
    if dest.is_dir() and not dest.is_symlink():
        logging.debug("remove directory %s", dest)
        safe_delete(dest)
    else:
        logging.debug("remove file %s", dest)
        dest.unlink()


def symlink(src, dest):
    ensure_safe_to_do(src, dest)
    logging.debug("symlink %s", _Debug(src, dest))
    dest.symlink_to(src, target_is_directory=src.is_dir())


def copy(src, dest):
    ensure_safe_to_do(src, dest)
    is_dir = src.is_dir()
    method = copytree if is_dir else shutil.copy
    logging.debug("copy %s", _Debug(src, dest))
    method(str(src), str(dest))


def copytree(src, dest):
    for root, _, files in os.walk(src):
        dest_dir = os.path.join(dest, os.path.relpath(root, src))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        for name in files:
            src_f = os.path.join(root, name)
            dest_f = os.path.join(dest_dir, name)
            shutil.copy(src_f, dest_f)


def safe_delete(dest):
    def onerror(func, path, exc_info):  # noqa: ARG001
        if not os.access(path, os.W_OK):
            os.chmod(path, S_IWUSR)
            func(path)
        else:
            raise

    kwargs = {"onexc" if sys.version_info >= (3, 12) else "onerror": onerror}
    shutil.rmtree(str(dest), ignore_errors=True, **kwargs)


class _Debug:
    def __init__(self, src, dest) -> None:
        self.src = src
        self.dest = dest

    def __str__(self) -> str:
        return (
            f"{'directory ' if self.src.is_dir() else ''}{self.src!s} to {self.dest!s}"
        )


__all__ = [
    "ensure_dir",
    "symlink",
    "copy",
    "symlink",
    "copytree",
    "safe_delete",
]
