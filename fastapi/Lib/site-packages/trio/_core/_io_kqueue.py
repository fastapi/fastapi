import errno
import select
import sys
from contextlib import contextmanager
from typing import TYPE_CHECKING

import attr
import outcome

from .. import _core
from ._run import _public
from ._wakeup_socketpair import WakeupSocketpair

assert not TYPE_CHECKING or (sys.platform != "linux" and sys.platform != "win32")


@attr.s(slots=True, eq=False, frozen=True)
class _KqueueStatistics:
    tasks_waiting = attr.ib()
    monitors = attr.ib()
    backend = attr.ib(default="kqueue")


@attr.s(slots=True, eq=False)
class KqueueIOManager:
    _kqueue = attr.ib(factory=select.kqueue)
    # {(ident, filter): Task or UnboundedQueue}
    _registered = attr.ib(factory=dict)
    _force_wakeup = attr.ib(factory=WakeupSocketpair)
    _force_wakeup_fd = attr.ib(default=None)

    def __attrs_post_init__(self):
        force_wakeup_event = select.kevent(
            self._force_wakeup.wakeup_sock, select.KQ_FILTER_READ, select.KQ_EV_ADD
        )
        self._kqueue.control([force_wakeup_event], 0)
        self._force_wakeup_fd = self._force_wakeup.wakeup_sock.fileno()

    def statistics(self):
        tasks_waiting = 0
        monitors = 0
        for receiver in self._registered.values():
            if type(receiver) is _core.Task:
                tasks_waiting += 1
            else:
                monitors += 1
        return _KqueueStatistics(tasks_waiting=tasks_waiting, monitors=monitors)

    def close(self):
        self._kqueue.close()
        self._force_wakeup.close()

    def force_wakeup(self):
        self._force_wakeup.wakeup_thread_and_signal_safe()

    def get_events(self, timeout):
        # max_events must be > 0 or kqueue gets cranky
        # and we generally want this to be strictly larger than the actual
        # number of events we get, so that we can tell that we've gotten
        # all the events in just 1 call.
        max_events = len(self._registered) + 1
        events = []
        while True:
            batch = self._kqueue.control([], max_events, timeout)
            events += batch
            if len(batch) < max_events:
                break
            else:
                timeout = 0
                # and loop back to the start
        return events

    def process_events(self, events):
        for event in events:
            key = (event.ident, event.filter)
            if event.ident == self._force_wakeup_fd:
                self._force_wakeup.drain()
                continue
            receiver = self._registered[key]
            if event.flags & select.KQ_EV_ONESHOT:
                del self._registered[key]
            if type(receiver) is _core.Task:
                _core.reschedule(receiver, outcome.Value(event))
            else:
                receiver.put_nowait(event)

    # kevent registration is complicated -- e.g. aio submission can
    # implicitly perform a EV_ADD, and EVFILT_PROC with NOTE_TRACK will
    # automatically register filters for child processes. So our lowlevel
    # API is *very* low-level: we expose the kqueue itself for adding
    # events or sticking into AIO submission structs, and split waiting
    # off into separate methods. It's your responsibility to make sure
    # that handle_io never receives an event without a corresponding
    # registration! This may be challenging if you want to be careful
    # about e.g. KeyboardInterrupt. Possibly this API could be improved to
    # be more ergonomic...

    @_public
    def current_kqueue(self):
        return self._kqueue

    @contextmanager
    @_public
    def monitor_kevent(self, ident, filter):
        key = (ident, filter)
        if key in self._registered:
            raise _core.BusyResourceError(
                "attempt to register multiple listeners for same ident/filter pair"
            )
        q = _core.UnboundedQueue()
        self._registered[key] = q
        try:
            yield q
        finally:
            del self._registered[key]

    @_public
    async def wait_kevent(self, ident, filter, abort_func):
        key = (ident, filter)
        if key in self._registered:
            raise _core.BusyResourceError(
                "attempt to register multiple listeners for same ident/filter pair"
            )
        self._registered[key] = _core.current_task()

        def abort(raise_cancel):
            r = abort_func(raise_cancel)
            if r is _core.Abort.SUCCEEDED:
                del self._registered[key]
            return r

        return await _core.wait_task_rescheduled(abort)

    async def _wait_common(self, fd, filter):
        if not isinstance(fd, int):
            fd = fd.fileno()
        flags = select.KQ_EV_ADD | select.KQ_EV_ONESHOT
        event = select.kevent(fd, filter, flags)
        self._kqueue.control([event], 0)

        def abort(_):
            event = select.kevent(fd, filter, select.KQ_EV_DELETE)
            try:
                self._kqueue.control([event], 0)
            except OSError as exc:
                # kqueue tracks individual fds (*not* the underlying file
                # object, see _io_epoll.py for a long discussion of why this
                # distinction matters), and automatically deregisters an event
                # if the fd is closed. So if kqueue.control says that it
                # doesn't know about this event, then probably it's because
                # the fd was closed behind our backs. (Too bad we can't ask it
                # to wake us up when this happens, versus discovering it after
                # the fact... oh well, you can't have everything.)
                #
                # FreeBSD reports this using EBADF. macOS uses ENOENT.
                if exc.errno in (errno.EBADF, errno.ENOENT):  # pragma: no branch
                    pass
                else:  # pragma: no cover
                    # As far as we know, this branch can't happen.
                    raise
            return _core.Abort.SUCCEEDED

        await self.wait_kevent(fd, filter, abort)

    @_public
    async def wait_readable(self, fd):
        await self._wait_common(fd, select.KQ_FILTER_READ)

    @_public
    async def wait_writable(self, fd):
        await self._wait_common(fd, select.KQ_FILTER_WRITE)

    @_public
    def notify_closing(self, fd):
        if not isinstance(fd, int):
            fd = fd.fileno()

        for filter in [select.KQ_FILTER_READ, select.KQ_FILTER_WRITE]:
            key = (fd, filter)
            receiver = self._registered.get(key)

            if receiver is None:
                continue

            if type(receiver) is _core.Task:
                event = select.kevent(fd, filter, select.KQ_EV_DELETE)
                self._kqueue.control([event], 0)
                exc = _core.ClosedResourceError("another task closed this fd")
                _core.reschedule(receiver, outcome.Error(exc))
                del self._registered[key]
            else:
                # XX this is an interesting example of a case where being able
                # to close a queue would be useful...
                raise NotImplementedError(
                    "can't close an fd that monitor_kevent is using"
                )
