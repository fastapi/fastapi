import pytest

# The example imports `httpx2` directly, so skip it in the CI job that
# uninstalls `httpx2` to exercise Starlette's deprecated `httpx` fallback.
pytest.importorskip("httpx2")

from docs_src.async_tests.app_a_py310.test_main import test_root  # noqa: E402


@pytest.mark.anyio
async def test_async_testing():
    await test_root()
