import threading
from collections import deque

import attr

from .. import _core
from .._util import NoPublicConstructor
from ._wakeup_socketpair import WakeupSocketpair


@attr.s(slots=True)
class EntryQueue:
    # This used to use a queue.Queue. but that was broken, because Queues are
    # implemented in Python, and not reentrant -- so it was thread-safe, but
    # not signal-safe. deque is implemented in C, so each operation is atomic
    # WRT threads (and this is guaranteed in the docs), AND each operation is
    # atomic WRT signal delivery (signal handlers can run on either side, but
    # not *during* a deque operation). dict makes similar guarantees - and
    # it's even ordered!
    queue = attr.ib(factory=deque)
    idempotent_queue = attr.ib(factory=dict)

    wakeup = attr.ib(factory=WakeupSocketpair)
    done = attr.ib(default=False)
    # Must be a reentrant lock, because it's acquired from signal handlers.
    # RLock is signal-safe as of cpython 3.2. NB that this does mean that the
    # lock is effectively *disabled* when we enter from signal context. The
    # way we use the lock this is OK though, because when
    # run_sync_soon is called from a signal it's atomic WRT the
    # main thread -- it just might happen at some inconvenient place. But if
    # you look at the one place where the main thread holds the lock, it's
    # just to make 1 assignment, so that's atomic WRT a signal anyway.
    lock = attr.ib(factory=threading.RLock)

    async def task(self):
        assert _core.currently_ki_protected()
        # RLock has two implementations: a signal-safe version in _thread, and
        # and signal-UNsafe version in threading. We need the signal safe
        # version. Python 3.2 and later should always use this anyway, but,
        # since the symptoms if this goes wrong are just "weird rare
        # deadlocks", then let's make a little check.
        # See:
        #     https://bugs.python.org/issue13697#msg237140
        assert self.lock.__class__.__module__ == "_thread"

        def run_cb(job):
            # We run this with KI protection enabled; it's the callback's
            # job to disable it if it wants it disabled. Exceptions are
            # treated like system task exceptions (i.e., converted into
            # TrioInternalError and cause everything to shut down).
            sync_fn, args = job
            try:
                sync_fn(*args)
            except BaseException as exc:

                async def kill_everything(exc):
                    raise exc

                try:
                    _core.spawn_system_task(kill_everything, exc)
                except RuntimeError:
                    # We're quite late in the shutdown process and the
                    # system nursery is already closed.
                    # TODO(2020-06): this is a gross hack and should
                    # be fixed soon when we address #1607.
                    _core.current_task().parent_nursery.start_soon(kill_everything, exc)

            return True

        # This has to be carefully written to be safe in the face of new items
        # being queued while we iterate, and to do a bounded amount of work on
        # each pass:
        def run_all_bounded():
            for _ in range(len(self.queue)):
                run_cb(self.queue.popleft())
            for job in list(self.idempotent_queue):
                del self.idempotent_queue[job]
                run_cb(job)

        try:
            while True:
                run_all_bounded()
                if not self.queue and not self.idempotent_queue:
                    await self.wakeup.wait_woken()
                else:
                    await _core.checkpoint()
        except _core.Cancelled:
            # Keep the work done with this lock held as minimal as possible,
            # because it doesn't protect us against concurrent signal delivery
            # (see the comment above). Notice that this code would still be
            # correct if written like:
            #   self.done = True
            #   with self.lock:
            #       pass
            # because all we want is to force run_sync_soon
            # to either be completely before or completely after the write to
            # done. That's why we don't need the lock to protect
            # against signal handlers.
            with self.lock:
                self.done = True
            # No more jobs will be submitted, so just clear out any residual
            # ones:
            run_all_bounded()
            assert not self.queue
            assert not self.idempotent_queue

    def close(self):
        self.wakeup.close()

    def size(self):
        return len(self.queue) + len(self.idempotent_queue)

    def run_sync_soon(self, sync_fn, *args, idempotent=False):
        with self.lock:
            if self.done:
                raise _core.RunFinishedError("run() has exited")
            # We have to hold the lock all the way through here, because
            # otherwise the main thread might exit *while* we're doing these
            # calls, and then our queue item might not be processed, or the
            # wakeup call might trigger an OSError b/c the IO manager has
            # already been shut down.
            if idempotent:
                self.idempotent_queue[(sync_fn, args)] = None
            else:
                self.queue.append((sync_fn, args))
            self.wakeup.wakeup_thread_and_signal_safe()


@attr.s(eq=False, hash=False, slots=True)
class TrioToken(metaclass=NoPublicConstructor):
    """An opaque object representing a single call to :func:`trio.run`.

    It has no public constructor; instead, see :func:`current_trio_token`.

    This object has two uses:

    1. It lets you re-enter the Trio run loop from external threads or signal
       handlers. This is the low-level primitive that :func:`trio.to_thread`
       and `trio.from_thread` use to communicate with worker threads, that
       `trio.open_signal_receiver` uses to receive notifications about
       signals, and so forth.

    2. Each call to :func:`trio.run` has exactly one associated
       :class:`TrioToken` object, so you can use it to identify a particular
       call.

    """

    _reentry_queue = attr.ib()

    def run_sync_soon(self, sync_fn, *args, idempotent=False):
        """Schedule a call to ``sync_fn(*args)`` to occur in the context of a
        Trio task.

        This is safe to call from the main thread, from other threads, and
        from signal handlers. This is the fundamental primitive used to
        re-enter the Trio run loop from outside of it.

        The call will happen "soon", but there's no guarantee about exactly
        when, and no mechanism provided for finding out when it's happened.
        If you need this, you'll have to build your own.

        The call is effectively run as part of a system task (see
        :func:`~trio.lowlevel.spawn_system_task`). In particular this means
        that:

        * :exc:`KeyboardInterrupt` protection is *enabled* by default; if
          you want ``sync_fn`` to be interruptible by control-C, then you
          need to use :func:`~trio.lowlevel.disable_ki_protection`
          explicitly.

        * If ``sync_fn`` raises an exception, then it's converted into a
          :exc:`~trio.TrioInternalError` and *all* tasks are cancelled. You
          should be careful that ``sync_fn`` doesn't crash.

        All calls with ``idempotent=False`` are processed in strict
        first-in first-out order.

        If ``idempotent=True``, then ``sync_fn`` and ``args`` must be
        hashable, and Trio will make a best-effort attempt to discard any
        call submission which is equal to an already-pending call. Trio
        will process these in first-in first-out order.

        Any ordering guarantees apply separately to ``idempotent=False``
        and ``idempotent=True`` calls; there's no rule for how calls in the
        different categories are ordered with respect to each other.

        :raises trio.RunFinishedError:
              if the associated call to :func:`trio.run`
              has already exited. (Any call that *doesn't* raise this error
              is guaranteed to be fully processed before :func:`trio.run`
              exits.)

        """
        self._reentry_queue.run_sync_soon(sync_fn, *args, idempotent=idempotent)
