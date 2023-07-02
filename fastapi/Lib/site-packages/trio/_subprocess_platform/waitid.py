import errno
import math
import os
import sys

from .. import _core, _subprocess
from .._sync import CapacityLimiter, Event
from .._threads import to_thread_run_sync

try:
    from os import waitid

    def sync_wait_reapable(pid):
        waitid(os.P_PID, pid, os.WEXITED | os.WNOWAIT)

except ImportError:
    # pypy doesn't define os.waitid so we need to pull it out ourselves
    # using cffi: https://bitbucket.org/pypy/pypy/issues/2922/
    import cffi

    waitid_ffi = cffi.FFI()

    # Believe it or not, siginfo_t starts with fields in the
    # same layout on both Linux and Darwin. The Linux structure
    # is bigger so that's what we use to size `pad`; while
    # there are a few extra fields in there, most of it is
    # true padding which would not be written by the syscall.
    waitid_ffi.cdef(
        """
typedef struct siginfo_s {
    int si_signo;
    int si_errno;
    int si_code;
    int si_pid;
    int si_uid;
    int si_status;
    int pad[26];
} siginfo_t;
int waitid(int idtype, int id, siginfo_t* result, int options);
"""
    )
    waitid = waitid_ffi.dlopen(None).waitid

    def sync_wait_reapable(pid):
        P_PID = 1
        WEXITED = 0x00000004
        if sys.platform == "darwin":  # pragma: no cover
            # waitid() is not exposed on Python on Darwin but does
            # work through CFFI; note that we typically won't get
            # here since Darwin also defines kqueue
            WNOWAIT = 0x00000020
        else:
            WNOWAIT = 0x01000000
        result = waitid_ffi.new("siginfo_t *")
        while waitid(P_PID, pid, result, WEXITED | WNOWAIT) < 0:
            got_errno = waitid_ffi.errno
            if got_errno == errno.EINTR:
                continue
            raise OSError(got_errno, os.strerror(got_errno))


# adapted from
# https://github.com/python-trio/trio/issues/4#issuecomment-398967572

waitid_limiter = CapacityLimiter(math.inf)


async def _waitid_system_task(pid: int, event: Event) -> None:
    """Spawn a thread that waits for ``pid`` to exit, then wake any tasks
    that were waiting on it.
    """
    # cancellable=True: if this task is cancelled, then we abandon the
    # thread to keep running waitpid in the background. Since this is
    # always run as a system task, this will only happen if the whole
    # call to trio.run is shutting down.

    try:
        await to_thread_run_sync(
            sync_wait_reapable, pid, cancellable=True, limiter=waitid_limiter
        )
    except OSError:
        # If waitid fails, waitpid will fail too, so it still makes
        # sense to wake up the callers of wait_process_exiting(). The
        # most likely reason for this error in practice is a child
        # exiting when wait() is not possible because SIGCHLD is
        # ignored.
        pass
    finally:
        event.set()


async def wait_child_exiting(process: "_subprocess.Process") -> None:
    # Logic of this function:
    # - The first time we get called, we create an Event and start
    #   an instance of _waitid_system_task that will set the Event
    #   when waitid() completes. If that Event is set before
    #   we get cancelled, we're good.
    # - Otherwise, a following call after the cancellation must
    #   reuse the Event created during the first call, lest we
    #   create an arbitrary number of threads waiting on the same
    #   process.

    if process._wait_for_exit_data is None:
        process._wait_for_exit_data = event = Event()  # type: ignore
        _core.spawn_system_task(_waitid_system_task, process.pid, event)
    assert isinstance(process._wait_for_exit_data, Event)
    await process._wait_for_exit_data.wait()
