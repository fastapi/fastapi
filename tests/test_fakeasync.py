import pytest
from fastapi.concurrency import _fake_asynccontextmanager


@_fake_asynccontextmanager
def never_run():
    pass  # pragma: no cover


def test_fake_async():
    with pytest.raises(RuntimeError):
        never_run()
