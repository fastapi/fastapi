import attr
import pytest

from ... import _abc, _core
from .tutil import check_sequence_matches


@attr.s(eq=False, hash=False)
class TaskRecorder:
    record = attr.ib(factory=list)

    def before_run(self):
        self.record.append(("before_run",))

    def task_scheduled(self, task):
        self.record.append(("schedule", task))

    def before_task_step(self, task):
        assert task is _core.current_task()
        self.record.append(("before", task))

    def after_task_step(self, task):
        assert task is _core.current_task()
        self.record.append(("after", task))

    def after_run(self):
        self.record.append(("after_run",))

    def filter_tasks(self, tasks):
        for item in self.record:
            if item[0] in ("schedule", "before", "after") and item[1] in tasks:
                yield item
            if item[0] in ("before_run", "after_run"):
                yield item


def test_instruments(recwarn):
    r1 = TaskRecorder()
    r2 = TaskRecorder()
    r3 = TaskRecorder()

    task = None

    # We use a child task for this, because the main task does some extra
    # bookkeeping stuff that can leak into the instrument results, and we
    # don't want to deal with it.
    async def task_fn():
        nonlocal task
        task = _core.current_task()

        for _ in range(4):
            await _core.checkpoint()
        # replace r2 with r3, to test that we can manipulate them as we go
        _core.remove_instrument(r2)
        with pytest.raises(KeyError):
            _core.remove_instrument(r2)
        # add is idempotent
        _core.add_instrument(r3)
        _core.add_instrument(r3)
        for _ in range(1):
            await _core.checkpoint()

    async def main():
        async with _core.open_nursery() as nursery:
            nursery.start_soon(task_fn)

    _core.run(main, instruments=[r1, r2])

    # It sleeps 5 times, so it runs 6 times.  Note that checkpoint()
    # reschedules the task immediately upon yielding, before the
    # after_task_step event fires.
    expected = (
        [("before_run",), ("schedule", task)]
        + [("before", task), ("schedule", task), ("after", task)] * 5
        + [("before", task), ("after", task), ("after_run",)]
    )
    assert r1.record == r2.record + r3.record
    assert list(r1.filter_tasks([task])) == expected


def test_instruments_interleave():
    tasks = {}

    async def two_step1():
        tasks["t1"] = _core.current_task()
        await _core.checkpoint()

    async def two_step2():
        tasks["t2"] = _core.current_task()
        await _core.checkpoint()

    async def main():
        async with _core.open_nursery() as nursery:
            nursery.start_soon(two_step1)
            nursery.start_soon(two_step2)

    r = TaskRecorder()
    _core.run(main, instruments=[r])

    expected = [
        ("before_run",),
        ("schedule", tasks["t1"]),
        ("schedule", tasks["t2"]),
        {
            ("before", tasks["t1"]),
            ("schedule", tasks["t1"]),
            ("after", tasks["t1"]),
            ("before", tasks["t2"]),
            ("schedule", tasks["t2"]),
            ("after", tasks["t2"]),
        },
        {
            ("before", tasks["t1"]),
            ("after", tasks["t1"]),
            ("before", tasks["t2"]),
            ("after", tasks["t2"]),
        },
        ("after_run",),
    ]
    print(list(r.filter_tasks(tasks.values())))
    check_sequence_matches(list(r.filter_tasks(tasks.values())), expected)


def test_null_instrument():
    # undefined instrument methods are skipped
    class NullInstrument:
        def something_unrelated(self):
            pass  # pragma: no cover

    async def main():
        await _core.checkpoint()

    _core.run(main, instruments=[NullInstrument()])


def test_instrument_before_after_run():
    record = []

    class BeforeAfterRun:
        def before_run(self):
            record.append("before_run")

        def after_run(self):
            record.append("after_run")

    async def main():
        pass

    _core.run(main, instruments=[BeforeAfterRun()])
    assert record == ["before_run", "after_run"]


def test_instrument_task_spawn_exit():
    record = []

    class SpawnExitRecorder:
        def task_spawned(self, task):
            record.append(("spawned", task))

        def task_exited(self, task):
            record.append(("exited", task))

    async def main():
        return _core.current_task()

    main_task = _core.run(main, instruments=[SpawnExitRecorder()])
    assert ("spawned", main_task) in record
    assert ("exited", main_task) in record


# This test also tests having a crash before the initial task is even spawned,
# which is very difficult to handle.
def test_instruments_crash(caplog):
    record = []

    class BrokenInstrument:
        def task_scheduled(self, task):
            record.append("scheduled")
            raise ValueError("oops")

        def close(self):
            # Shouldn't be called -- tests that the instrument disabling logic
            # works right.
            record.append("closed")  # pragma: no cover

    async def main():
        record.append("main ran")
        return _core.current_task()

    r = TaskRecorder()
    main_task = _core.run(main, instruments=[r, BrokenInstrument()])
    assert record == ["scheduled", "main ran"]
    # the TaskRecorder kept going throughout, even though the BrokenInstrument
    # was disabled
    assert ("after", main_task) in r.record
    assert ("after_run",) in r.record
    # And we got a log message
    exc_type, exc_value, exc_traceback = caplog.records[0].exc_info
    assert exc_type is ValueError
    assert str(exc_value) == "oops"
    assert "Instrument has been disabled" in caplog.records[0].message


def test_instruments_monkeypatch():
    class NullInstrument(_abc.Instrument):
        pass

    instrument = NullInstrument()

    async def main():
        record = []

        # Changing the set of hooks implemented by an instrument after
        # it's installed doesn't make them start being called right away
        instrument.before_task_step = record.append
        await _core.checkpoint()
        await _core.checkpoint()
        assert len(record) == 0

        # But if we remove and re-add the instrument, the new hooks are
        # picked up
        _core.remove_instrument(instrument)
        _core.add_instrument(instrument)
        await _core.checkpoint()
        await _core.checkpoint()
        assert record.count(_core.current_task()) == 2

        _core.remove_instrument(instrument)
        await _core.checkpoint()
        await _core.checkpoint()
        assert record.count(_core.current_task()) == 2

    _core.run(main, instruments=[instrument])


def test_instrument_that_raises_on_getattr():
    class EvilInstrument:
        def task_exited(self, task):
            raise AssertionError()  # pragma: no cover

        @property
        def after_run(self):
            raise ValueError("oops")

    async def main():
        with pytest.raises(ValueError):
            _core.add_instrument(EvilInstrument())

        # Make sure the instrument is fully removed from the per-method lists
        runner = _core.current_task()._runner
        assert "after_run" not in runner.instruments
        assert "task_exited" not in runner.instruments

    _core.run(main)
