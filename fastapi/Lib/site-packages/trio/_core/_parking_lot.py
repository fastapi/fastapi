# ParkingLot provides an abstraction for a fair waitqueue with cancellation
# and requeueing support. Inspiration:
#
#    https://webkit.org/blog/6161/locking-in-webkit/
#    https://amanieu.github.io/parking_lot/
#
# which were in turn heavily influenced by
#
#    http://gee.cs.oswego.edu/dl/papers/aqs.pdf
#
# Compared to these, our use of cooperative scheduling allows some
# simplifications (no need for internal locking). On the other hand, the need
# to support Trio's strong cancellation semantics adds some complications
# (tasks need to know where they're queued so they can cancel). Also, in the
# above work, the ParkingLot is a global structure that holds a collection of
# waitqueues keyed by lock address, and which are opportunistically allocated
# and destroyed as contention arises; this allows the worst-case memory usage
# for all waitqueues to be O(#tasks). Here we allocate a separate wait queue
# for each synchronization object, so we're O(#objects + #tasks). This isn't
# *so* bad since compared to our synchronization objects are heavier than
# theirs and our tasks are lighter, so for us #objects is smaller and #tasks
# is larger.
#
# This is in the core because for two reasons. First, it's used by
# UnboundedQueue, and UnboundedQueue is used for a number of things in the
# core. And second, it's responsible for providing fairness to all of our
# high-level synchronization primitives (locks, queues, etc.). For now with
# our FIFO scheduler this is relatively trivial (it's just a FIFO waitqueue),
# but in the future we ever start support task priorities or fair scheduling
#
#    https://github.com/python-trio/trio/issues/32
#
# then all we'll have to do is update this. (Well, full-fledged task
# priorities might also require priority inheritance, which would require more
# work.)
#
# For discussion of data structures to use here, see:
#
#     https://github.com/dabeaz/curio/issues/136
#
# (and also the articles above). Currently we use a SortedDict ordered by a
# global monotonic counter that ensures FIFO ordering. The main advantage of
# this is that it's easy to implement :-). An intrusive doubly-linked list
# would also be a natural approach, so long as we only handle FIFO ordering.
#
# XX: should we switch to the shared global ParkingLot approach?
#
# XX: we should probably add support for "parking tokens" to allow for
# task-fair RWlock (basically: when parking a task needs to be able to mark
# itself as a reader or a writer, and then a task-fair wakeup policy is, wake
# the next task, and if it's a reader than keep waking tasks so long as they
# are readers). Without this I think you can implement write-biased or
# read-biased RWlocks (by using two parking lots and drawing from whichever is
# preferred), but not task-fair -- and task-fair plays much more nicely with
# WFQ. (Consider what happens in the two-lot implementation if you're
# write-biased but all the pending writers are blocked at the scheduler level
# by the WFQ logic...)
# ...alternatively, "phase-fair" RWlocks are pretty interesting:
#    http://www.cs.unc.edu/~anderson/papers/ecrts09b.pdf
# Useful summary:
# https://docs.oracle.com/javase/7/docs/api/java/util/concurrent/locks/ReadWriteLock.html
#
# XX: if we do add WFQ, then we might have to drop the current feature where
# unpark returns the tasks that were unparked. Rationale: suppose that at the
# time we call unpark, the next task is deprioritized... and then, before it
# becomes runnable, a new task parks which *is* runnable. Ideally we should
# immediately wake the new task, and leave the old task on the queue for
# later. But this means we can't commit to which task we are unparking when
# unpark is called.
#
# See: https://github.com/python-trio/trio/issues/53

from collections import OrderedDict

import attr

from .. import _core
from .._util import Final


@attr.s(frozen=True, slots=True)
class _ParkingLotStatistics:
    tasks_waiting = attr.ib()


@attr.s(eq=False, hash=False, slots=True)
class ParkingLot(metaclass=Final):
    """A fair wait queue with cancellation and requeueing.

    This class encapsulates the tricky parts of implementing a wait
    queue. It's useful for implementing higher-level synchronization
    primitives like queues and locks.

    In addition to the methods below, you can use ``len(parking_lot)`` to get
    the number of parked tasks, and ``if parking_lot: ...`` to check whether
    there are any parked tasks.

    """

    # {task: None}, we just want a deque where we can quickly delete random
    # items
    _parked = attr.ib(factory=OrderedDict, init=False)

    def __len__(self):
        """Returns the number of parked tasks."""
        return len(self._parked)

    def __bool__(self):
        """True if there are parked tasks, False otherwise."""
        return bool(self._parked)

    # XX this currently returns None
    # if we ever add the ability to repark while one's resuming place in
    # line (for false wakeups), then we could have it return a ticket that
    # abstracts the "place in line" concept.
    @_core.enable_ki_protection
    async def park(self):
        """Park the current task until woken by a call to :meth:`unpark` or
        :meth:`unpark_all`.

        """
        task = _core.current_task()
        self._parked[task] = None
        task.custom_sleep_data = self

        def abort_fn(_):
            del task.custom_sleep_data._parked[task]
            return _core.Abort.SUCCEEDED

        await _core.wait_task_rescheduled(abort_fn)

    def _pop_several(self, count):
        for _ in range(min(count, len(self._parked))):
            task, _ = self._parked.popitem(last=False)
            yield task

    @_core.enable_ki_protection
    def unpark(self, *, count=1):
        """Unpark one or more tasks.

        This wakes up ``count`` tasks that are blocked in :meth:`park`. If
        there are fewer than ``count`` tasks parked, then wakes as many tasks
        are available and then returns successfully.

        Args:
          count (int): the number of tasks to unpark.

        """
        tasks = list(self._pop_several(count))
        for task in tasks:
            _core.reschedule(task)
        return tasks

    def unpark_all(self):
        """Unpark all parked tasks."""
        return self.unpark(count=len(self))

    @_core.enable_ki_protection
    def repark(self, new_lot, *, count=1):
        """Move parked tasks from one :class:`ParkingLot` object to another.

        This dequeues ``count`` tasks from one lot, and requeues them on
        another, preserving order. For example::

           async def parker(lot):
               print("sleeping")
               await lot.park()
               print("woken")

           async def main():
               lot1 = trio.lowlevel.ParkingLot()
               lot2 = trio.lowlevel.ParkingLot()
               async with trio.open_nursery() as nursery:
                   nursery.start_soon(parker, lot1)
                   await trio.testing.wait_all_tasks_blocked()
                   assert len(lot1) == 1
                   assert len(lot2) == 0
                   lot1.repark(lot2)
                   assert len(lot1) == 0
                   assert len(lot2) == 1
                   # This wakes up the task that was originally parked in lot1
                   lot2.unpark()

        If there are fewer than ``count`` tasks parked, then reparks as many
        tasks as are available and then returns successfully.

        Args:
          new_lot (ParkingLot): the parking lot to move tasks to.
          count (int): the number of tasks to move.

        """
        if not isinstance(new_lot, ParkingLot):
            raise TypeError("new_lot must be a ParkingLot")
        for task in self._pop_several(count):
            new_lot._parked[task] = None
            task.custom_sleep_data = new_lot

    def repark_all(self, new_lot):
        """Move all parked tasks from one :class:`ParkingLot` object to
        another.

        See :meth:`repark` for details.

        """
        return self.repark(new_lot, count=len(self))

    def statistics(self):
        """Return an object containing debugging information.

        Currently the following fields are defined:

        * ``tasks_waiting``: The number of tasks blocked on this lot's
          :meth:`park` method.

        """
        return _ParkingLotStatistics(tasks_waiting=len(self._parked))
