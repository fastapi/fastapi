from typing import Any, Callable

from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

asynccontextmanager_error_message = """
FastAPI's contextmanager_in_threadpool require Python 3.7 or above,
or the backport for Python 3.6, installed with:
    pip install async-generator
"""


def _fake_asynccontextmanager(func: Callable[..., Any]) -> Callable[..., Any]:
    def raiser(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError(asynccontextmanager_error_message)

    return raiser


try:
    from contextlib import asynccontextmanager as asynccontextmanager  # type: ignore
except ImportError:
    try:
        from async_generator import (  # type: ignore  # isort: skip
            asynccontextmanager as asynccontextmanager,
        )
    except ImportError:  # pragma: no cover
        asynccontextmanager = _fake_asynccontextmanager

try:
    from contextlib import AsyncExitStack as AsyncExitStack  # type: ignore
except ImportError:
    try:
        from async_exit_stack import AsyncExitStack as AsyncExitStack  # type: ignore
    except ImportError:  # pragma: no cover
        AsyncExitStack = None  # type: ignore


@asynccontextmanager  # type: ignore
async def contextmanager_in_threadpool(cm: Any) -> Any:
    try:
        yield await run_in_threadpool(cm.__enter__)
    except Exception as e:
        ok = await run_in_threadpool(cm.__exit__, type(e), e, None)
        if not ok:
            raise e
    else:
        await run_in_threadpool(cm.__exit__, None, None, None)
