from __future__ import annotations

import logging
import os
import platform
import sys
import tempfile

IMPLEMENTATION = platform.python_implementation()
IS_PYPY = IMPLEMENTATION == "PyPy"
IS_CPYTHON = IMPLEMENTATION == "CPython"
IS_WIN = sys.platform == "win32"
IS_MAC_ARM64 = sys.platform == "darwin" and platform.machine() == "arm64"
ROOT = os.path.realpath(
    os.path.join(os.path.abspath(__file__), os.path.pardir, os.path.pardir)
)
IS_ZIPAPP = os.path.isfile(ROOT)

_CAN_SYMLINK = _FS_CASE_SENSITIVE = _CFG_DIR = _DATA_DIR = None


def fs_is_case_sensitive():
    global _FS_CASE_SENSITIVE  # noqa: PLW0603

    if _FS_CASE_SENSITIVE is None:
        with tempfile.NamedTemporaryFile(prefix="TmP") as tmp_file:
            _FS_CASE_SENSITIVE = not os.path.exists(tmp_file.name.lower())
            logging.debug(
                "filesystem is %scase-sensitive", "" if _FS_CASE_SENSITIVE else "not "
            )
    return _FS_CASE_SENSITIVE


def fs_supports_symlink():
    global _CAN_SYMLINK  # noqa: PLW0603

    if _CAN_SYMLINK is None:
        can = False
        if hasattr(os, "symlink"):
            if IS_WIN:
                with tempfile.NamedTemporaryFile(prefix="TmP") as tmp_file:
                    temp_dir = os.path.dirname(tmp_file.name)
                    dest = os.path.join(temp_dir, f"{tmp_file.name}-{'b'}")
                    try:
                        os.symlink(tmp_file.name, dest)
                        can = True
                    except (OSError, NotImplementedError):
                        pass
                logging.debug(
                    "symlink on filesystem does%s work", "" if can else " not"
                )
            else:
                can = True
        _CAN_SYMLINK = can
    return _CAN_SYMLINK


__all__ = (
    "IS_PYPY",
    "IS_CPYTHON",
    "IS_WIN",
    "fs_is_case_sensitive",
    "fs_supports_symlink",
    "ROOT",
    "IS_ZIPAPP",
    "IS_MAC_ARM64",
)
