import functools
import sys
import typing
from contextlib import asynccontextmanager as asynccontextmanager
from typing import AsyncGenerator, ContextManager, Optional, TypeVar

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

import anyio.to_thread
from anyio import CapacityLimiter
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

_P = ParamSpec("_P")
_T = TypeVar("_T")


async def run_in_threadpool(
    func: typing.Callable[_P, _T],
    *args: typing.Any,
    _limiter: Optional[anyio.CapacityLimiter] = None,
    **kwargs: typing.Any,
) -> _T:
    if kwargs:  # pragma: no cover
        # run_sync doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)
    return await anyio.to_thread.run_sync(func, *args, limiter=_limiter)


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
    limiter: Optional[anyio.CapacityLimiter] = None,
) -> AsyncGenerator[_T, None]:
    # blocking __exit__ from running waiting on a free thread
    # can create race conditions/deadlocks if the context manager itself
    # has its own internal pool (e.g. a database connection pool)
    # to avoid this we let __exit__ run without a capacity limit
    # since we're creating a new limiter for each call, any non-zero limit
    # works (1 is arbitrary)
    exit_limiter = CapacityLimiter(1)
    try:
        yield await run_in_threadpool(cm.__enter__, _limiter=limiter)
    except Exception as e:
        ok = bool(
            await run_in_threadpool(
                cm.__exit__, type(e), e, e.__traceback__, _limiter=exit_limiter
            )
        )
        if not ok:
            raise e
    else:
        await run_in_threadpool(cm.__exit__, None, None, None, _limiter=exit_limiter)
