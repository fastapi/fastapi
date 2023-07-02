from __future__ import annotations

from typing import Callable, TypeVar
from warnings import warn

from ._core._eventloop import get_asynclib
from .abc import CapacityLimiter

T_Retval = TypeVar("T_Retval")


async def run_sync(
    func: Callable[..., T_Retval],
    *args: object,
    cancellable: bool = False,
    limiter: CapacityLimiter | None = None,
) -> T_Retval:
    """
    Call the given function with the given arguments in a worker thread.

    If the ``cancellable`` option is enabled and the task waiting for its completion is cancelled,
    the thread will still run its course but its return value (or any raised exception) will be
    ignored.

    :param func: a callable
    :param args: positional arguments for the callable
    :param cancellable: ``True`` to allow cancellation of the operation
    :param limiter: capacity limiter to use to limit the total amount of threads running
        (if omitted, the default limiter is used)
    :return: an awaitable that yields the return value of the function.

    """
    return await get_asynclib().run_sync_in_worker_thread(
        func, *args, cancellable=cancellable, limiter=limiter
    )


async def run_sync_in_worker_thread(
    func: Callable[..., T_Retval],
    *args: object,
    cancellable: bool = False,
    limiter: CapacityLimiter | None = None,
) -> T_Retval:
    warn(
        "run_sync_in_worker_thread() has been deprecated, use anyio.to_thread.run_sync() instead",
        DeprecationWarning,
    )
    return await run_sync(func, *args, cancellable=cancellable, limiter=limiter)


def current_default_thread_limiter() -> CapacityLimiter:
    """
    Return the capacity limiter that is used by default to limit the number of concurrent threads.

    :return: a capacity limiter object

    """
    return get_asynclib().current_default_thread_limiter()


def current_default_worker_thread_limiter() -> CapacityLimiter:
    warn(
        "current_default_worker_thread_limiter() has been deprecated, "
        "use anyio.to_thread.current_default_thread_limiter() instead",
        DeprecationWarning,
    )
    return current_default_thread_limiter()
