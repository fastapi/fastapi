import sys
from typing import AsyncGenerator, ContextManager, TypeVar

from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

if sys.version_info >= (3, 7):
    from contextlib import AsyncExitStack as AsyncExitStack
    from contextlib import asynccontextmanager as asynccontextmanager
else:
    from contextlib2 import AsyncExitStack as AsyncExitStack  # noqa
    from contextlib2 import asynccontextmanager as asynccontextmanager  # noqa


_T = TypeVar("_T")


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok: bool = await run_in_threadpool(cm.__exit__, type(e), e, None)
        if not ok:
            raise e
    else:
        await run_in_threadpool(cm.__exit__, None, None, None)
