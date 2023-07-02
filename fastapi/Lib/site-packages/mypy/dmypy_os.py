from __future__ import annotations

import sys
from typing import Any, Callable

if sys.platform == "win32":
    import ctypes
    import subprocess
    from ctypes.wintypes import DWORD, HANDLE

    PROCESS_QUERY_LIMITED_INFORMATION = ctypes.c_ulong(0x1000)

    kernel32 = ctypes.windll.kernel32
    OpenProcess: Callable[[DWORD, int, int], HANDLE] = kernel32.OpenProcess
    GetExitCodeProcess: Callable[[HANDLE, Any], int] = kernel32.GetExitCodeProcess
else:
    import os
    import signal


def alive(pid: int) -> bool:
    """Is the process alive?"""
    if sys.platform == "win32":
        # why can't anything be easy...
        status = DWORD()
        handle = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
        GetExitCodeProcess(handle, ctypes.byref(status))
        return status.value == 259  # STILL_ACTIVE
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True


def kill(pid: int) -> None:
    """Kill the process."""
    if sys.platform == "win32":
        subprocess.check_output(f"taskkill /pid {pid} /f /t")
    else:
        os.kill(pid, signal.SIGKILL)
