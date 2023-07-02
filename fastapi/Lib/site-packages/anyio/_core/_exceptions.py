from __future__ import annotations

from traceback import format_exception


class BrokenResourceError(Exception):
    """
    Raised when trying to use a resource that has been rendered unusable due to external causes
    (e.g. a send stream whose peer has disconnected).
    """


class BrokenWorkerProcess(Exception):
    """
    Raised by :func:`run_sync_in_process` if the worker process terminates abruptly or otherwise
    misbehaves.
    """


class BusyResourceError(Exception):
    """Raised when two tasks are trying to read from or write to the same resource concurrently."""

    def __init__(self, action: str):
        super().__init__(f"Another task is already {action} this resource")


class ClosedResourceError(Exception):
    """Raised when trying to use a resource that has been closed."""


class DelimiterNotFound(Exception):
    """
    Raised during :meth:`~anyio.streams.buffered.BufferedByteReceiveStream.receive_until` if the
    maximum number of bytes has been read without the delimiter being found.
    """

    def __init__(self, max_bytes: int) -> None:
        super().__init__(
            f"The delimiter was not found among the first {max_bytes} bytes"
        )


class EndOfStream(Exception):
    """Raised when trying to read from a stream that has been closed from the other end."""


class ExceptionGroup(BaseException):
    """
    Raised when multiple exceptions have been raised in a task group.

    :var ~typing.Sequence[BaseException] exceptions: the sequence of exceptions raised together
    """

    SEPARATOR = "----------------------------\n"

    exceptions: list[BaseException]

    def __str__(self) -> str:
        tracebacks = [
            "".join(format_exception(type(exc), exc, exc.__traceback__))
            for exc in self.exceptions
        ]
        return (
            f"{len(self.exceptions)} exceptions were raised in the task group:\n"
            f"{self.SEPARATOR}{self.SEPARATOR.join(tracebacks)}"
        )

    def __repr__(self) -> str:
        exception_reprs = ", ".join(repr(exc) for exc in self.exceptions)
        return f"<{self.__class__.__name__}: {exception_reprs}>"


class IncompleteRead(Exception):
    """
    Raised during :meth:`~anyio.streams.buffered.BufferedByteReceiveStream.receive_exactly` or
    :meth:`~anyio.streams.buffered.BufferedByteReceiveStream.receive_until` if the
    connection is closed before the requested amount of bytes has been read.
    """

    def __init__(self) -> None:
        super().__init__(
            "The stream was closed before the read operation could be completed"
        )


class TypedAttributeLookupError(LookupError):
    """
    Raised by :meth:`~anyio.TypedAttributeProvider.extra` when the given typed attribute is not
    found and no default value has been given.
    """


class WouldBlock(Exception):
    """Raised by ``X_nowait`` functions if ``X()`` would block."""
