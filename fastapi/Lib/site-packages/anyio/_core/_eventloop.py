from __future__ import annotations

import math
import sys
import threading
from contextlib import contextmanager
from importlib import import_module
from typing import (
    Any,
    Awaitable,
    Callable,
    Generator,
    TypeVar,
)

import sniffio

# This must be updated when new backends are introduced
from ._compat import DeprecatedAwaitableFloat

BACKENDS = "asyncio", "trio"

T_Retval = TypeVar("T_Retval")
threadlocals = threading.local()


def run(
    func: Callable[..., Awaitable[T_Retval]],
    *args: object,
    backend: str = "asyncio",
    backend_options: dict[str, Any] | None = None,
) -> T_Retval:
    """
    Run the given coroutine function in an asynchronous event loop.

    The current thread must not be already running an event loop.

    :param func: a coroutine function
    :param args: positional arguments to ``func``
    :param backend: name of the asynchronous event loop implementation – currently either
        ``asyncio`` or ``trio``
    :param backend_options: keyword arguments to call the backend ``run()`` implementation with
        (documented :ref:`here <backend options>`)
    :return: the return value of the coroutine function
    :raises RuntimeError: if an asynchronous event loop is already running in this thread
    :raises LookupError: if the named backend is not found

    """
    try:
        asynclib_name = sniffio.current_async_library()
    except sniffio.AsyncLibraryNotFoundError:
        pass
    else:
        raise RuntimeError(f"Already running {asynclib_name} in this thread")

    try:
        asynclib = import_module(f"..._backends._{backend}", package=__name__)
    except ImportError as exc:
        raise LookupError(f"No such backend: {backend}") from exc

    token = None
    if sniffio.current_async_library_cvar.get(None) is None:
        # Since we're in control of the event loop, we can cache the name of the async library
        token = sniffio.current_async_library_cvar.set(backend)

    try:
        backend_options = backend_options or {}
        return asynclib.run(func, *args, **backend_options)
    finally:
        if token:
            sniffio.current_async_library_cvar.reset(token)


async def sleep(delay: float) -> None:
    """
    Pause the current task for the specified duration.

    :param delay: the duration, in seconds

    """
    return await get_asynclib().sleep(delay)


async def sleep_forever() -> None:
    """
    Pause the current task until it's cancelled.

    This is a shortcut for ``sleep(math.inf)``.

    .. versionadded:: 3.1

    """
    await sleep(math.inf)


async def sleep_until(deadline: float) -> None:
    """
    Pause the current task until the given time.

    :param deadline: the absolute time to wake up at (according to the internal monotonic clock of
        the event loop)

    .. versionadded:: 3.1

    """
    now = current_time()
    await sleep(max(deadline - now, 0))


def current_time() -> DeprecatedAwaitableFloat:
    """
    Return the current value of the event loop's internal clock.

    :return: the clock value (seconds)

    """
    return DeprecatedAwaitableFloat(get_asynclib().current_time(), current_time)


def get_all_backends() -> tuple[str, ...]:
    """Return a tuple of the names of all built-in backends."""
    return BACKENDS


def get_cancelled_exc_class() -> type[BaseException]:
    """Return the current async library's cancellation exception class."""
    return get_asynclib().CancelledError


#
# Private API
#


@contextmanager
def claim_worker_thread(backend: str) -> Generator[Any, None, None]:
    module = sys.modules["anyio._backends._" + backend]
    threadlocals.current_async_module = module
    try:
        yield
    finally:
        del threadlocals.current_async_module


def get_asynclib(asynclib_name: str | None = None) -> Any:
    if asynclib_name is None:
        asynclib_name = sniffio.current_async_library()

    modulename = "anyio._backends._" + asynclib_name
    try:
        return sys.modules[modulename]
    except KeyError:
        return import_module(modulename)
