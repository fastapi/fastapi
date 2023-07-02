import sys

if sys.version_info >= (3, 11):
    __all__ = (
        "BrokenBarrierError",
        "CancelledError",
        "InvalidStateError",
        "TimeoutError",
        "IncompleteReadError",
        "LimitOverrunError",
        "SendfileNotAvailableError",
    )
else:
    __all__ = (
        "CancelledError",
        "InvalidStateError",
        "TimeoutError",
        "IncompleteReadError",
        "LimitOverrunError",
        "SendfileNotAvailableError",
    )

class CancelledError(BaseException): ...
class TimeoutError(Exception): ...
class InvalidStateError(Exception): ...
class SendfileNotAvailableError(RuntimeError): ...

class IncompleteReadError(EOFError):
    expected: int | None
    partial: bytes
    def __init__(self, partial: bytes, expected: int | None) -> None: ...

class LimitOverrunError(Exception):
    consumed: int
    def __init__(self, message: str, consumed: int) -> None: ...

if sys.version_info >= (3, 11):
    class BrokenBarrierError(RuntimeError): ...
