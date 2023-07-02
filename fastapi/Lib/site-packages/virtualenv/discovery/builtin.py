from __future__ import annotations

import logging
import os
import sys

from virtualenv.info import IS_WIN

from .discover import Discover
from .py_info import PythonInfo
from .py_spec import PythonSpec


class Builtin(Discover):
    def __init__(self, options) -> None:
        super().__init__(options)
        self.python_spec = options.python if options.python else [sys.executable]
        self.app_data = options.app_data
        self.try_first_with = options.try_first_with

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument(
            "-p",
            "--python",
            dest="python",
            metavar="py",
            type=str,
            action="append",
            default=[],
            help="interpreter based on what to create environment (path/identifier) "
            "- by default use the interpreter where the tool is installed - first found wins",
        )
        parser.add_argument(
            "--try-first-with",
            dest="try_first_with",
            metavar="py_exe",
            type=str,
            action="append",
            default=[],
            help="try first these interpreters before starting the discovery",
        )

    def run(self):
        for python_spec in self.python_spec:
            result = get_interpreter(
                python_spec, self.try_first_with, self.app_data, self._env
            )
            if result is not None:
                return result
        return None

    def __repr__(self) -> str:
        spec = self.python_spec[0] if len(self.python_spec) == 1 else self.python_spec
        return f"{self.__class__.__name__} discover of python_spec={spec!r}"


def get_interpreter(key, try_first_with, app_data=None, env=None):
    spec = PythonSpec.from_string_spec(key)
    logging.info("find interpreter for spec %r", spec)
    proposed_paths = set()
    env = os.environ if env is None else env
    for interpreter, impl_must_match in propose_interpreters(
        spec, try_first_with, app_data, env
    ):
        key = interpreter.system_executable, impl_must_match
        if key in proposed_paths:
            continue
        logging.info("proposed %s", interpreter)
        if interpreter.satisfies(spec, impl_must_match):
            logging.debug("accepted %s", interpreter)
            return interpreter
        proposed_paths.add(key)
    return None


def propose_interpreters(
    spec, try_first_with, app_data, env=None
):  # noqa: C901, PLR0912
    # 0. try with first
    env = os.environ if env is None else env
    for py_exe in try_first_with:
        path = os.path.abspath(py_exe)
        try:
            os.lstat(
                path
            )  # Windows Store Python does not work with os.path.exists, but does for os.lstat
        except OSError:
            pass
        else:
            yield PythonInfo.from_exe(os.path.abspath(path), app_data, env=env), True

    # 1. if it's a path and exists
    if spec.path is not None:
        try:
            os.lstat(
                spec.path
            )  # Windows Store Python does not work with os.path.exists, but does for os.lstat
        except OSError:
            if spec.is_abs:
                raise
        else:
            yield PythonInfo.from_exe(
                os.path.abspath(spec.path), app_data, env=env
            ), True
        if spec.is_abs:
            return
    else:
        # 2. otherwise try with the current
        yield PythonInfo.current_system(app_data), True

        # 3. otherwise fallback to platform default logic
        if IS_WIN:
            from .windows import propose_interpreters

            for interpreter in propose_interpreters(spec, app_data, env):
                yield interpreter, True
    # finally just find on path, the path order matters (as the candidates are less easy to control by end user)
    paths = get_paths(env)
    tested_exes = set()
    for pos, path in enumerate(paths):
        path_str = str(path)
        logging.debug(LazyPathDump(pos, path_str, env))
        for candidate, match in possible_specs(spec):
            found = check_path(candidate, path_str)
            if found is not None:
                exe = os.path.abspath(found)
                if exe not in tested_exes:
                    tested_exes.add(exe)
                    interpreter = PathPythonInfo.from_exe(
                        exe, app_data, raise_on_error=False, env=env
                    )
                    if interpreter is not None:
                        yield interpreter, match


def get_paths(env):
    path = env.get("PATH", None)
    if path is None:
        try:
            path = os.confstr("CS_PATH")
        except (AttributeError, ValueError):
            path = os.defpath
    return [] if not path else [p for p in path.split(os.pathsep) if os.path.exists(p)]


class LazyPathDump:
    def __init__(self, pos, path, env) -> None:
        self.pos = pos
        self.path = path
        self.env = env

    def __repr__(self) -> str:
        content = f"discover PATH[{self.pos}]={self.path}"
        if self.env.get("_VIRTUALENV_DEBUG"):  # this is the over the board debug
            content += " with =>"
            for file_name in os.listdir(self.path):
                try:
                    file_path = os.path.join(self.path, file_name)
                    if os.path.isdir(file_path) or not os.access(file_path, os.X_OK):
                        continue
                except OSError:
                    pass
                content += " "
                content += file_name
        return content


def check_path(candidate, path):
    _, ext = os.path.splitext(candidate)
    if sys.platform == "win32" and ext != ".exe":
        candidate = candidate + ".exe"
    if os.path.isfile(candidate):
        return candidate
    candidate = os.path.join(path, candidate)
    if os.path.isfile(candidate):
        return candidate
    return None


def possible_specs(spec):
    # 4. then maybe it's something exact on PATH - if it was direct lookup implementation no longer counts
    yield spec.str_spec, False
    # 5. or from the spec we can deduce a name on path  that matches
    yield from spec.generate_names()


class PathPythonInfo(PythonInfo):
    """python info from path."""


__all__ = [
    "get_interpreter",
    "Builtin",
    "PathPythonInfo",
]
