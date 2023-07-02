from __future__ import annotations

import json
import logging
import os
import sys
from abc import ABCMeta, abstractmethod
from argparse import ArgumentTypeError
from ast import literal_eval
from collections import OrderedDict
from pathlib import Path

from virtualenv.discovery.cached_py_info import LogCmd
from virtualenv.util.path import safe_delete
from virtualenv.util.subprocess import run_cmd
from virtualenv.version import __version__

from .pyenv_cfg import PyEnvCfg

HERE = Path(os.path.abspath(__file__)).parent
DEBUG_SCRIPT = HERE / "debug.py"


class CreatorMeta:
    def __init__(self) -> None:
        self.error = None


class Creator(metaclass=ABCMeta):
    """A class that given a python Interpreter creates a virtual environment."""

    def __init__(self, options, interpreter) -> None:
        """
        Construct a new virtual environment creator.

        :param options: the CLI option as parsed from :meth:`add_parser_arguments`
        :param interpreter: the interpreter to create virtual environment from
        """
        self.interpreter = interpreter
        self._debug = None
        self.dest = Path(options.dest)
        self.clear = options.clear
        self.no_vcs_ignore = options.no_vcs_ignore
        self.pyenv_cfg = PyEnvCfg.from_folder(self.dest)
        self.app_data = options.app_data
        self.env = options.env

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self._args())})"

    def _args(self):
        return [
            ("dest", str(self.dest)),
            ("clear", self.clear),
            ("no_vcs_ignore", self.no_vcs_ignore),
        ]

    @classmethod
    def can_create(cls, interpreter):  # noqa: ARG003
        """
        Determine if we can create a virtual environment.

        :param interpreter: the interpreter in question
        :return: ``None`` if we can't create, any other object otherwise that will be forwarded to \
                  :meth:`add_parser_arguments`
        """
        return True

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, meta, app_data):  # noqa: ARG003
        """
        Add CLI arguments for the creator.

        :param parser: the CLI parser
        :param app_data: the application data folder
        :param interpreter: the interpreter we're asked to create virtual environment for
        :param meta: value as returned by :meth:`can_create`
        """
        parser.add_argument(
            "dest",
            help="directory to create virtualenv at",
            type=cls.validate_dest,
        )
        parser.add_argument(
            "--clear",
            dest="clear",
            action="store_true",
            help="remove the destination directory if exist before starting (will overwrite files otherwise)",
            default=False,
        )
        parser.add_argument(
            "--no-vcs-ignore",
            dest="no_vcs_ignore",
            action="store_true",
            help="don't create VCS ignore directive in the destination directory",
            default=False,
        )

    @abstractmethod
    def create(self):
        """Perform the virtual environment creation."""
        raise NotImplementedError

    @classmethod
    def validate_dest(cls, raw_value):  # noqa: C901
        """No path separator in the path, valid chars and must be write-able."""

        def non_write_able(dest, value):
            common = Path(*os.path.commonprefix([value.parts, dest.parts]))
            msg = f"the destination {dest.relative_to(common)} is not write-able at {common}"
            raise ArgumentTypeError(msg)

        # the file system must be able to encode
        # note in newer CPython this is always utf-8 https://www.python.org/dev/peps/pep-0529/
        encoding = sys.getfilesystemencoding()
        refused = OrderedDict()
        kwargs = {"errors": "ignore"} if encoding != "mbcs" else {}
        for char in str(raw_value):
            try:
                trip = char.encode(encoding, **kwargs).decode(encoding)
                if trip == char:
                    continue
                raise ValueError(trip)  # noqa: TRY301
            except ValueError:
                refused[char] = None
        if refused:
            bad = "".join(refused.keys())
            msg = f"the file system codec ({encoding}) cannot handle characters {bad!r} within {raw_value!r}"
            raise ArgumentTypeError(msg)
        if os.pathsep in raw_value:
            msg = (
                f"destination {raw_value!r} must not contain the path separator ({os.pathsep})"
                f" as this would break the activation scripts"
            )
            raise ArgumentTypeError(msg)

        value = Path(raw_value)
        if value.exists() and value.is_file():
            msg = f"the destination {value} already exists and is a file"
            raise ArgumentTypeError(msg)
        dest = Path(
            os.path.abspath(str(value))
        ).resolve()  # on Windows absolute does not imply resolve so use both
        value = dest
        while dest:
            if dest.exists():
                if os.access(str(dest), os.W_OK):
                    break
                non_write_able(dest, value)
            base, _ = dest.parent, dest.name
            if base == dest:
                non_write_able(dest, value)  # pragma: no cover
            dest = base
        return str(value)

    def run(self):
        if self.dest.exists() and self.clear:
            logging.debug("delete %s", self.dest)
            safe_delete(self.dest)
        self.create()
        self.set_pyenv_cfg()
        if not self.no_vcs_ignore:
            self.setup_ignore_vcs()

    def set_pyenv_cfg(self):
        self.pyenv_cfg.content = OrderedDict()
        self.pyenv_cfg["home"] = os.path.dirname(
            os.path.abspath(self.interpreter.system_executable)
        )
        self.pyenv_cfg["implementation"] = self.interpreter.implementation
        self.pyenv_cfg["version_info"] = ".".join(
            str(i) for i in self.interpreter.version_info
        )
        self.pyenv_cfg["virtualenv"] = __version__

    def setup_ignore_vcs(self):
        """Generate ignore instructions for version control systems."""
        # mark this folder to be ignored by VCS, handle https://www.python.org/dev/peps/pep-0610/#registered-vcs
        git_ignore = self.dest / ".gitignore"
        if not git_ignore.exists():
            git_ignore.write_text(
                "# created by virtualenv automatically\n*\n", encoding="utf-8"
            )
        # Mercurial - does not support the .hgignore file inside a subdirectory directly, but only if included via the
        # subinclude directive from root, at which point on might as well ignore the directory itself, see
        # https://www.selenic.com/mercurial/hgignore.5.html for more details
        # Bazaar - does not support ignore files in sub-directories, only at root level via .bzrignore
        # Subversion - does not support ignore files, requires direct manipulation with the svn tool

    @property
    def debug(self):
        """:return: debug information about the virtual environment (only valid after :meth:`create` has run)"""
        if self._debug is None and self.exe is not None:
            self._debug = get_env_debug_info(
                self.exe, self.debug_script(), self.app_data, self.env
            )
        return self._debug

    @staticmethod
    def debug_script():
        return DEBUG_SCRIPT


def get_env_debug_info(env_exe, debug_script, app_data, env):
    env = env.copy()
    env.pop("PYTHONPATH", None)

    with app_data.ensure_extracted(debug_script) as debug_script:
        cmd = [str(env_exe), str(debug_script)]
        logging.debug("debug via %r", LogCmd(cmd))
        code, out, err = run_cmd(cmd)

    try:
        if code != 0:
            if out:
                result = literal_eval(out)
            else:
                if code == 2 and "file" in err:  # noqa: PLR2004
                    # Re-raise FileNotFoundError from `run_cmd()`
                    raise OSError(err)  # noqa: TRY301
                raise Exception(err)  # noqa: TRY002, TRY301
        else:
            result = json.loads(out)
        if err:
            result["err"] = err
    except Exception as exception:  # noqa: BLE001
        return {
            "out": out,
            "err": err,
            "returncode": code,
            "exception": repr(exception),
        }
    if "sys" in result and "path" in result["sys"]:
        del result["sys"]["path"][0]
    return result


__all__ = [
    "Creator",
    "CreatorMeta",
]
