from collections.abc import AsyncGenerator, Callable, Iterable
from contextlib import AbstractContextManager
from contextlib import asynccontextmanager as asynccontextmanager
from typing import ParamSpec, TypeVar

import anyio.to_thread
from anyio import CapacityLimiter
from starlette.concurrency import (
    iterate_in_threadpool as _starlette_iterate_in_threadpool,
)
from starlette.concurrency import run_in_threadpool as _starlette_run_in_threadpool
from starlette.concurrency import (
    run_until_first_complete as _starlette_run_until_first_complete,
)

_P = ParamSpec("_P")
_T = TypeVar("_T")

# The default threadpool in anyio is 40. This limiter keeps one thread
# for teardown tasks in order to prevent deadlocks when there is a pool
# of finite resources (e.g. database connections) which threads will block
# on trying to acquire.
# NOTE: we defer instantiation until runtime since we must support anyio's trio backend
_anti_deadlock_capacity_limiter: CapacityLimiter | None = None


def _get_anti_deadlock_capacity_limiter() -> CapacityLimiter:
    global _anti_deadlock_capacity_limiter
    if _anti_deadlock_capacity_limiter is None:
        global_limit = anyio.to_thread.current_default_thread_limiter().total_tokens
        _anti_deadlock_capacity_limiter = CapacityLimiter(global_limit - 1)
    return _anti_deadlock_capacity_limiter


async def run_in_threadpool(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    async with _get_anti_deadlock_capacity_limiter():
        return await _starlette_run_in_threadpool(func, *args, **kwargs)


async def iterate_in_threadpool(iterator: Iterable[_T]) -> AsyncGenerator[_T, None]:
    async with _get_anti_deadlock_capacity_limiter():
        async for item in _starlette_iterate_in_threadpool(iterator):
            yield item


async def run_until_first_complete(*args: tuple[Callable, dict]) -> None:  # type: ignore[type-arg]
    async with _get_anti_deadlock_capacity_limiter():
        return await _starlette_run_until_first_complete(*args)


# NOTE: a separate function is required only because mypy dislikes trying to add
# a boolean flag along side the param spec
async def _run_in_threadpool_with_overflow(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    """Run a function in the thread pool, allowing it to use the overflow threads.

    Unless you know what you are doing you probably do not want to use this function.
    It has access to the entire thread pool, including the anti-deadlock reserve threads.
    """
    return await _starlette_run_in_threadpool(func, *args, **kwargs)


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: AbstractContextManager[_T],
) -> AsyncGenerator[_T, None]:
    # blocking __exit__ from running waiting on a free thread
    # can create race conditions/deadlocks if the context manager itself
    # has its own internal pool (e.g. a database connection pool)
    # to avoid this we let __exit__ run without a capacity limit
    # since we're creating a new limiter for each call, any non-zero limit
    # works (1 is arbitrary)
    exit_limiter = CapacityLimiter(1)
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = bool(
            await anyio.to_thread.run_sync(
                cm.__exit__, type(e), e, e.__traceback__, limiter=exit_limiter
            )
        )
        if not ok:
            raise e
    else:
        await anyio.to_thread.run_sync(
            cm.__exit__, None, None, None, limiter=exit_limiter
        )
