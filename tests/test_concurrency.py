from contextlib import contextmanager
from threading import BoundedSemaphore
from time import sleep
from typing import Iterator

import anyio
import pytest
from fastapi.concurrency import contextmanager_in_threadpool


@contextmanager
def slow_cm(db_pool: BoundedSemaphore) -> Iterator[None]:
    print("acquiring db token")
    with db_pool:
        sleep(0)
        yield
        sleep(0)
        print("releasing db token")


async def run_cm(db_pool: BoundedSemaphore) -> None:
    print("acquiring therad token")
    async with contextmanager_in_threadpool(slow_cm(db_pool)):
        await anyio.sleep(0)


@pytest.mark.anyio
async def test_contextmanager_in_threadpool_does_not_deadlock() -> None:
    # simulate a synchronous DB connection pool
    # first we acquire a token from the thread pool
    # then we acquire a token from the db pool
    # previously __exit__ was run in a different thread
    # so in order to release the db pool token we needed another
    # thread token
    # but if we had already exhausted thead tokens then we can't run __exit__
    # and so we can't free up a db pool token
    # resulting in a deadlock
    limiter = anyio.to_thread.current_default_thread_limiter()
    total_tokens = int(limiter.total_tokens)
    db_pool = BoundedSemaphore(1)
    with anyio.fail_after(1):  # deadlock
        async with anyio.create_task_group() as tg:
            for _ in range(total_tokens * 2):
                tg.start_soon(run_cm, db_pool)
