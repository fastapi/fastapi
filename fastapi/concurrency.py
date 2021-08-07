import contextvars
import functools
from typing import (
    Any,
    AsyncContextManager,
    AsyncGenerator,
    Awaitable,
    Callable,
    ContextManager,
    TypeVar,
)

import anyio
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
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
except ImportError:  # pragma: no cover
    try:
        from async_generator import (  # type: ignore  # isort: skip
            asynccontextmanager as asynccontextmanager,
        )
    except ImportError:  # pragma: no cover
        asynccontextmanager = _fake_asynccontextmanager

try:
    from contextlib import AsyncExitStack as AsyncExitStack  # type: ignore
except ImportError:  # pragma: no cover
    try:
        from async_exit_stack import AsyncExitStack as AsyncExitStack  # type: ignore
    except ImportError:  # pragma: no cover
        AsyncExitStack = None  # type: ignore


T = TypeVar("T")


def bind_callable_to_threadpool(func: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    async def inner(*args: Any, **kwargs: Any) -> T:
        if contextvars is not None:  # pragma: no cover
            # Ensure we run in the same context
            child = functools.partial(func, *args, **kwargs)
            context = contextvars.copy_context()
            call = context.run
            args = (child,)
        elif kwargs:  # pragma: no cover
            # run_sync doesn't accept 'kwargs', so bind them in here
            call = functools.partial(func, **kwargs)
        return await anyio.to_thread.run_sync(call, *args)

    return inner


def bind_context_manager_to_threadpool(
    call: Callable[..., ContextManager[T]]
) -> Callable[..., AsyncContextManager[T]]:
    @asynccontextmanager
    async def inner(*args: Any, **kwds: Any) -> AsyncGenerator[T, None]:
        cm = call(*args, **kwds)
        try:
            yield await bind_callable_to_threadpool(cm.__enter__)()
        except Exception as e:
            ok = await bind_callable_to_threadpool(cm.__exit__)(type(e), e, None)
            if not ok:
                raise e
        else:
            await bind_callable_to_threadpool(cm.__exit__)(None, None, None)

    return inner


def bind_async_context_manager_to_stack(
    cm: Callable[..., AsyncContextManager[T]], stack: AsyncExitStack
) -> Callable[..., Awaitable[T]]:
    async def inner(*args: Any, **kwargs: Any) -> T:
        return await stack.enter_async_context(cm(*args, **kwargs))

    return inner


@asynccontextmanager  # type: ignore
async def contextmanager_in_threadpool(cm: Any) -> Any:
    def wrap():
        return cm

    async with bind_context_manager_to_threadpool(wrap)() as val:
        yield val
