import functools
from collections.abc import AsyncGenerator, Callable, Iterable
from contextlib import AbstractContextManager
from contextlib import asynccontextmanager as asynccontextmanager
from typing import Literal, ParamSpec, TypeVar

import anyio.to_thread
from anyio import CapacityLimiter
from starlette.concurrency import (
    _next,
    _StopIteration,
    run_until_first_complete,  # noqa
)

_P = ParamSpec("_P")
_T = TypeVar("_T")

# A pair of limiters keep one thread for teardown tasks in order to prevent deadlocks
# when there is a pool of finite resources (e.g. database connections) which threads will
# block on trying to acquire.
# NOTE: we cannot use anyio's default limiter, since other libraries will not respect the
# anti-deadlock reserve and may use up all available threads - we maintain our own pool.
_global_capacity_limiter: CapacityLimiter | None = None
_anti_deadlock_capacity_limiter: CapacityLimiter | None = None


def _get_capacity_limiter(kind: Literal["global", "anti_deadlock"]) -> CapacityLimiter:
    global _global_capacity_limiter, _anti_deadlock_capacity_limiter
    if _global_capacity_limiter is None:
        global_limit = anyio.to_thread.current_default_thread_limiter().total_tokens
        _global_capacity_limiter = CapacityLimiter(global_limit)
        _anti_deadlock_capacity_limiter = CapacityLimiter(global_limit - 1)
    return (
        _anti_deadlock_capacity_limiter
        if kind == "anti_deadlock"
        else _global_capacity_limiter
    )


# These are vendored from starlette to allow setting our own thread limiter
async def run_in_threadpool(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    async with _get_capacity_limiter("anti_deadlock"):
        func = functools.partial(func, *args, **kwargs)
        return await anyio.to_thread.run_sync(
            func, limiter=_get_capacity_limiter("global")
        )


async def iterate_in_threadpool(iterator: Iterable[_T]) -> AsyncGenerator[_T, None]:
    async with _get_capacity_limiter("anti_deadlock"):
        as_iterator = iter(iterator)
        while True:
            try:
                yield await anyio.to_thread.run_sync(
                    _next, as_iterator, limiter=_get_capacity_limiter("global")
                )
            except _StopIteration:
                break


# NOTE: a separate function is required only because mypy dislikes trying to add
# a boolean flag along side the param spec
async def _run_in_threadpool_with_overflow(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    """Run a function in the thread pool, allowing it to use the overflow threads.

    Unless you know what you are doing you probably do not want to use this function.
    It has access to the entire thread pool, including the anti-deadlock reserve threads.
    """
    func = functools.partial(func, *args, **kwargs)
    return await anyio.to_thread.run_sync(func, limiter=_global_capacity_limiter)


def set_thread_limit(limit: int = 40, anti_deadlock_reserve: int = 1) -> None:
    """
    Set the maximum number of threads that can be used by the thread pool.

    This is a global setting that affects all calls to `run_in_threadpool` and
    `iterate_in_threadpool`.
    """
    if not isinstance(limit, int):
        raise TypeError("Thread limit must be an integer.")

    if not isinstance(anti_deadlock_reserve, int):
        raise TypeError("Anti deadlock reserve must be an integer.")

    if limit < 2:
        raise ValueError("Thread limit must be at least 2.")

    if not 0 < anti_deadlock_reserve < limit - 1:
        raise ValueError("Anti deadlock reserve must be between 0 and limit - 1.")

    _get_capacity_limiter("global").total_tokens = limit
    _get_capacity_limiter("anti_deadlock").total_tokens = limit - anti_deadlock_reserve


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: AbstractContextManager[_T],
) -> AsyncGenerator[_T, None]:
    # blocking __exit__ from running waiting on a free thread
    # can create race conditions/deadlocks if the context manager itself
    # has its own internal pool (e.g. a database connection pool)
    # to avoid this we let __exit__ run without a capacity limit
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = bool(
            await _run_in_threadpool_with_overflow(
                cm.__exit__, type(e), e, e.__traceback__
            )
        )
        if not ok:
            raise e
    else:
        await _run_in_threadpool_with_overflow(cm.__exit__, None, None, None)
