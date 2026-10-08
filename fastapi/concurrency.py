import functools
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractContextManager
from contextlib import asynccontextmanager as asynccontextmanager
from typing import ParamSpec, TypeVar

import anyio.to_thread
from anyio import CapacityLimiter
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

_P = ParamSpec("_P")
_T = TypeVar("_T")

# Blocking __exit__ and other teardown operations from running can create race
# conditions/deadlocks if the context manager itself has its own internal pool
# (e.g. a database connection pool).
# To avoid this maintain a separate limiter for teardown operations, so that the
# operations acquiring resources can never block operations releasing resources.
# NOTE: 5 is arbitrary, we would like more than 1 so that teardowns are not serialised.
_teardown_limiter = CapacityLimiter(5)


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: AbstractContextManager[_T],
) -> AsyncGenerator[_T, None]:
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = bool(
            await run_in_teardown_threadpool(cm.__exit__, type(e), e, e.__traceback__)
        )
        if not ok:
            raise e
    else:
        await run_in_teardown_threadpool(cm.__exit__, None, None, None)


async def run_in_teardown_threadpool(
    func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    """Run a function in the separate teardown threadpool.

    This will run the function in the teardown threadpool in order to avoid it
    being blocked by other operations waiting to acquire resources.

    Unless you know what you are doing, you probably don't want this function,
    use run_in_threadpool instead.
    """
    func = functools.partial(func, *args, **kwargs)
    return await anyio.to_thread.run_sync(func, limiter=_teardown_limiter)
