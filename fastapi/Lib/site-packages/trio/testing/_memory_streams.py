import operator

from .. import _core, _util
from .._highlevel_generic import StapledStream
from ..abc import ReceiveStream, SendStream

################################################################
# In-memory streams - Unbounded buffer version
################################################################


class _UnboundedByteQueue:
    def __init__(self):
        self._data = bytearray()
        self._closed = False
        self._lot = _core.ParkingLot()
        self._fetch_lock = _util.ConflictDetector(
            "another task is already fetching data"
        )

    # This object treats "close" as being like closing the send side of a
    # channel: so after close(), calling put() raises ClosedResourceError, and
    # calling the get() variants drains the buffer and then returns an empty
    # bytearray.
    def close(self):
        self._closed = True
        self._lot.unpark_all()

    def close_and_wipe(self):
        self._data = bytearray()
        self.close()

    def put(self, data):
        if self._closed:
            raise _core.ClosedResourceError("virtual connection closed")
        self._data += data
        self._lot.unpark_all()

    def _check_max_bytes(self, max_bytes):
        if max_bytes is None:
            return
        max_bytes = operator.index(max_bytes)
        if max_bytes < 1:
            raise ValueError("max_bytes must be >= 1")

    def _get_impl(self, max_bytes):
        assert self._closed or self._data
        if max_bytes is None:
            max_bytes = len(self._data)
        if self._data:
            chunk = self._data[:max_bytes]
            del self._data[:max_bytes]
            assert chunk
            return chunk
        else:
            return bytearray()

    def get_nowait(self, max_bytes=None):
        with self._fetch_lock:
            self._check_max_bytes(max_bytes)
            if not self._closed and not self._data:
                raise _core.WouldBlock
            return self._get_impl(max_bytes)

    async def get(self, max_bytes=None):
        with self._fetch_lock:
            self._check_max_bytes(max_bytes)
            if not self._closed and not self._data:
                await self._lot.park()
            else:
                await _core.checkpoint()
            return self._get_impl(max_bytes)


class MemorySendStream(SendStream, metaclass=_util.Final):
    """An in-memory :class:`~trio.abc.SendStream`.

    Args:
      send_all_hook: An async function, or None. Called from
          :meth:`send_all`. Can do whatever you like.
      wait_send_all_might_not_block_hook: An async function, or None. Called
          from :meth:`wait_send_all_might_not_block`. Can do whatever you
          like.
      close_hook: A synchronous function, or None. Called from :meth:`close`
          and :meth:`aclose`. Can do whatever you like.

    .. attribute:: send_all_hook
                   wait_send_all_might_not_block_hook
                   close_hook

       All of these hooks are also exposed as attributes on the object, and
       you can change them at any time.

    """

    def __init__(
        self,
        send_all_hook=None,
        wait_send_all_might_not_block_hook=None,
        close_hook=None,
    ):
        self._conflict_detector = _util.ConflictDetector(
            "another task is using this stream"
        )
        self._outgoing = _UnboundedByteQueue()
        self.send_all_hook = send_all_hook
        self.wait_send_all_might_not_block_hook = wait_send_all_might_not_block_hook
        self.close_hook = close_hook

    async def send_all(self, data):
        """Places the given data into the object's internal buffer, and then
        calls the :attr:`send_all_hook` (if any).

        """
        # Execute two checkpoints so we have more of a chance to detect
        # buggy user code that calls this twice at the same time.
        with self._conflict_detector:
            await _core.checkpoint()
            await _core.checkpoint()
            self._outgoing.put(data)
            if self.send_all_hook is not None:
                await self.send_all_hook()

    async def wait_send_all_might_not_block(self):
        """Calls the :attr:`wait_send_all_might_not_block_hook` (if any), and
        then returns immediately.

        """
        # Execute two checkpoints so we have more of a chance to detect
        # buggy user code that calls this twice at the same time.
        with self._conflict_detector:
            await _core.checkpoint()
            await _core.checkpoint()
            # check for being closed:
            self._outgoing.put(b"")
            if self.wait_send_all_might_not_block_hook is not None:
                await self.wait_send_all_might_not_block_hook()

    def close(self):
        """Marks this stream as closed, and then calls the :attr:`close_hook`
        (if any).

        """
        # XXX should this cancel any pending calls to the send_all_hook and
        # wait_send_all_might_not_block_hook? Those are the only places where
        # send_all and wait_send_all_might_not_block can be blocked.
        #
        # The way we set things up, send_all_hook is memory_stream_pump, and
        # wait_send_all_might_not_block_hook is unset. memory_stream_pump is
        # synchronous. So normally, send_all and wait_send_all_might_not_block
        # cannot block at all.
        self._outgoing.close()
        if self.close_hook is not None:
            self.close_hook()

    async def aclose(self):
        """Same as :meth:`close`, but async."""
        self.close()
        await _core.checkpoint()

    async def get_data(self, max_bytes=None):
        """Retrieves data from the internal buffer, blocking if necessary.

        Args:
          max_bytes (int or None): The maximum amount of data to
              retrieve. None (the default) means to retrieve all the data
              that's present (but still blocks until at least one byte is
              available).

        Returns:
          If this stream has been closed, an empty bytearray. Otherwise, the
          requested data.

        """
        return await self._outgoing.get(max_bytes)

    def get_data_nowait(self, max_bytes=None):
        """Retrieves data from the internal buffer, but doesn't block.

        See :meth:`get_data` for details.

        Raises:
          trio.WouldBlock: if no data is available to retrieve.

        """
        return self._outgoing.get_nowait(max_bytes)


