import pytest

from ... import _core


# scary runvar tests
def test_runvar_smoketest():
    t1 = _core.RunVar("test1")
    t2 = _core.RunVar("test2", default="catfish")

    assert "RunVar" in repr(t1)

    async def first_check():
        with pytest.raises(LookupError):
            t1.get()

        t1.set("swordfish")
        assert t1.get() == "swordfish"
        assert t2.get() == "catfish"
        assert t2.get(default="eel") == "eel"

        t2.set("goldfish")
        assert t2.get() == "goldfish"
        assert t2.get(default="tuna") == "goldfish"

    async def second_check():
        with pytest.raises(LookupError):
            t1.get()

        assert t2.get() == "catfish"

    _core.run(first_check)
    _core.run(second_check)


def test_runvar_resetting():
    t1 = _core.RunVar("test1")
    t2 = _core.RunVar("test2", default="dogfish")
    t3 = _core.RunVar("test3")

    async def reset_check():
        token = t1.set("moonfish")
        assert t1.get() == "moonfish"
        t1.reset(token)

        with pytest.raises(TypeError):
            t1.reset(None)

        with pytest.raises(LookupError):
            t1.get()

        token2 = t2.set("catdogfish")
        assert t2.get() == "catdogfish"
        t2.reset(token2)
        assert t2.get() == "dogfish"

        with pytest.raises(ValueError):
            t2.reset(token2)

        token3 = t3.set("basculin")
        assert t3.get() == "basculin"

        with pytest.raises(ValueError):
            t1.reset(token3)

    _core.run(reset_check)


def test_runvar_sync():
    t1 = _core.RunVar("test1")

    async def sync_check():
        async def task1():
            t1.set("plaice")
            assert t1.get() == "plaice"

        async def task2(tok):
            t1.reset(token)

            with pytest.raises(LookupError):
                t1.get()

            t1.set("cod")

        async with _core.open_nursery() as n:
            token = t1.set("cod")
            assert t1.get() == "cod"

            n.start_soon(task1)
            await _core.wait_all_tasks_blocked()
            assert t1.get() == "plaice"

            n.start_soon(task2, token)
            await _core.wait_all_tasks_blocked()
            assert t1.get() == "cod"

    _core.run(sync_check)


def test_accessing_runvar_outside_run_call_fails():
    t1 = _core.RunVar("test1")

    with pytest.raises(RuntimeError):
        t1.set("asdf")

    with pytest.raises(RuntimeError):
        t1.get()

    async def get_token():
        return t1.set("ok")

    token = _core.run(get_token)

    with pytest.raises(RuntimeError):
        t1.reset(token)
