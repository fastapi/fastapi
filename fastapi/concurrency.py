from contextlib import AsyncExitStack as AsyncExitStack
from contextlib import asynccontextmanager as asynccontextmanager
from contextvars import copy_context
from functools import partial
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    ContextManager,
    Optional,
    TypeVar,
)

import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from anyio.to_thread import run_sync

T = TypeVar("T")


def callable_in_thread_pool(
    call: Callable[..., T], *, limiter: Optional[anyio.CapacityLimiter]
) -> Callable[..., Awaitable[T]]:
    def inner(*args: Any, **kwargs: Any) -> "Awaitable[T]":
        return anyio.to_thread.run_sync(
            copy_context().run, lambda: call(*args, **kwargs), limiter=limiter
        )  # type: ignore[return-value]

    return inner


def _cm_thead_worker(
    cm: ContextManager[T],
    res_stream: MemoryObjectSendStream[T],
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
    cm: ContextManager[T],
    limiter: Optional[anyio.CapacityLimiter] = None,
) -> AsyncGenerator[T, None]:
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