class MemoryReceiveStream(ReceiveStream, metaclass=_util.Final):
    """An in-memory :class:`~trio.abc.ReceiveStream`.

    Args:
      receive_some_hook: An async function, or None. Called from
          :meth:`receive_some`. Can do whatever you like.
      close_hook: A synchronous function, or None. Called from :meth:`close`
          and :meth:`aclose`. Can do whatever you like.

    .. attribute:: receive_some_hook
                   close_hook

       Both hooks are also exposed as attributes on the object, and you can
       change them at any time.

    """

    def __init__(self, receive_some_hook=None, close_hook=None):
        self._conflict_detector = _util.ConflictDetector(
            "another task is using this stream"
        )
        self._incoming = _UnboundedByteQueue()
        self._closed = False
        self.receive_some_hook = receive_some_hook
        self.close_hook = close_hook

    async def receive_some(self, max_bytes=None):
        """Calls the :attr:`receive_some_hook` (if any), and then retrieves
        data from the internal buffer, blocking if necessary.

        """
        # Execute two checkpoints so we have more of a chance to detect
        # buggy user code that calls this twice at the same time.
        with self._conflict_detector:
            await _core.checkpoint()
            await _core.checkpoint()
            if self._closed:
                raise _core.ClosedResourceError
            if self.receive_some_hook is not None:
                await self.receive_some_hook()
            # self._incoming's closure state tracks whether we got an EOF.
            # self._closed tracks whether we, ourselves, are closed.
            # self.close() sends an EOF to wake us up and sets self._closed,
            # so after we wake up we have to check self._closed again.
            data = await self._incoming.get(max_bytes)
            if self._closed:
                raise _core.ClosedResourceError
            return data

    def close(self):
        """Discards any pending data from the internal buffer, and marks this
        stream as closed.

        """
        self._closed = True
        self._incoming.close_and_wipe()
        if self.close_hook is not None:
            self.close_hook()

    async def aclose(self):
        """Same as :meth:`close`, but async."""
        self.close()
        await _core.checkpoint()

    def put_data(self, data):
        """Appends the given data to the internal buffer."""
        self._incoming.put(data)

    def put_eof(self):
        """Adds an end-of-file marker to the internal buffer."""
        self._incoming.close()


def memory_stream_pump(memory_send_stream, memory_receive_stream, *, max_bytes=None):
    """Take data out of the given :class:`MemorySendStream`'s internal buffer,
    and put it into the given :class:`MemoryReceiveStream`'s internal buffer.

    Args:
      memory_send_stream (MemorySendStream): The stream to get data from.
      memory_receive_stream (MemoryReceiveStream): The stream to put data into.
      max_bytes (int or None): The maximum amount of data to transfer in this
          call, or None to transfer all available data.

    Returns:
      True if it successfully transferred some data, or False if there was no
      data to transfer.

    This is used to implement :func:`memory_stream_one_way_pair` and
    :func:`memory_stream_pair`; see the latter's docstring for an example
    of how you might use it yourself.

    """
    try:
        data = memory_send_stream.get_data_nowait(max_bytes)
    except _core.WouldBlock:
        return False
    try:
        if not data:
            memory_receive_stream.put_eof()
        else:
            memory_receive_stream.put_data(data)
    except _core.ClosedResourceError:
        raise _core.BrokenResourceError("MemoryReceiveStream was closed")
    return True


