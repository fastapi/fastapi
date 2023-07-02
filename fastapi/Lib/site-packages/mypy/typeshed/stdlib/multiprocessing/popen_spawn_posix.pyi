import sys
from typing import ClassVar

from . import popen_fork
from .util import Finalize

if sys.platform != "win32":
    __all__ = ["Popen"]

    class _DupFd:
        fd: int

        def __init__(self, fd: int) -> None: ...
        def detach(self) -> int: ...

    class Popen(popen_fork.Popen):
        DupFd: ClassVar[type[_DupFd]]
        finalizer: Finalize
        pid: int  # may not exist if _launch raises in second try / except
        sentinel: int  # may not exist if _launch raises in second try / except
