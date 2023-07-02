import itertools

import pytest

from ... import _core
from ...testing import assert_checkpoints, wait_all_tasks_blocked

pytestmark = pytest.mark.filterwarnings(
    "ignore:.*UnboundedQueue:trio.TrioDeprecationWarning"
)


async def test_UnboundedQueue_basic():
    q = _core.UnboundedQueue()
    q.put_nowait("hi")
    assert await q.get_batch() == ["hi"]
    with pytest.raises(_core.WouldBlock):
        q.get_batch_nowait()
    q.put_nowait(1)
    q.put_nowait(2)
    q.put_nowait(3)
    assert q.get_batch_nowait() == [1, 2, 3]

    assert q.empty()
    assert q.qsize() == 0
    q.put_nowait(None)
    assert not q.empty()
    assert q.qsize() == 1

    stats = q.statistics()
    assert stats.qsize == 1
    assert stats.tasks_waiting == 0

    # smoke test
    repr(q)


async def test_UnboundedQueue_blocking():
    record = []
    q = _core.UnboundedQueue()

    async def get_batch_consumer():
        while True:
            batch = await q.get_batch()
            assert batch
            record.append(batch)

    async def aiter_consumer():
        async for batch in q:
            assert batch
            record.append(batch)

    for consumer in (get_batch_consumer, aiter_consumer):
        record.clear()
        async with _core.open_nursery() as nursery:
            nursery.start_soon(consumer)
            await _core.wait_all_tasks_blocked()
            stats = q.statistics()
            assert stats.qsize == 0
            assert stats.tasks_waiting == 1
            q.put_nowait(10)
            q.put_nowait(11)
            await _core.wait_all_tasks_blocked()
            q.put_nowait(12)
            await _core.wait_all_tasks_blocked()
            assert record == [[10, 11], [12]]
            nursery.cancel_scope.cancel()


async def test_UnboundedQueue_fairness():
    q = _core.UnboundedQueue()

    # If there's no-one else around, we can put stuff in and take it out
    # again, no problem
    q.put_nowait(1)
    q.put_nowait(2)
    assert q.get_batch_nowait() == [1, 2]

    result = None

    async def get_batch(q):
        nonlocal result
        result = await q.get_batch()

    # But if someone else is waiting to read, then they get dibs
    async with _core.open_nursery() as nursery:
        nursery.start_soon(get_batch, q)
        await _core.wait_all_tasks_blocked()
        q.put_nowait(3)
        q.put_nowait(4)
        with pytest.raises(_core.WouldBlock):
            q.get_batch_nowait()
    assert result == [3, 4]

    # If two tasks are trying to read, they alternate
    record = []

    async def reader(name):
        while True:
            record.append((name, await q.get_batch()))

    async with _core.open_nursery() as nursery:
        nursery.start_soon(reader, "a")
        await _core.wait_all_tasks_blocked()
        nursery.start_soon(reader, "b")
        await _core.wait_all_tasks_blocked()

        for i in range(20):
            q.put_nowait(i)
            await _core.wait_all_tasks_blocked()

        nursery.cancel_scope.cancel()

    assert record == list(zip(itertools.cycle("ab"), [[i] for i in range(20)]))


async def test_UnboundedQueue_trivial_yields():
    q = _core.UnboundedQueue()

    q.put_nowait(None)
    with assert_checkpoints():
        await q.get_batch()

    q.put_nowait(None)
    with assert_checkpoints():
        async for _ in q:  # noqa # pragma: no branch
            break


async def test_UnboundedQueue_no_spurious_wakeups():
    # If we have two tasks waiting, and put two items into the queue... then
    # only one task wakes up
    record = []

    async def getter(q, i):
        got = await q.get_batch()
        record.append((i, got))

    async with _core.open_nursery() as nursery:
        q = _core.UnboundedQueue()
        nursery.start_soon(getter, q, 1)
        await wait_all_tasks_blocked()
        nursery.start_soon(getter, q, 2)
        await wait_all_tasks_blocked()

        for i in range(10):
            q.put_nowait(i)
        await wait_all_tasks_blocked()

        assert record == [(1, list(range(10)))]

        nursery.cancel_scope.cancel()
