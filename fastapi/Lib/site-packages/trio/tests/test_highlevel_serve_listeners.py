import errno
from functools import partial

import attr
import pytest

import trio
from trio.testing import memory_stream_pair, wait_all_tasks_blocked


@attr.s(hash=False, eq=False)
class MemoryListener(trio.abc.Listener):
    closed = attr.ib(default=False)
    accepted_streams = attr.ib(factory=list)
    queued_streams = attr.ib(factory=(lambda: trio.open_memory_channel(1)))
    accept_hook = attr.ib(default=None)

    async def connect(self):
        assert not self.closed
        client, server = memory_stream_pair()
        await self.queued_streams[0].send(server)
        return client

    async def accept(self):
        await trio.lowlevel.checkpoint()
        assert not self.closed
        if self.accept_hook is not None:
            await self.accept_hook()
        stream = await self.queued_streams[1].receive()
        self.accepted_streams.append(stream)
        return stream

    async def aclose(self):
        self.closed = True
        await trio.lowlevel.checkpoint()


async def test_serve_listeners_basic():
    listeners = [MemoryListener(), MemoryListener()]

    record = []

    def close_hook():
        # Make sure this is a forceful close
        assert trio.current_effective_deadline() == float("-inf")
        record.append("closed")

    async def handler(stream):
        await stream.send_all(b"123")
        assert await stream.receive_some(10) == b"456"
        stream.send_stream.close_hook = close_hook
        stream.receive_stream.close_hook = close_hook

    async def client(listener):
        s = await listener.connect()
        assert await s.receive_some(10) == b"123"
        await s.send_all(b"456")

    async def do_tests(parent_nursery):
        async with trio.open_nursery() as nursery:
            for listener in listeners:
                for _ in range(3):
                    nursery.start_soon(client, listener)

        await wait_all_tasks_blocked()

        # verifies that all 6 streams x 2 directions each were closed ok
        assert len(record) == 12

        parent_nursery.cancel_scope.cancel()

    async with trio.open_nursery() as nursery:
        l2 = await nursery.start(trio.serve_listeners, handler, listeners)
        assert l2 == listeners
        # This is just split into another function because gh-136 isn't
        # implemented yet
        nursery.start_soon(do_tests, nursery)

    for listener in listeners:
        assert listener.closed


async def test_serve_listeners_accept_unrecognized_error():
    for error in [KeyError(), OSError(errno.ECONNABORTED, "ECONNABORTED")]:
        listener = MemoryListener()

        async def raise_error():
            raise error

        listener.accept_hook = raise_error

        with pytest.raises(type(error)) as excinfo:
            await trio.serve_listeners(None, [listener])
        assert excinfo.value is error


async def test_serve_listeners_accept_capacity_error(autojump_clock, caplog):
    listener = MemoryListener()

    async def raise_EMFILE():
        raise OSError(errno.EMFILE, "out of file descriptors")

    listener.accept_hook = raise_EMFILE

    # It retries every 100 ms, so in 950 ms it will retry at 0, 100, ..., 900
    # = 10 times total
    with trio.move_on_after(0.950):
        await trio.serve_listeners(None, [listener])

    assert len(caplog.records) == 10
    for record in caplog.records:
        assert "retrying" in record.msg
        assert record.exc_info[1].errno == errno.EMFILE


async def test_serve_listeners_connection_nursery(autojump_clock):
    listener = MemoryListener()

    async def handler(stream):
        await trio.sleep(1)

    class Done(Exception):
        pass

    async def connection_watcher(*, task_status=trio.TASK_STATUS_IGNORED):
        async with trio.open_nursery() as nursery:
            task_status.started(nursery)
            await wait_all_tasks_blocked()
            assert len(nursery.child_tasks) == 10
            raise Done

    with pytest.raises(Done):
        async with trio.open_nursery() as nursery:
            handler_nursery = await nursery.start(connection_watcher)
            await nursery.start(
                partial(
                    trio.serve_listeners,
                    handler,
                    [listener],
                    handler_nursery=handler_nursery,
                )
            )
            for _ in range(10):
                nursery.start_soon(listener.connect)
