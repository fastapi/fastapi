from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from contextlib import asynccontextmanager as asynccontextmanager
from typing import TypeVar
from weakref import WeakKeyDictionary

import anyio.to_thread
from anyio import CancelScope, CapacityLimiter, Semaphore
from anyio.lowlevel import RunVar, checkpoint_if_cancelled
from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
from starlette.concurrency import (  # noqa
    run_until_first_complete as run_until_first_complete,
)

_T = TypeVar("_T")

# Weak keys release semaphore bookkeeping when its declaration is collected.
_dependency_semaphores: RunVar[
    WeakKeyDictionary["_DependencyConcurrency", Semaphore]
] = RunVar("fastapi_dependency_semaphores")


@asynccontextmanager
async def contextmanager_in_threadpool(
    cm: AbstractContextManager[_T],
) -> AsyncGenerator[_T, None]:
    # blocking __exit__ from running waiting on a free thread
    # can create race conditions/deadlocks if the context manager itself
    # has its own internal pool (e.g. a database connection pool)
    # to avoid this we let __exit__ run without a capacity limit
    # since we're creating a new limiter for each call, any non-zero limit
    # works (1 is arbitrary)
    exit_limiter = CapacityLimiter(1)
    # AnyIO cancellation waits for a running worker, but not for worker capacity.
    # Only call __exit__ after __enter__ has succeeded.
    value = await run_in_threadpool(cm.__enter__)
    try:
        yield value
    except BaseException as e:
        with CancelScope(shield=True):
            ok = bool(
                await anyio.to_thread.run_sync(
                    cm.__exit__, type(e), e, e.__traceback__, limiter=exit_limiter
                )
            )
        if not ok:
            raise
    else:
        with CancelScope(shield=True):
            await anyio.to_thread.run_sync(
                cm.__exit__, None, None, None, limiter=exit_limiter
            )


@asynccontextmanager
async def _asynccontextmanager_with_shielded_exit(
    cm: AbstractAsyncContextManager[_T], cleanup_scope: CancelScope
) -> AsyncGenerator[_T, None]:
    # The shared scope was entered before the dependency, so exiting a scope
    # opened by the dependency still follows LIFO order.
    was_shielded = cleanup_scope.shield
    try:
        async with cm as value:
            try:
                yield value
            finally:
                cleanup_scope.shield = True
    finally:
        cleanup_scope.shield = was_shielded
    # A task group can suppress cancellation while its parent is shielded.
    await checkpoint_if_cancelled()


class _DependencyConcurrency:
    def __init__(self, max_concurrency: int) -> None:
        self.max_concurrency = max_concurrency

    def get_semaphore(self) -> Semaphore:
        semaphores = _dependency_semaphores.get(None)
        if semaphores is None:
            semaphores = WeakKeyDictionary()
            _dependency_semaphores.set(semaphores)

        semaphore = semaphores.get(self)
        if semaphore is None:
            semaphore = semaphores[self] = Semaphore(self.max_concurrency)
        return semaphore


@asynccontextmanager
async def _contextmanager_with_concurrency_limit(
    cm: AbstractAsyncContextManager[_T], semaphore: Semaphore
) -> AsyncGenerator[_T, None]:
    async with semaphore:
        # The wrapped generator handles cancellation-safe cleanup. Do not open
        # a cancel scope here: the dependency may own scopes that must exit first.
        async with cm as value:
            yield value
