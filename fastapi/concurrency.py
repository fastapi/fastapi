from contextlib import asynccontextmanager as asynccontextmanager
from typing import AsyncGenerator, ContextManager, TypeVar

import anyio
from anyio import CapacityLimiter
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

_T = TypeVar("_T")


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:
    """
    Context manager that allows running a synchronous context manager in a thread pool.

    This helps to avoid blocking the event loop while the synchronous context manager
    is being entered or exited.
    """
    exit_limiter = CapacityLimiter(1)
    try:
        yield await run_in_threadpool(cm._enter_)
    except Exception as e:
        ok = bool(
            await anyio.to_thread.run_sync(
                cm._exit_, type(e), e, None, limiter=exit_limiter
            )
        )

        if not ok:
            raise RuntimeError("Failed to exit context manager properly.") from e
    else:
        await anyio.to_thread.run_sync(
            cm.exit, None, None, None, limiter=exit_limiter
            )