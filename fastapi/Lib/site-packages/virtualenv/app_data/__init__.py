"""Application data stored by virtualenv."""

from __future__ import annotations

import logging
import os

from platformdirs import user_data_dir

from .na import AppDataDisabled
from .read_only import ReadOnlyAppData
from .via_disk_folder import AppDataDiskFolder
from .via_tempdir import TempAppData


def _default_app_data_dir(env):
    key = "VIRTUALENV_OVERRIDE_APP_DATA"
    if key in env:
        return env[key]
    return user_data_dir(appname="virtualenv", appauthor="pypa")


def make_app_data(folder, **kwargs):
    is_read_only = kwargs.pop("read_only")
    env = kwargs.pop("env")
    if kwargs:  # py3+ kwonly
        msg = "unexpected keywords: {}"
        raise TypeError(msg)

    if folder is None:
        folder = _default_app_data_dir(env)
    folder = os.path.abspath(folder)

    if is_read_only:
        return ReadOnlyAppData(folder)

    if not os.path.isdir(folder):
        try:
            os.makedirs(folder)
            logging.debug("created app data folder %s", folder)
        except OSError as exception:
            logging.info(
                "could not create app data folder %s due to %r", folder, exception
            )

    if os.access(folder, os.W_OK):
        return AppDataDiskFolder(folder)
    logging.debug("app data folder %s has no write access", folder)
    return TempAppData()


__all__ = (
    "AppDataDisabled",
    "AppDataDiskFolder",
    "ReadOnlyAppData",
    "TempAppData",
    "make_app_data",
)
