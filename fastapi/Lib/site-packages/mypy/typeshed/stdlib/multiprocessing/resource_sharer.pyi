import sys
from socket import socket

__all__ = ["stop"]

if sys.platform == "win32":
    __all__ += ["DupSocket"]

    class DupSocket:
        def __init__(self, sock: socket) -> None: ...
        def detach(self) -> socket: ...

else:
    __all__ += ["DupFd"]

    class DupFd:
        def __init__(self, fd: int) -> None: ...
        def detach(self) -> int: ...

def stop(timeout: float | None = None) -> None: ...
