import threading
from types import TracebackType
from typing import Optional, Type

import sniffio

from ._exceptions import ExceptionMapping, PoolTimeout, map_exceptions

# Our async synchronization primatives use either 'anyio' or 'trio' depending
# on if they're running under asyncio or trio.

try:
    import trio
except ImportError:  # pragma: nocover
    trio = None  # type: ignore

try:
    import anyio
except ImportError:  # pragma: nocover
    anyio = None  # type: ignore


class AsyncLock:
    def __init__(self) -> None:
        self._backend = ""

    def setup(self) -> None:
        """
        Detect if we're running under 'asyncio' or 'trio' and create
        a lock with the correct implementation.
        """
        self._backend = sniffio.current_async_library()
        if self._backend == "trio":
            if trio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under trio, requires the 'trio' package to be installed."
                )
            self._trio_lock = trio.Lock()
        else:
            if anyio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under asyncio requires the 'anyio' package to be installed."
                )
            self._anyio_lock = anyio.Lock()

    async def __aenter__(self) -> "AsyncLock":
        if not self._backend:
            self.setup()

        if self._backend == "trio":
            await self._trio_lock.acquire()
        else:
            await self._anyio_lock.acquire()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        if self._backend == "trio":
            self._trio_lock.release()
        else:
            self._anyio_lock.release()


class AsyncEvent:
    def __init__(self) -> None:
        self._backend = ""

    def setup(self) -> None:
        """
        Detect if we're running under 'asyncio' or 'trio' and create
        a lock with the correct implementation.
        """
        self._backend = sniffio.current_async_library()
        if self._backend == "trio":
            if trio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under trio requires the 'trio' package to be installed."
                )
            self._trio_event = trio.Event()
        else:
            if anyio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under asyncio requires the 'anyio' package to be installed."
                )
            self._anyio_event = anyio.Event()

    def set(self) -> None:
        if not self._backend:
            self.setup()

        if self._backend == "trio":
            self._trio_event.set()
        else:
            self._anyio_event.set()

    async def wait(self, timeout: Optional[float] = None) -> None:
        if not self._backend:
            self.setup()

        if self._backend == "trio":
            if trio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under trio requires the 'trio' package to be installed."
                )

            trio_exc_map: ExceptionMapping = {trio.TooSlowError: PoolTimeout}
            timeout_or_inf = float("inf") if timeout is None else timeout
            with map_exceptions(trio_exc_map):
                with trio.fail_after(timeout_or_inf):
                    await self._trio_event.wait()
        else:
            if anyio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under asyncio requires the 'anyio' package to be installed."
                )

            anyio_exc_map: ExceptionMapping = {TimeoutError: PoolTimeout}
            with map_exceptions(anyio_exc_map):
                with anyio.fail_after(timeout):
                    await self._anyio_event.wait()


class AsyncSemaphore:
    def __init__(self, bound: int) -> None:
        self._bound = bound
        self._backend = ""

    def setup(self) -> None:
        """
        Detect if we're running under 'asyncio' or 'trio' and create
        a semaphore with the correct implementation.
        """
        self._backend = sniffio.current_async_library()
        if self._backend == "trio":
            if trio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under trio requires the 'trio' package to be installed."
                )

            self._trio_semaphore = trio.Semaphore(
                initial_value=self._bound, max_value=self._bound
            )
        else:
            if anyio is None:  # pragma: nocover
                raise RuntimeError(
                    "Running under asyncio requires the 'anyio' package to be installed."
                )

            self._anyio_semaphore = anyio.Semaphore(
                initial_value=self._bound, max_value=self._bound
            )

    async def acquire(self) -> None:
        if not self._backend:
            self.setup()

        if self._backend == "trio":
            await self._trio_semaphore.acquire()
        else:
            await self._anyio_semaphore.acquire()

    async def release(self) -> None:
        if self._backend == "trio":
            self._trio_semaphore.release()
        else:
            self._anyio_semaphore.release()


# Our thread-based synchronization primitives...


class Lock:
    def __init__(self) -> None:
        self._lock = threading.Lock()

    def __enter__(self) -> "Lock":
        self._lock.acquire()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        self._lock.release()


class Event:
    def __init__(self) -> None:
        self._event = threading.Event()

    def set(self) -> None:
        self._event.set()

    def wait(self, timeout: Optional[float] = None) -> None:
        if not self._event.wait(timeout=timeout):
            raise PoolTimeout()  # pragma: nocover


class Semaphore:
    def __init__(self, bound: int) -> None:
        self._semaphore = threading.Semaphore(value=bound)

    def acquire(self) -> None:
        self._semaphore.acquire()

    def release(self) -> None:
        self._semaphore.release()
