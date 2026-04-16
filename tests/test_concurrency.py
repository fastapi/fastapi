from collections.abc import Iterator

import pytest
from fastapi import concurrency


@pytest.fixture
def _reset_capacity_limiter() -> Iterator[None]:
    # Reset the capacity limiter before each test to ensure a clean slate
    concurrency._anti_deadlock_capacity_limiter = None
    yield
    concurrency._anti_deadlock_capacity_limiter = None


@pytest.mark.anyio
async def test_run_in_threadpool(_reset_capacity_limiter: None) -> None:
    def blocking_function(x: int, y: int) -> int:
        return x + y

    result = await concurrency.run_in_threadpool(blocking_function, 1, y=2)
    assert result == 3


@pytest.mark.anyio
async def test_iterate_in_threadpool(_reset_capacity_limiter: None) -> None:
    result = []
    async for item in concurrency.iterate_in_threadpool(range(5)):
        result.append(item)

    assert result == [0, 1, 2, 3, 4]
