import os
import subprocess
import sys
import sysconfig
from pathlib import Path


def find_ruff_bin() -> Path:
    """Return the ruff binary path."""

    ruff_exe = "ruff" + sysconfig.get_config_var("EXE")

    path = Path(sysconfig.get_path("scripts")) / ruff_exe
    if path.is_file():
        return path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    path = Path(sysconfig.get_path("scripts", scheme=user_scheme)) / ruff_exe
    if path.is_file():
        return path

    raise FileNotFoundError(path)


if __name__ == "__main__":
    ruff = find_ruff_bin()
    # Passing a path-like to `subprocess.run()` on windows is only supported in 3.8+,
    # but we also support 3.7
    completed_process = subprocess.run([os.fsdecode(ruff), *sys.argv[1:]])
    sys.exit(completed_process.returncode)
