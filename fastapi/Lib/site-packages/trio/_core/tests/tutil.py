# Utilities for testing
import asyncio
import gc
import os
import socket as stdlib_socket
import sys
import threading
import warnings
from contextlib import closing, contextmanager
from typing import TYPE_CHECKING

import pytest

# See trio/tests/conftest.py for the other half of this
from trio.tests.conftest import RUN_SLOW

slow = pytest.mark.skipif(not RUN_SLOW, reason="use --run-slow to run slow tests")

# PyPy 7.2 was released with a bug that just never called the async
# generator 'firstiter' hook at all.  This impacts tests of end-of-run
# finalization (nothing gets added to runner.asyncgens) and tests of
# "foreign" async generator behavior (since the firstiter hook is what
# marks the asyncgen as foreign), but most tests of GC-mediated
# finalization still work.
buggy_pypy_asyncgens = (
    not TYPE_CHECKING
    and sys.implementation.name == "pypy"
    and sys.pypy_version_info < (7, 3)
)

try:
    s = stdlib_socket.socket(stdlib_socket.AF_INET6, stdlib_socket.SOCK_STREAM, 0)
except OSError:  # pragma: no cover
    # Some systems don't even support creating an IPv6 socket, let alone
    # binding it. (ex: Linux with 'ipv6.disable=1' in the kernel command line)
    # We don't have any of those in our CI, and there's nothing that gets
    # tested _only_ if can_create_ipv6 = False, so we'll just no-cover this.
    can_create_ipv6 = False
    can_bind_ipv6 = False
else:
    can_create_ipv6 = True
    with s:
        try:
            s.bind(("::1", 0))
        except OSError:
            can_bind_ipv6 = False
        else:
            can_bind_ipv6 = True

creates_ipv6 = pytest.mark.skipif(not can_create_ipv6, reason="need IPv6")
binds_ipv6 = pytest.mark.skipif(not can_bind_ipv6, reason="need IPv6")


def gc_collect_harder():
    # In the test suite we sometimes want to call gc.collect() to make sure
    # that any objects with noisy __del__ methods (e.g. unawaited coroutines)
    # get collected before we continue, so their noise doesn't leak into
    # unrelated tests.
    #
    # On PyPy, coroutine objects (for example) can survive at least 1 round of
    # garbage collection, because executing their __del__ method to print the
    # warning can cause them to be resurrected. So we call collect a few times
    # to make sure.
    for _ in range(4):
        gc.collect()


# Some of our tests need to leak coroutines, and thus trigger the
# "RuntimeWarning: coroutine '...' was never awaited" message. This context
# manager should be used anywhere this happens to hide those messages, because
# when expected they're clutter.
@contextmanager
def ignore_coroutine_never_awaited_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="coroutine '.*' was never awaited")
        try:
            yield
        finally:
            # Make sure to trigger any coroutine __del__ methods now, before
            # we leave the context manager.
            gc_collect_harder()


def _noop(*args, **kwargs):
    pass


if sys.version_info >= (3, 8):

    @contextmanager
    def restore_unraisablehook():
        sys.unraisablehook, prev = sys.__unraisablehook__, sys.unraisablehook
        try:
            yield
        finally:
            sys.unraisablehook = prev

    @contextmanager
    def disable_threading_excepthook():
        if sys.version_info >= (3, 10):
            threading.excepthook, prev = threading.__excepthook__, threading.excepthook
        else:
            threading.excepthook, prev = _noop, threading.excepthook

        try:
            yield
        finally:
            threading.excepthook = prev

else:

    @contextmanager
    def restore_unraisablehook():  # pragma: no cover
        yield

    @contextmanager
    def disable_threading_excepthook():  # pragma: no cover
        yield


# template is like:
#   [1, {2.1, 2.2}, 3] -> matches [1, 2.1, 2.2, 3] or [1, 2.2, 2.1, 3]
def check_sequence_matches(seq, template):
    i = 0
    for pattern in template:
        if not isinstance(pattern, set):
            pattern = {pattern}
        got = set(seq[i : i + len(pattern)])
        assert got == pattern
        i += len(got)


# https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=246350
skip_if_fbsd_pipes_broken = pytest.mark.skipif(
    sys.platform != "win32"  # prevent mypy from complaining about missing uname
    and hasattr(os, "uname")
    and os.uname().sysname == "FreeBSD"
    and os.uname().release[:4] < "12.2",
    reason="hangs on FreeBSD 12.1 and earlier, due to FreeBSD bug #246350",
)


def create_asyncio_future_in_new_loop():
    with closing(asyncio.new_event_loop()) as loop:
        return loop.create_future()
