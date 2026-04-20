import contextlib
import time
from collections.abc import Iterator

import anyio.to_thread
import pytest
from anyio import CapacityLimiter
from fastapi import concurrency


@pytest.fixture
def reset_teardown_limiter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset the teardown limiter before/after tests to avoid interference
    between different anyio backends."""
    monkeypatch.setattr(concurrency, "_teardown_limiter", CapacityLimiter(5))


@pytest.mark.anyio
@pytest.mark.usefixtures("reset_teardown_limiter")
async def test_run_in_teardown_threadpool() -> None:
    def func(x: int, y: int) -> int:
        return x + y

    result = await concurrency.run_in_teardown_threadpool(func, 1, y=2)
    assert result == 3


@pytest.mark.anyio
@pytest.mark.usefixtures("reset_teardown_limiter")
async def test_contextmanager_in_threadpool() -> None:
    @contextlib.contextmanager
    def context_manager() -> Iterator[str]:
        yield "entered"

    async with concurrency.contextmanager_in_threadpool(context_manager()) as result:
        assert result == "entered"


@pytest.mark.anyio
@pytest.mark.usefixtures("reset_teardown_limiter")
async def test_competing_acquire_release() -> None:
    """Check that the main threadpool does not block the teardown threadpool."""
    pool_size = anyio.to_thread.current_default_thread_limiter().total_tokens
    acquirable = False
    acquired = []

    def acquire() -> None:
        while not acquirable:
            time.sleep(0.001)
        acquired.append(True)

    def release() -> bool:
        nonlocal acquirable
        time.sleep(0.001)
        acquirable = True
        return acquirable

    async with anyio.create_task_group() as tg:
        for _ in range(pool_size):
            tg.start_soon(concurrency.run_in_threadpool, acquire)

        await anyio.sleep(0.001)

        # The threadpool should now be full of threads waiting to acquire
        # The release function should be able to run without being blocked by acquires
        await concurrency.run_in_teardown_threadpool(release)

    assert len(acquired) == pool_size
