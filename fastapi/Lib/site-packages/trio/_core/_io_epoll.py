import select
import sys
from collections import defaultdict
from typing import TYPE_CHECKING, Dict

import attr

from .. import _core
from ._io_common import wake_all
from ._run import _public
from ._wakeup_socketpair import WakeupSocketpair

assert not TYPE_CHECKING or sys.platform == "linux"


@attr.s(slots=True, eq=False, frozen=True)
class _EpollStatistics:
    tasks_waiting_read = attr.ib()
    tasks_waiting_write = attr.ib()
    backend = attr.ib(default="epoll")


# Some facts about epoll
# ----------------------
#
# Internally, an epoll object is sort of like a WeakKeyDictionary where the
# keys are tuples of (fd number, file object). When you call epoll_ctl, you
# pass in an fd; that gets converted to an (fd number, file object) tuple by
# looking up the fd in the process's fd table at the time of the call. When an
# event happens on the file object, epoll_wait drops the file object part, and
# just returns the fd number in its event. So from the outside it looks like
# it's keeping a table of fds, but really it's a bit more complicated. This
# has some subtle consequences.
#
# In general, file objects inside the kernel are reference counted. Each entry
# in a process's fd table holds a strong reference to the corresponding file
# object, and most operations that use file objects take a temporary strong
# reference while they're working. So when you call close() on an fd, that
# might or might not cause the file object to be deallocated -- it depends on
# whether there are any other references to that file object. Some common ways
# this can happen:
#
# - after calling dup(), you have two fds in the same process referring to the
#   same file object. Even if you close one fd (= remove that entry from the
#   fd table), the file object will be kept alive by the other fd.
# - when calling fork(), the child inherits a copy of the parent's fd table,
#   so all the file objects get another reference. (But if the fork() is
#   followed by exec(), then all of the child's fds that have the CLOEXEC flag
#   set will be closed at that point.)
# - most syscalls that work on fds take a strong reference to the underlying
#   file object while they're using it. So there's one thread blocked in
#   read(fd), and then another thread calls close() on the last fd referring
#   to that object, the underlying file won't actually be closed until
#   after read() returns.
#
# However, epoll does *not* take a reference to any of the file objects in its
# interest set (that's what makes it similar to a WeakKeyDictionary). File
# objects inside an epoll interest set will be deallocated if all *other*
# references to them are closed. And when that happens, the epoll object will
# automatically deregister that file object and stop reporting events on it.
# So that's quite handy.
#
# But, what happens if we do this?
#
#   fd1 = open(...)
#   epoll_ctl(EPOLL_CTL_ADD, fd1, ...)
#   fd2 = dup(fd1)
#   close(fd1)
#
# In this case, the dup() keeps the underlying file object alive, so it
# remains registered in the epoll object's interest set, as the tuple (fd1,
# file object). But, fd1 no longer refers to this file object! You might think
# there was some magic to handle this, but unfortunately no; the consequences
# are totally predictable from what I said above:
#
# If any events occur on the file object, then epoll will report them as
# happening on fd1, even though that doesn't make sense.
#
# Perhaps we would like to deregister fd1 to stop getting nonsensical events.
# But how? When we call epoll_ctl, we have to pass an fd number, which will
# get expanded to an (fd number, file object) tuple. We can't pass fd1,
# because when epoll_ctl tries to look it up, it won't find our file object.
# And we can't pass fd2, because that will get expanded to (fd2, file object),
# which is a different lookup key. In fact, it's *impossible* to de-register
# this fd!
#
# We could even have fd1 get assigned to another file object, and then we can
# have multiple keys registered simultaneously using the same fd number, like:
# (fd1, file object 1), (fd1, file object 2). And if events happen on either
# file object, then epoll will happily report that something happened to
# "fd1".
#
# Now here's what makes this especially nasty: suppose the old file object
# becomes, say, readable. That means that every time we call epoll_wait, it
# will return immediately to tell us that "fd1" is readable. Normally, we
# would handle this by de-registering fd1, waking up the corresponding call to
# wait_readable, then the user will call read() or recv() or something, and
# we're fine. But if this happens on a stale fd where we can't remove the
# registration, then we might get stuck in a state where epoll_wait *always*
# returns immediately, so our event loop becomes unable to sleep, and now our
# program is burning 100% of the CPU doing nothing, with no way out.
#
#
# What does this mean for Trio?
# -----------------------------
#
# Since we don't control the user's code, we have no way to guarantee that we
# don't get stuck with stale fd's in our epoll interest set. For example, a
# user could call wait_readable(fd) in one task, and then while that's
# running, they might close(fd) from another task. In this situation, they're
# *supposed* to call notify_closing(fd) to let us know what's happening, so we
# can interrupt the wait_readable() call and avoid getting into this mess. And
# that's the only thing that can possibly work correctly in all cases. But
# sometimes user code has bugs. So if this does happen, we'd like to degrade
# gracefully, and survive without corrupting Trio's internal state or
# otherwise causing the whole program to explode messily.
#
# Our solution: we always use EPOLLONESHOT. This way, we might get *one*
# spurious event on a stale fd, but then epoll will automatically silence it
# until we explicitly say that we want more events... and if we have a stale
# fd, then we actually can't re-enable it! So we can't get stuck in an
# infinite busy-loop. If there's a stale fd hanging around, then it might
# cause a spurious `BusyResourceError`, or cause one wait_* call to return
# before it should have... but in general, the wait_* functions are allowed to
# have some spurious wakeups; the user code will just attempt the operation,
# get EWOULDBLOCK, and call wait_* again. And the program as a whole will
# survive, any exceptions will propagate, etc.
#
# As a bonus, EPOLLONESHOT also saves us having to explicitly deregister fds
# on the normal wakeup path, so it's a bit more efficient in general.
#
# However, EPOLLONESHOT has a few trade-offs to consider:
#
# First, you can't combine EPOLLONESHOT with EPOLLEXCLUSIVE. This is a bit sad
# in one somewhat rare case: if you have a multi-process server where a group
# of processes all share the same listening socket, then EPOLLEXCLUSIVE can be
# used to avoid "thundering herd" problems when a new connection comes in. But
# this isn't too bad. It's not clear if EPOLLEXCLUSIVE even works for us
# anyway:
#
#   https://stackoverflow.com/questions/41582560/how-does-epolls-epollexclusive-mode-interact-with-level-triggering
#
# And it's not clear that EPOLLEXCLUSIVE is a great approach either:
#
#   https://blog.cloudflare.com/the-sad-state-of-linux-socket-balancing/
#
# And if we do need to support this, we could always add support through some
# more-specialized API in the future. So this isn't a blocker to using
# EPOLLONESHOT.
#
# Second, EPOLLONESHOT does not actually *deregister* the fd after delivering
# an event (EPOLL_CTL_DEL). Instead, it keeps the fd registered, but
# effectively does an EPOLL_CTL_MOD to set the fd's interest flags to
# all-zeros. So we could still end up with an fd hanging around in the
# interest set for a long time, even if we're not using it.
#
# Fortunately, this isn't a problem, because it's only a weak reference – if
# we have a stale fd that's been silenced by EPOLLONESHOT, then it wastes a
# tiny bit of kernel memory remembering this fd that can never be revived, but
# when the underlying file object is eventually closed, that memory will be
# reclaimed. So that's OK.
#
# The other issue is that when someone calls wait_*, using EPOLLONESHOT means
# that if we have ever waited for this fd before, we have to use EPOLL_CTL_MOD
# to re-enable it; but if it's a new fd, we have to use EPOLL_CTL_ADD. How do
# we know which one to use? There's no reasonable way to track which fds are
# currently registered -- remember, we're assuming the user might have gone
# and rearranged their fds without telling us!
#
# Fortunately, this also has a simple solution: if we wait on a socket or
# other fd once, then we'll probably wait on it lots of times. And the epoll
# object itself knows which fds it already has registered. So when an fd comes
# in, we optimistically assume that it's been waited on before, and try doing
# EPOLL_CTL_MOD. And if that fails with an ENOENT error, then we try again
# with EPOLL_CTL_ADD.
#
# So that's why this code is the way it is. And now you know more than you
# wanted to about how epoll works.


