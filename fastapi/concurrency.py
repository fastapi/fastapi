from contextlib import asynccontextmanager as asynccontextmanager
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    ContextManager,
    Generator,
    Optional,
    Type,
    TypeVar,
    Union,
)

import anyio.to_thread
from anyio import CapacityLimiter
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

_T = TypeVar("_T")


@asynccontextmanager
async def contextmanager_in_threadpool(  # not used, kept for backwards compatibility
    cm: ContextManager[_T],
) -> AsyncGenerator[_T, None]:  # pragma: no cover
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


class _StopIteration(Exception):
    pass


class ContextManagerFromGenerator:
    """Create a context manager from a generator.

    It handles both sync and async generators. Generator has to have exactly one yield.

    Implementation is based on contextlib's contextmanager.

    Additionally, as apposed to contextlib.contextmanager/contextlib.asynccontextmanager,
    this context manager allows to call `asend` on underlaying generator and gracefully handle
    this scenario in __aexit__.

    Instances of this class cannot be reused.
    """

    def __init__(self, gen: Union[AsyncGenerator[_T, None], Generator[_T, None, None]]):
        self.gen = gen
        self._has_started = False
        self._has_executed = False

    @staticmethod
    def _send(gen: Generator[_T, None, None], value: Any) -> Any:
        # We can't raise `StopIteration` from within the threadpool executor
        # and catch it outside that context, so we coerce them into a different
        # exception type.
        try:
            return gen.send(value)
        except StopIteration:
            raise _StopIteration from None

    @staticmethod
    def _throw(gen: Generator[_T, None, None], value: Any) -> Any:
        # We can't raise `StopIteration` from within the threadpool executor
        # and catch it outside that context, so we coerce them into a different
        # exception type.
        try:
            return gen.throw(value)
        except StopIteration:
            raise _StopIteration from None

    async def __aenter__(self) -> Any:
        try:
            if isinstance(self.gen, Generator):
                result = await run_in_threadpool(self._send, self.gen, None)
            else:
                result = await self.gen.asend(None)
            self._has_started = True
            return result
        except (_StopIteration, StopAsyncIteration):
            raise RuntimeError("generator didn't yield") from None  # pragma: no cover

    async def asend(self, value: Any) -> None:
        if self._has_executed:
            raise RuntimeError(
                "ContextManagerFromGenerator can only be used once"
            )  # pragma: no cover
        if not self._has_started:
            raise RuntimeError(
                "ContextManagerFromGenerator has not been entered"
            )  # pragma: no cover
        self._has_executed = True
        try:
            if isinstance(self.gen, Generator):
                await run_in_threadpool(self._send, self.gen, value)
            else:
                await self.gen.asend(value)
        except (_StopIteration, StopAsyncIteration):
            return
        else:  # pragma: no cover
            try:
                raise RuntimeError("generator didn't stop")
            finally:
                if isinstance(self.gen, Generator):
                    self.gen.close()
                else:
                    await self.gen.aclose()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if self._has_executed:
            if isinstance(self.gen, Generator):
                self.gen.close()
                return False
            await self.gen.aclose()
            return False

        # blocking __exit__ from running waiting on a free thread
        # can create race conditions/deadlocks if the context manager itself
        # has its own internal pool (e.g. a database connection pool)
        # to avoid this we let __exit__ run without a capacity limit
        # since we're creating a new limiter for each call, any non-zero limit
        # works (1 is arbitrary)
        exit_limiter = CapacityLimiter(1)

        if exc_type is None:  # pragma: no cover
            # usually shouldn't happen, as we call asend
            try:
                if isinstance(self.gen, Generator):
                    await anyio.to_thread.run_sync(
                        self._send,
                        self.gen,
                        None,
                        limiter=exit_limiter,
                    )
                else:
                    await self.gen.asend(None)
            except (_StopIteration, StopAsyncIteration):
                return False
            else:  # pragma: no cover
                try:
                    raise RuntimeError("generator didn't stop")
                finally:
                    if isinstance(self.gen, Generator):
                        self.gen.close()
                    else:
                        await self.gen.aclose()

        if exc_value is None:  # pragma: no cover
            # Need to force instantiation so we can reliably
            # tell if we get the same exception back
            exc_value = exc_type()

        try:
            if isinstance(self.gen, Generator):
                await anyio.to_thread.run_sync(
                    self._throw,
                    self.gen,
                    exc_value,
                    limiter=exit_limiter,
                )
            else:
                await self.gen.athrow(exc_value)
        except (StopIteration, _StopIteration, StopAsyncIteration) as exc:
            # Suppress Stop(Async)Iteration *unless* it's the same exception that
            # was passed to throw().  This prevents a Stop(Async)Iteration
            # raised inside the "with" statement from being suppressed.
            return exc is not exc_value
        except RuntimeError as exc:  # pragma: no cover
            # Don't re-raise the passed in exception. (issue27122)
            if exc is exc_value:
                exc.__traceback__ = traceback
                return False
            # Avoid suppressing if a Stop(Async)Iteration exception
            # was passed to athrow() and later wrapped into a RuntimeError
            # (see PEP 479 for sync generators; async generators also
            # have this behavior). But do this only if the exception wrapped
            # by the RuntimeError is actually Stop(Async)Iteration (see
            # issue29692).
            if (
                isinstance(
                    exc_value,
                    (StopIteration, _StopIteration, StopAsyncIteration),
                )
                and exc.__cause__ is exc_value
            ):
                exc_value.__traceback__ = traceback
                return False
            raise
        except BaseException as exc:
            # only re-raise if it's *not* the exception that was
            # passed to throw(), because __exit__() must not raise
            # an exception unless __exit__() itself failed.  But throw()
            # has to raise the exception to signal propagation, so this
            # fixes the impedance mismatch between the throw() protocol
            # and the __exit__() protocol.
            if exc is not exc_value:
                raise
            exc.__traceback__ = traceback
            return False
        try:  # pragma: no cover
            raise RuntimeError("generator didn't stop after athrow()")
        finally:  # pragma: no cover
            if isinstance(self.gen, Generator):
                self.gen.close()
            else:
                await self.gen.aclose()
