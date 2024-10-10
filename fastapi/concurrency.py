from contextlib import asynccontextmanager
from typing import AsyncGenerator, ContextManager, TypeVar

import anyio
from anyio import CapacityLimiter
from starlette.concurrency import (
    iterate_in_threadpool,  # noqa
    run_in_threadpool,  # noqa
    run_until_first_complete,  # noqa
)

_T = TypeVar("_T")


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:
    """
    Context manager to run a synchronous context manager in a thread pool.

    This avoids blocking the event loop while entering or exiting the synchronous context manager.

    Args:
        cm: A synchronous context manager to be run in a thread pool.

    Yields:
        The result of entering the context manager.
    """
    # Allow _exit_ to run without a capacity limit to avoid deadlocks
    exit_limiter = CapacityLimiter(1)

    try:
        yield await run_in_threadpool(cm._enter_)
    except Exception as e:
        # Handle the exit of the context manager on exception
        exit_success = await anyio.to_thread.run_sync(
            cm._exit_, type(e), e, None, limiter=exit_limiter
        )
        if not exit_success:
            raise RuntimeError("Failed to exit context manager properly.") from e
    else:
        # Ensure the context manager exits successfully
        await anyio.to_thread.run_sync(
            cm._exit_, None, None, None, limiter=exit_limiter
        )
