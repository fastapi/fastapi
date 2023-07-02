import contextvars

from .. import _core

trio_testing_contextvar = contextvars.ContextVar("trio_testing_contextvar")


async def test_contextvars_default():
    trio_testing_contextvar.set("main")
    record = []

    async def child():
        value = trio_testing_contextvar.get()
        record.append(value)

    async with _core.open_nursery() as nursery:
        nursery.start_soon(child)
    assert record == ["main"]


async def test_contextvars_set():
    trio_testing_contextvar.set("main")
    record = []

    async def child():
        trio_testing_contextvar.set("child")
        value = trio_testing_contextvar.get()
        record.append(value)

    async with _core.open_nursery() as nursery:
        nursery.start_soon(child)
    value = trio_testing_contextvar.get()
    assert record == ["child"]
    assert value == "main"


async def test_contextvars_copy():
    trio_testing_contextvar.set("main")
    context = contextvars.copy_context()
    trio_testing_contextvar.set("second_main")
    record = []

    async def child():
        value = trio_testing_contextvar.get()
        record.append(value)

    async with _core.open_nursery() as nursery:
        context.run(nursery.start_soon, child)
        nursery.start_soon(child)
    value = trio_testing_contextvar.get()
    assert set(record) == {"main", "second_main"}
    assert value == "second_main"