@attr.s(slots=True, eq=False)
class EpollWaiters:
    read_task = attr.ib(default=None)
    write_task = attr.ib(default=None)
    current_flags = attr.ib(default=0)


@attr.s(slots=True, eq=False, hash=False)
class EpollIOManager:
    _epoll = attr.ib(factory=select.epoll)
    # {fd: EpollWaiters}
    _registered = attr.ib(
        factory=lambda: defaultdict(EpollWaiters), type=Dict[int, EpollWaiters]
    )
    _force_wakeup = attr.ib(factory=WakeupSocketpair)
    _force_wakeup_fd = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._epoll.register(self._force_wakeup.wakeup_sock, select.EPOLLIN)
        self._force_wakeup_fd = self._force_wakeup.wakeup_sock.fileno()

    def statistics(self):
        tasks_waiting_read = 0
        tasks_waiting_write = 0
        for waiter in self._registered.values():
            if waiter.read_task is not None:
                tasks_waiting_read += 1
            if waiter.write_task is not None:
                tasks_waiting_write += 1
        return _EpollStatistics(
            tasks_waiting_read=tasks_waiting_read,
            tasks_waiting_write=tasks_waiting_write,
        )

    def close(self):
        self._epoll.close()
        self._force_wakeup.close()

    def force_wakeup(self):
        self._force_wakeup.wakeup_thread_and_signal_safe()

    # Return value must be False-y IFF the timeout expired, NOT if any I/O
    # happened or force_wakeup was called. Otherwise it can be anything; gets
    # passed straight through to process_events.
    def get_events(self, timeout):
        # max_events must be > 0 or epoll gets cranky
        # accessing self._registered from a thread looks dangerous, but it's
        # OK because it doesn't matter if our value is a little bit off.
        max_events = max(1, len(self._registered))
        return self._epoll.poll(timeout, max_events)

    def process_events(self, events):
        for fd, flags in events:
            if fd == self._force_wakeup_fd:
                self._force_wakeup.drain()
                continue
            waiters = self._registered[fd]
            # EPOLLONESHOT always clears the flags when an event is delivered
            waiters.current_flags = 0
            # Clever hack stolen from selectors.EpollSelector: an event
            # with EPOLLHUP or EPOLLERR flags wakes both readers and
            # writers.
            if flags & ~select.EPOLLIN and waiters.write_task is not None:
                _core.reschedule(waiters.write_task)
                waiters.write_task = None
            if flags & ~select.EPOLLOUT and waiters.read_task is not None:
                _core.reschedule(waiters.read_task)
                waiters.read_task = None
            self._update_registrations(fd)

    def _update_registrations(self, fd):
        waiters = self._registered[fd]
        wanted_flags = 0
        if waiters.read_task is not None:
            wanted_flags |= select.EPOLLIN
        if waiters.write_task is not None:
            wanted_flags |= select.EPOLLOUT
        if wanted_flags != waiters.current_flags:
            try:
                try:
                    # First try EPOLL_CTL_MOD
                    self._epoll.modify(fd, wanted_flags | select.EPOLLONESHOT)
                except OSError:
                    # If that fails, it might be a new fd; try EPOLL_CTL_ADD
                    self._epoll.register(fd, wanted_flags | select.EPOLLONESHOT)
                waiters.current_flags = wanted_flags
            except OSError as exc:
                # If everything fails, probably it's a bad fd, e.g. because
                # the fd was closed behind our back. In this case we don't
                # want to try to unregister the fd, because that will probably
                # fail too. Just clear our state and wake everyone up.
                del self._registered[fd]
                # This could raise (in case we're calling this inside one of
                # the to-be-woken tasks), so we have to do it last.
                wake_all(waiters, exc)
                return
        if not wanted_flags:
            del self._registered[fd]

    async def _epoll_wait(self, fd, attr_name):
        if not isinstance(fd, int):
            fd = fd.fileno()
        waiters = self._registered[fd]
        if getattr(waiters, attr_name) is not None:
            raise _core.BusyResourceError(
                "another task is already reading / writing this fd"
            )
        setattr(waiters, attr_name, _core.current_task())
        self._update_registrations(fd)

        def abort(_):
            setattr(waiters, attr_name, None)
            self._update_registrations(fd)
            return _core.Abort.SUCCEEDED

        await _core.wait_task_rescheduled(abort)

    @_public
    async def wait_readable(self, fd):
        await self._epoll_wait(fd, "read_task")

    @_public
    async def wait_writable(self, fd):
        await self._epoll_wait(fd, "write_task")

    @_public
    def notify_closing(self, fd):
        if not isinstance(fd, int):
            fd = fd.fileno()
        wake_all(
            self._registered[fd],
            _core.ClosedResourceError("another task closed this fd"),
        )
        del self._registered[fd]
        try:
            self._epoll.unregister(fd)
        except (OSError, ValueError):
            pass
