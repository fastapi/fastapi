from typing import Any

from starlette.concurrency import iterate_in_threadpool, run_in_threadpool  # noqa

asynccontextmanager_error_message = """
FastAPI contextmanagers with require Python 3.7 or the backport installed with:
    pip install async-generator
"""


def _fake_asynccontextmanager(func):
    def raiser(*args, **kwargs):
        raise RuntimeError(asynccontextmanager_error_message)

    return raiser


try:
    from contextlib import asynccontextmanager
except ImportError:  # pragma: no cover
    try:
        from async_generator import asynccontextmanager
    except ImportError:  # pragma: no cover
        asynccontextmanager = _fake_asynccontextmanager

try:
    from contextlib import AsyncExitStack
except ImportError:  # pragma: no cover
    try:
        from async_exit_stack import AsyncExitStack
    except ImportError:  # pragma: no cover
        AsyncExitStack = None


@asynccontextmanager
async def contextmanager_in_threadpool(cm: Any) -> Any:
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = await run_in_threadpool(cm.__exit__, type(e), e, None)
        if not ok:
            raise e
    else:
        await run_in_threadpool(cm.__exit__, None, None, None)
