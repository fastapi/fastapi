from __future__ import annotations

import logging
import os
from configparser import ConfigParser
from pathlib import Path

from platformdirs import user_config_dir

from .convert import convert


class IniConfig:
    VIRTUALENV_CONFIG_FILE_ENV_VAR = "VIRTUALENV_CONFIG_FILE"
    STATE = {None: "failed to parse", True: "active", False: "missing"}

    section = "virtualenv"

    def __init__(self, env=None) -> None:
        env = os.environ if env is None else env
        config_file = env.get(self.VIRTUALENV_CONFIG_FILE_ENV_VAR, None)
        self.is_env_var = config_file is not None
        if config_file is None:
            config_file = (
                Path(user_config_dir(appname="virtualenv", appauthor="pypa"))
                / "virtualenv.ini"
            )
        else:
            config_file = Path(config_file)
        self.config_file = config_file
        self._cache = {}

        exception = None
        self.has_config_file = None
        try:
            self.has_config_file = self.config_file.exists()
        except OSError as exc:
            exception = exc
        else:
            if self.has_config_file:
                self.config_file = self.config_file.resolve()
                self.config_parser = ConfigParser()
                try:
                    self._load()
                    self.has_virtualenv_section = self.config_parser.has_section(
                        self.section
                    )
                except Exception as exc:  # noqa: BLE001
                    exception = exc
        if exception is not None:
            logging.error(
                "failed to read config file %s because %r", config_file, exception
            )

    def _load(self):
        with self.config_file.open("rt", encoding="utf-8") as file_handler:
            return self.config_parser.read_file(file_handler)

    def get(self, key, as_type):
        cache_key = key, as_type
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            source = "file"
            raw_value = self.config_parser.get(self.section, key.lower())
            value = convert(raw_value, as_type, source)
            result = value, source
        except Exception:  # noqa: BLE001
            result = None
        self._cache[cache_key] = result
        return result

    def __bool__(self) -> bool:
        return bool(self.has_config_file) and bool(self.has_virtualenv_section)

    @property
    def epilog(self):
        return (
            f"\nconfig file {self.config_file} {self.STATE[self.has_config_file]} "
            f"(change{'d' if self.is_env_var else ''} via env var {self.VIRTUALENV_CONFIG_FILE_ENV_VAR})"
        )
