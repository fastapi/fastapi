from contextlib import AsyncExitStack as AsyncExitStack  # noqa
from contextlib import asynccontextmanager as asynccontextmanager
from functools import partial
from typing import Any, AsyncGenerator, ContextManager, Optional, TypeVar

import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from anyio.to_thread import run_sync
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

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


MaybeException = Optional[Exception]


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
    limiter: Optional[anyio.CapacityLimiter] = None,
) -> AsyncGenerator[_T, None]:
    # streams for the data
    send_res, rcv_res = anyio.create_memory_object_stream(  # type: ignore
        0, item_type=Any
    )
    # streams for exceptions
    send_err, rcv_err = anyio.create_memory_object_stream(  # type: ignore
        0, item_type=MaybeException
    )
    async with AsyncExitStack() as stack:
        stack.enter_context(rcv_res)
        stack.enter_context(rcv_err)
        stack.enter_context(send_res)
        stack.enter_context(send_err)
        tg = await stack.enter_async_context(anyio.create_task_group())
        target = partial(
            run_sync, _cm_thead_worker, cm, send_res, rcv_err, limiter=limiter
        )
        tg.start_soon(target)
        res = await rcv_res.receive()
        try:
            yield res
        except Exception as e:
            await send_err.send(e)
        else:
            await send_err.send(None)
