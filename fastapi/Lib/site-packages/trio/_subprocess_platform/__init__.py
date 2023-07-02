# Platform-specific subprocess bits'n'pieces.

import os
import sys
from typing import TYPE_CHECKING, Optional, Tuple

import trio

from .. import _core, _subprocess
from .._abc import ReceiveStream, SendStream

_wait_child_exiting_error: Optional[ImportError] = None
_create_child_pipe_error: Optional[ImportError] = None


if TYPE_CHECKING:
    # internal types for the pipe representations used in type checking only
    class ClosableSendStream(SendStream):
        def close(self) -> None:
            ...

    class ClosableReceiveStream(ReceiveStream):
        def close(self) -> None:
            ...


# Fallback versions of the functions provided -- implementations
# per OS are imported atop these at the bottom of the module.
async def wait_child_exiting(process: "_subprocess.Process") -> None:
    """Block until the child process managed by ``process`` is exiting.

    It is invalid to call this function if the process has already
    been waited on; that is, ``process.returncode`` must be None.

    When this function returns, it indicates that a call to
    :meth:`subprocess.Popen.wait` will immediately be able to
    return the process's exit status. The actual exit status is not
    consumed by this call, since :class:`~subprocess.Popen` wants
    to be able to do that itself.
    """
    raise NotImplementedError from _wait_child_exiting_error  # pragma: no cover


def create_pipe_to_child_stdin() -> Tuple["ClosableSendStream", int]:
    """Create a new pipe suitable for sending data from this
    process to the standard input of a child we're about to spawn.

    Returns:
      A pair ``(trio_end, subprocess_end)`` where ``trio_end`` is a
      :class:`~trio.abc.SendStream` and ``subprocess_end`` is
      something suitable for passing as the ``stdin`` argument of
      :class:`subprocess.Popen`.
    """
    raise NotImplementedError from _create_child_pipe_error  # pragma: no cover


def create_pipe_from_child_output() -> Tuple["ClosableReceiveStream", int]:
    """Create a new pipe suitable for receiving data into this
    process from the standard output or error stream of a child
    we're about to spawn.

    Returns:
      A pair ``(trio_end, subprocess_end)`` where ``trio_end`` is a
      :class:`~trio.abc.ReceiveStream` and ``subprocess_end`` is
      something suitable for passing as the ``stdin`` argument of
      :class:`subprocess.Popen`.
    """
    raise NotImplementedError from _create_child_pipe_error  # pragma: no cover


try:
    if sys.platform == "win32":
        from .windows import wait_child_exiting  # noqa: F811
    elif sys.platform != "linux" and (TYPE_CHECKING or hasattr(_core, "wait_kevent")):
        from .kqueue import wait_child_exiting  # noqa: F811
    else:
        from .waitid import wait_child_exiting  # noqa: F811
except ImportError as ex:  # pragma: no cover
    _wait_child_exiting_error = ex

try:
    if TYPE_CHECKING:
        # Not worth type checking these definitions
        pass

    elif os.name == "posix":

        def create_pipe_to_child_stdin():  # noqa: F811
            rfd, wfd = os.pipe()
            return trio.lowlevel.FdStream(wfd), rfd

        def create_pipe_from_child_output():  # noqa: F811
            rfd, wfd = os.pipe()
            return trio.lowlevel.FdStream(rfd), wfd

    elif os.name == "nt":
        import msvcrt

        # This isn't exported or documented, but it's also not
        # underscore-prefixed, and seems kosher to use. The asyncio docs
        # for 3.5 included an example that imported socketpair from
        # windows_utils (before socket.socketpair existed on Windows), and
        # when asyncio.windows_utils.socketpair was removed in 3.7, the
        # removal was mentioned in the release notes.
        from asyncio.windows_utils import pipe as windows_pipe

        from .._windows_pipes import PipeReceiveStream, PipeSendStream

        def create_pipe_to_child_stdin():  # noqa: F811
            # for stdin, we want the write end (our end) to use overlapped I/O
            rh, wh = windows_pipe(overlapped=(False, True))
            return PipeSendStream(wh), msvcrt.open_osfhandle(rh, os.O_RDONLY)

        def create_pipe_from_child_output():  # noqa: F811
            # for stdout/err, it's the read end that's overlapped
            rh, wh = windows_pipe(overlapped=(True, False))
            return PipeReceiveStream(rh), msvcrt.open_osfhandle(wh, 0)

    else:  # pragma: no cover
        raise ImportError("pipes not implemented on this platform")

except ImportError as ex:  # pragma: no cover
    _create_child_pipe_error = ex