def memory_stream_one_way_pair():
    """Create a connected, pure-Python, unidirectional stream with infinite
    buffering and flexible configuration options.

    You can think of this as being a no-operating-system-involved
    Trio-streamsified version of :func:`os.pipe` (except that :func:`os.pipe`
    returns the streams in the wrong order – we follow the superior convention
    that data flows from left to right).

    Returns:
      A tuple (:class:`MemorySendStream`, :class:`MemoryReceiveStream`), where
      the :class:`MemorySendStream` has its hooks set up so that it calls
      :func:`memory_stream_pump` from its
      :attr:`~MemorySendStream.send_all_hook` and
      :attr:`~MemorySendStream.close_hook`.

    The end result is that data automatically flows from the
    :class:`MemorySendStream` to the :class:`MemoryReceiveStream`. But you're
    also free to rearrange things however you like. For example, you can
    temporarily set the :attr:`~MemorySendStream.send_all_hook` to None if you
    want to simulate a stall in data transmission. Or see
    :func:`memory_stream_pair` for a more elaborate example.

    """
    send_stream = MemorySendStream()
    recv_stream = MemoryReceiveStream()

    def pump_from_send_stream_to_recv_stream():
        memory_stream_pump(send_stream, recv_stream)

    async def async_pump_from_send_stream_to_recv_stream():
        pump_from_send_stream_to_recv_stream()

    send_stream.send_all_hook = async_pump_from_send_stream_to_recv_stream
    send_stream.close_hook = pump_from_send_stream_to_recv_stream
    return send_stream, recv_stream


def _make_stapled_pair(one_way_pair):
    pipe1_send, pipe1_recv = one_way_pair()
    pipe2_send, pipe2_recv = one_way_pair()
    stream1 = StapledStream(pipe1_send, pipe2_recv)
    stream2 = StapledStream(pipe2_send, pipe1_recv)
    return stream1, stream2


def memory_stream_pair():
    """Create a connected, pure-Python, bidirectional stream with infinite
    buffering and flexible configuration options.

    This is a convenience function that creates two one-way streams using
    :func:`memory_stream_one_way_pair`, and then uses
    :class:`~trio.StapledStream` to combine them into a single bidirectional
    stream.

    This is like a no-operating-system-involved, Trio-streamsified version of
    :func:`socket.socketpair`.

    Returns:
      A pair of :class:`~trio.StapledStream` objects that are connected so
      that data automatically flows from one to the other in both directions.

    After creating a stream pair, you can send data back and forth, which is
    enough for simple tests::

       left, right = memory_stream_pair()
       await left.send_all(b"123")
       assert await right.receive_some() == b"123"
       await right.send_all(b"456")
       assert await left.receive_some() == b"456"

    But if you read the docs for :class:`~trio.StapledStream` and
    :func:`memory_stream_one_way_pair`, you'll see that all the pieces
    involved in wiring this up are public APIs, so you can adjust to suit the
    requirements of your tests. For example, here's how to tweak a stream so
    that data flowing from left to right trickles in one byte at a time (but
    data flowing from right to left proceeds at full speed)::

        left, right = memory_stream_pair()
        async def trickle():
            # left is a StapledStream, and left.send_stream is a MemorySendStream
            # right is a StapledStream, and right.recv_stream is a MemoryReceiveStream
            while memory_stream_pump(left.send_stream, right.recv_stream, max_bytes=1):
                # Pause between each byte
                await trio.sleep(1)
        # Normally this send_all_hook calls memory_stream_pump directly without
        # passing in a max_bytes. We replace it with our custom version:
        left.send_stream.send_all_hook = trickle

    And here's a simple test using our modified stream objects::

        async def sender():
            await left.send_all(b"12345")
            await left.send_eof()

        async def receiver():
            async for data in right:
                print(data)

        async with trio.open_nursery() as nursery:
            nursery.start_soon(sender)
            nursery.start_soon(receiver)

    By default, this will print ``b"12345"`` and then immediately exit; with
    our trickle stream it instead sleeps 1 second, then prints ``b"1"``, then
    sleeps 1 second, then prints ``b"2"``, etc.

    Pro-tip: you can insert sleep calls (like in our example above) to
    manipulate the flow of data across tasks... and then use
    :class:`MockClock` and its :attr:`~MockClock.autojump_threshold`
    functionality to keep your test suite running quickly.

    If you want to stress test a protocol implementation, one nice trick is to
    use the :mod:`random` module (preferably with a fixed seed) to move random
    numbers of bytes at a time, and insert random sleeps in between them. You
    can also set up a custom :attr:`~MemoryReceiveStream.receive_some_hook` if
    you want to manipulate things on the receiving side, and not just the
    sending side.

    """
    return _make_stapled_pair(memory_stream_one_way_pair)


################################################################
# In-memory streams - Lockstep version
################################################################


