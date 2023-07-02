import signal
from collections import OrderedDict
from contextlib import contextmanager

import trio

from ._util import ConflictDetector, is_main_thread, signal_raise

# Discussion of signal handling strategies:
#
# - On Windows signals barely exist. There are no options; signal handlers are
#   the only available API.
#
# - On Linux signalfd is arguably the natural way. Semantics: signalfd acts as
#   an *alternative* signal delivery mechanism. The way you use it is to mask
#   out the relevant signals process-wide (so that they don't get delivered
#   the normal way), and then when you read from signalfd that actually counts
#   as delivering it (despite the mask). The problem with this is that we
#   don't have any reliable way to mask out signals process-wide -- the only
#   way to do that in Python is to call pthread_sigmask from the main thread
#   *before starting any other threads*, and as a library we can't really
#   impose that, and the failure mode is annoying (signals get delivered via
#   signal handlers whether we want them to or not).
#
# - on macOS/*BSD, kqueue is the natural way. Semantics: kqueue acts as an
#   *extra* signal delivery mechanism. Signals are delivered the normal
#   way, *and* are delivered to kqueue. So you want to set them to SIG_IGN so
#   that they don't end up pending forever (I guess?). I can't find any actual
#   docs on how masking and EVFILT_SIGNAL interact. I did see someone note
#   that if a signal is pending when the kqueue filter is added then you
#   *don't* get notified of that, which makes sense. But still, we have to
#   manipulate signal state (e.g. setting SIG_IGN) which as far as Python is
#   concerned means we have to do this from the main thread.
#
# So in summary, there don't seem to be any compelling advantages to using the
# platform-native signal notification systems; they're kinda nice, but it's
# simpler to implement the naive signal-handler-based system once and be
# done. (The big advantage would be if there were a reliable way to monitor
# for SIGCHLD from outside the main thread and without interfering with other
# libraries that also want to monitor for SIGCHLD. But there isn't. I guess
# kqueue might give us that, but in kqueue we don't need it, because kqueue
# can directly monitor for child process state changes.)


@contextmanager
def _signal_handler(signals, handler):
    original_handlers = {}
    try:
        for signum in set(signals):
            original_handlers[signum] = signal.signal(signum, handler)
        yield
    finally:
        for signum, original_handler in original_handlers.items():
            signal.signal(signum, original_handler)


class SignalReceiver:
    def __init__(self):
        # {signal num: None}
        self._pending = OrderedDict()
        self._lot = trio.lowlevel.ParkingLot()
        self._conflict_detector = ConflictDetector(
            "only one task can iterate on a signal receiver at a time"
        )
        self._closed = False

    def _add(self, signum):
        if self._closed:
            signal_raise(signum)
        else:
            self._pending[signum] = None
            self._lot.unpark()

    def _redeliver_remaining(self):
        # First make sure that any signals still in the delivery pipeline will
        # get redelivered
        self._closed = True

        # And then redeliver any that are sitting in pending. This is done
        # using a weird recursive construct to make sure we process everything
        # even if some of the handlers raise exceptions.
        def deliver_next():
            if self._pending:
                signum, _ = self._pending.popitem(last=False)
                try:
                    signal_raise(signum)
                finally:
                    deliver_next()

        deliver_next()

    # Helper for tests, not public or otherwise used
    def _pending_signal_count(self):
        return len(self._pending)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._closed:
            raise RuntimeError("open_signal_receiver block already exited")
        # In principle it would be possible to support multiple concurrent
        # calls to __anext__, but doing it without race conditions is quite
        # tricky, and there doesn't seem to be any point in trying.
        with self._conflict_detector:
            if not self._pending:
                await self._lot.park()
            else:
                await trio.lowlevel.checkpoint()
            signum, _ = self._pending.popitem(last=False)
            return signum


@contextmanager
def open_signal_receiver(*signals):
    """A context manager for catching signals.

    Entering this context manager starts listening for the given signals and
    returns an async iterator; exiting the context manager stops listening.

    The async iterator blocks until a signal arrives, and then yields it.

    Note that if you leave the ``with`` block while the iterator has
    unextracted signals still pending inside it, then they will be
    re-delivered using Python's regular signal handling logic. This avoids a
    race condition when signals arrives just before we exit the ``with``
    block.

    Args:
      signals: the signals to listen for.

    Raises:
      TypeError: if no signals were provided.

      RuntimeError: if you try to use this anywhere except Python's main
          thread. (This is a Python limitation.)

    Example:

      A common convention for Unix daemons is that they should reload their
      configuration when they receive a ``SIGHUP``. Here's a sketch of what
      that might look like using :func:`open_signal_receiver`::

         with trio.open_signal_receiver(signal.SIGHUP) as signal_aiter:
             async for signum in signal_aiter:
                 assert signum == signal.SIGHUP
                 reload_configuration()

    """
    if not signals:
        raise TypeError("No signals were provided")

    if not is_main_thread():
        raise RuntimeError(
            "Sorry, open_signal_receiver is only possible when running in "
            "Python interpreter's main thread"
        )
    token = trio.lowlevel.current_trio_token()
    queue = SignalReceiver()

    def handler(signum, _):
        token.run_sync_soon(queue._add, signum, idempotent=True)

    try:
        with _signal_handler(signals, handler):
            yield queue
    finally:
        queue._redeliver_remaining()
