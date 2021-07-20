import sys
from typing import AsyncGenerator, ContextManager, TypeVar

__all__ = [
    "iterate_in_threadpool",
    "run_in_threadpool",
    "run_until_first_complete",
    "contextmanager_in_threadpool",
    "asynccontextmanager",
    "AsyncExitStack",
]

from starlette.concurrency import (
    iterate_in_threadpool,
    run_in_threadpool,
    run_until_first_complete,
)

if sys.version_info >= (3, 7):
    from contextlib import AsyncExitStack, asynccontextmanager
else:
    from contextlib2 import AsyncExitStack, asynccontextmanager


_T = TypeVar("_T")


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = await run_in_threadpool(cm.__exit__, type(e), e, None)
        if not ok:
            raise e
    else:
        await run_in_threadpool(cm.__exit__, None, None, None)