class _LockstepByteQueue:
    def __init__(self):
        self._data = bytearray()
        self._sender_closed = False
        self._receiver_closed = False
        self._receiver_waiting = False
        self._waiters = _core.ParkingLot()
        self._send_conflict_detector = _util.ConflictDetector(
            "another task is already sending"
        )
        self._receive_conflict_detector = _util.ConflictDetector(
            "another task is already receiving"
        )

    def _something_happened(self):
        self._waiters.unpark_all()

    # Always wakes up when one side is closed, because everyone always reacts
    # to that.
    async def _wait_for(self, fn):
        while True:
            if fn():
                break
            if self._sender_closed or self._receiver_closed:
                break
            await self._waiters.park()
        await _core.checkpoint()

    def close_sender(self):
        self._sender_closed = True
        self._something_happened()

    def close_receiver(self):
        self._receiver_closed = True
        self._something_happened()

    async def send_all(self, data):
        with self._send_conflict_detector:
            if self._sender_closed:
                raise _core.ClosedResourceError
            if self._receiver_closed:
                raise _core.BrokenResourceError
            assert not self._data
            self._data += data
            self._something_happened()
            await self._wait_for(lambda: not self._data)
            if self._sender_closed:
                raise _core.ClosedResourceError
            if self._data and self._receiver_closed:
                raise _core.BrokenResourceError

    async def wait_send_all_might_not_block(self):
        with self._send_conflict_detector:
            if self._sender_closed:
                raise _core.ClosedResourceError
            if self._receiver_closed:
                await _core.checkpoint()
                return
            await self._wait_for(lambda: self._receiver_waiting)
            if self._sender_closed:
                raise _core.ClosedResourceError

    async def receive_some(self, max_bytes=None):
        with self._receive_conflict_detector:
            # Argument validation
            if max_bytes is not None:
                max_bytes = operator.index(max_bytes)
                if max_bytes < 1:
                    raise ValueError("max_bytes must be >= 1")
            # State validation
            if self._receiver_closed:
                raise _core.ClosedResourceError
            # Wake wait_send_all_might_not_block and wait for data
            self._receiver_waiting = True
            self._something_happened()
            try:
                await self._wait_for(lambda: self._data)
            finally:
                self._receiver_waiting = False
            if self._receiver_closed:
                raise _core.ClosedResourceError
            # Get data, possibly waking send_all
            if self._data:
                # Neat trick: if max_bytes is None, then obj[:max_bytes] is
                # the same as obj[:].
                got = self._data[:max_bytes]
                del self._data[:max_bytes]
                self._something_happened()
                return got
            else:
                assert self._sender_closed
                return b""


class _LockstepSendStream(SendStream):
    def __init__(self, lbq):
        self._lbq = lbq

    def close(self):
        self._lbq.close_sender()

    async def aclose(self):
        self.close()
        await _core.checkpoint()

    async def send_all(self, data):
        await self._lbq.send_all(data)

    async def wait_send_all_might_not_block(self):
        await self._lbq.wait_send_all_might_not_block()


class _LockstepReceiveStream(ReceiveStream):
    def __init__(self, lbq):
        self._lbq = lbq

    def close(self):
        self._lbq.close_receiver()

    async def aclose(self):
        self.close()
        await _core.checkpoint()

    async def receive_some(self, max_bytes=None):
        return await self._lbq.receive_some(max_bytes)


def lockstep_stream_one_way_pair():
    """Create a connected, pure Python, unidirectional stream where data flows
    in lockstep.

    Returns:
      A tuple
      (:class:`~trio.abc.SendStream`, :class:`~trio.abc.ReceiveStream`).

    This stream has *absolutely no* buffering. Each call to
    :meth:`~trio.abc.SendStream.send_all` will block until all the given data
    has been returned by a call to
    :meth:`~trio.abc.ReceiveStream.receive_some`.

    This can be useful for testing flow control mechanisms in an extreme case,
    or for setting up "clogged" streams to use with
    :func:`check_one_way_stream` and friends.

    In addition to fulfilling the :class:`~trio.abc.SendStream` and
    :class:`~trio.abc.ReceiveStream` interfaces, the return objects
    also have a synchronous ``close`` method.

    """

    lbq = _LockstepByteQueue()
    return _LockstepSendStream(lbq), _LockstepReceiveStream(lbq)


def lockstep_stream_pair():
    """Create a connected, pure-Python, bidirectional stream where data flows
    in lockstep.

    Returns:
      A tuple (:class:`~trio.StapledStream`, :class:`~trio.StapledStream`).

    This is a convenience function that creates two one-way streams using
    :func:`lockstep_stream_one_way_pair`, and then uses
    :class:`~trio.StapledStream` to combine them into a single bidirectional
    stream.

    """
    return _make_stapled_pair(lockstep_stream_one_way_pair)
