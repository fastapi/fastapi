"""Mypyc command-line tool.

Usage:

    $ mypyc foo.py [...]
    $ python3 -c 'import foo'  # Uses compiled 'foo'


This is just a thin wrapper that generates a setup.py file that uses
mypycify, suitable for prototyping and testing.
"""

from __future__ import annotations

import os
import os.path
import subprocess
import sys

base_path = os.path.join(os.path.dirname(__file__), "..")

setup_format = """\
from setuptools import setup
from mypyc.build import mypycify

setup(name='mypyc_output',
      ext_modules=mypycify({}, opt_level="{}", debug_level="{}"),
)
"""


def main() -> None:
    build_dir = "build"  # can this be overridden??
    try:
        os.mkdir(build_dir)
    except FileExistsError:
        pass

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    debug_level = os.getenv("MYPYC_DEBUG_LEVEL", "1")

    setup_file = os.path.join(build_dir, "setup.py")
    with open(setup_file, "w") as f:
        f.write(setup_format.format(sys.argv[1:], opt_level, debug_level))

    # We don't use run_setup (like we do in the test suite) because it throws
    # away the error code from distutils, and we don't care about the slight
    # performance loss here.
    env = os.environ.copy()
    base_path = os.path.join(os.path.dirname(__file__), "..")
    env["PYTHONPATH"] = base_path + os.pathsep + env.get("PYTHONPATH", "")
    cmd = subprocess.run(
        [sys.executable, setup_file, "build_ext", "--inplace"], env=env
    )
    sys.exit(cmd.returncode)


if __name__ == "__main__":
    main()
