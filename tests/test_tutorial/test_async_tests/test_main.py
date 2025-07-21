import pytest

from docs_src.async_tests.test_main import test_root


@pytest.mark.anyio
async def test_async_testing():
    await test_root()
