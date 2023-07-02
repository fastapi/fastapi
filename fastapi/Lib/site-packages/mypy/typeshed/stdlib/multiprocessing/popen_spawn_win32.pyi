import sys
from multiprocessing.process import BaseProcess
from typing import ClassVar

from .util import Finalize

if sys.platform == "win32":
    __all__ = ["Popen"]

    TERMINATE: int
    WINEXE: bool
    WINSERVICE: bool
    WINENV: bool

    class Popen:
        finalizer: Finalize
        method: ClassVar[str]
        pid: int
        returncode: int | None
        sentinel: int

        def __init__(self, process_obj: BaseProcess) -> None: ...
        def duplicate_for_child(self, handle: int) -> int: ...
        def wait(self, timeout: float | None = None) -> int | None: ...
        def poll(self) -> int | None: ...
        def terminate(self) -> None: ...

        kill = terminate

        def close(self) -> None: ...
