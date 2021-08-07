from contextlib import contextmanager

import pytest
from fastapi.concurrency import contextmanager_in_threadpool


@pytest.mark.asyncio
async def test_cm_in_threadpool():
    state = {}

    @contextmanager
    def cm():
        yield 1234
        state["cleanup"] = "run"

    async with contextmanager_in_threadpool(cm()) as val:
        assert val == 1234
    assert state == {"cleanup": "run"}
