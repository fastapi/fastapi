import sys
from typing import Any, AsyncGenerator, ContextManager, Optional, TypeVar

import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

if sys.version_info >= (3, 7):
    from contextlib import AsyncExitStack as AsyncExitStack
    from contextlib import asynccontextmanager as asynccontextmanager
else:
    from contextlib2 import AsyncExitStack as AsyncExitStack  # noqa
    from contextlib2 import asynccontextmanager as asynccontextmanager  # noqa


_T = TypeVar("_T")


def _cm_thead_worker(
    cm: ContextManager[_T],
    res_stream: MemoryObjectSendStream[_T],
    err_stream: MemoryObjectReceiveStream[Optional[Exception]],
) -> None:
    with cm as res:
        anyio.from_thread.run(res_stream.send, res)
        exc = anyio.from_thread.run(err_stream.receive)
        if exc:
            raise exc


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:
    # streams for the data
    send_res, rcv_res = anyio.create_memory_object_stream(  # type: ignore
        0, item_type=Any
    )
    # streams for exceptions
    send_err, rcv_err = anyio.create_memory_object_stream(  # type: ignore
        0, item_type=Optional[Exception]
    )
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(rcv_res)
        await stack.enter_async_context(rcv_err)
        await stack.enter_async_context(send_res)
        await stack.enter_async_context(send_err)
        tg = await stack.enter_async_context(anyio.create_task_group())
        tg.start_soon(run_in_threadpool, _cm_thead_worker, cm, send_res, rcv_err)
        res = await rcv_res.receive()
        try:
            yield res
        except Exception as e:
            await send_err.send(e)
        else:
            await send_err.send(None)
