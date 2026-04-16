from collections.abc import Iterator
from typing import Any

import anyio
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


@pytest.mark.parametrize(
    "limit, anti_deadlock_reserve, error_kind",
    [
        ("not an int", 2, TypeError),
        (10, "not an int", TypeError),
        (1, 0, ValueError),
        (10, 0, ValueError),
        (10, 9, ValueError),
    ],
)
def test_set_thread_limit_invalid_args(
    limit: Any, anti_deadlock_reserve: Any, error_kind: type[Exception]
) -> None:
    with pytest.raises(error_kind):
        concurrency.set_thread_limit(limit, anti_deadlock_reserve)


@pytest.mark.anyio
async def test_set_thread_limit(_reset_capacity_limiter: None) -> None:
    original_total_tokens = (
        anyio.to_thread.current_default_thread_limiter().total_tokens
    )

    try:
        concurrency.set_thread_limit(10, anti_deadlock_reserve=2)
        assert concurrency._anti_deadlock_capacity_limiter.total_tokens == 8
        assert anyio.to_thread.current_default_thread_limiter().total_tokens == 10
    finally:
        # Restore original settings to avoid affecting other tests
        anyio.to_thread.current_default_thread_limiter().total_tokens = (
            original_total_tokens
        )
