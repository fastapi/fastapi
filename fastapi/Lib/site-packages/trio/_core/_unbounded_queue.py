import attr

from .. import _core
from .._deprecate import deprecated
from .._util import Final


@attr.s(frozen=True)
class _UnboundedQueueStats:
    qsize = attr.ib()
    tasks_waiting = attr.ib()


class UnboundedQueue(metaclass=Final):
    """An unbounded queue suitable for certain unusual forms of inter-task
    communication.

    This class is designed for use as a queue in cases where the producer for
    some reason cannot be subjected to back-pressure, i.e., :meth:`put_nowait`
    has to always succeed. In order to prevent the queue backlog from actually
    growing without bound, the consumer API is modified to dequeue items in
    "batches". If a consumer task processes each batch without yielding, then
    this helps achieve (but does not guarantee) an effective bound on the
    queue's memory use, at the cost of potentially increasing system latencies
    in general. You should generally prefer to use a memory channel
    instead if you can.

    Currently each batch completely empties the queue, but `this may change in
    the future <https://github.com/python-trio/trio/issues/51>`__.

    A :class:`UnboundedQueue` object can be used as an asynchronous iterator,
    where each iteration returns a new batch of items. I.e., these two loops
    are equivalent::

       async for batch in queue:
           ...

       while True:
           obj = await queue.get_batch()
           ...

    """

    @deprecated(
        "0.9.0",
        issue=497,
        thing="trio.lowlevel.UnboundedQueue",
        instead="trio.open_memory_channel(math.inf)",
    )
    def __init__(self):
        self._lot = _core.ParkingLot()
        self._data = []
        # used to allow handoff from put to the first task in the lot
        self._can_get = False

    def __repr__(self):
        return "<UnboundedQueue holding {} items>".format(len(self._data))

    def qsize(self):
        """Returns the number of items currently in the queue."""
        return len(self._data)

    def empty(self):
        """Returns True if the queue is empty, False otherwise.

        There is some subtlety to interpreting this method's return value: see
        `issue #63 <https://github.com/python-trio/trio/issues/63>`__.

        """
        return not self._data

    @_core.enable_ki_protection
    def put_nowait(self, obj):
        """Put an object into the queue, without blocking.

        This always succeeds, because the queue is unbounded. We don't provide
        a blocking ``put`` method, because it would never need to block.

        Args:
          obj (object): The object to enqueue.

        """
        if not self._data:
            assert not self._can_get
            if self._lot:
                self._lot.unpark(count=1)
            else:
                self._can_get = True
        self._data.append(obj)

    def _get_batch_protected(self):
        data = self._data.copy()
        self._data.clear()
        self._can_get = False
        return data

    def get_batch_nowait(self):
        """Attempt to get the next batch from the queue, without blocking.

        Returns:
          list: A list of dequeued items, in order. On a successful call this
              list is always non-empty; if it would be empty we raise
              :exc:`~trio.WouldBlock` instead.

        Raises:
          ~trio.WouldBlock: if the queue is empty.

        """
        if not self._can_get:
            raise _core.WouldBlock
        return self._get_batch_protected()

    async def get_batch(self):
        """Get the next batch from the queue, blocking as necessary.

        Returns:
          list: A list of dequeued items, in order. This list is always
              non-empty.

        """
        await _core.checkpoint_if_cancelled()
        if not self._can_get:
            await self._lot.park()
            return self._get_batch_protected()
        else:
            try:
                return self._get_batch_protected()
            finally:
                await _core.cancel_shielded_checkpoint()

    def statistics(self):
        """Return an object containing debugging information.

        Currently the following fields are defined:

        * ``qsize``: The number of items currently in the queue.
        * ``tasks_waiting``: The number of tasks blocked on this queue's
          :meth:`get_batch` method.

        """
        return _UnboundedQueueStats(
            qsize=len(self._data), tasks_waiting=self._lot.statistics().tasks_waiting
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.get_batch()
