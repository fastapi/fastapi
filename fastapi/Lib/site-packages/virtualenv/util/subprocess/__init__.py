from __future__ import annotations

import subprocess

CREATE_NO_WINDOW = 0x80000000


def run_cmd(cmd):
    try:
        process = subprocess.Popen(
            cmd,  # noqa: S603
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        out, err = process.communicate()  # input disabled
        code = process.returncode
    except OSError as error:
        code, out, err = error.errno, "", error.strerror
        if code == 2 and "file" in err:  # noqa: PLR2004
            err = str(error)  # FileNotFoundError in Python >= 3.3
    return code, out, err


__all__ = (
    "run_cmd",
    "CREATE_NO_WINDOW",
)
