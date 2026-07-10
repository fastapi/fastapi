from collections.abc import Generator
from contextlib import contextmanager

import pytest
from fastapi import Depends, FastAPI
from fastapi.concurrency import contextmanager_in_threadpool
from fastapi.testclient import TestClient

app = FastAPI()

state: dict[str, str] = {}


def reset_state() -> None:
    state.clear()


def gen_value() -> Generator[str, None, None]:
    state["phase"] = "started"
    try:
        yield "value"
    finally:
        state["phase"] = "finalized"


def gen_raises_before_yield() -> Generator[str, None, None]:
    raise ValueError("setup failed")
    yield  # pragma: no cover


def gen_raises_after_yield() -> Generator[str, None, None]:
    try:
        yield "value"
    finally:
        state["phase"] = "finalized"
        raise ValueError("cleanup failed")


def gen_swallows_body_error() -> Generator[str, None, None]:
    try:
        yield "value"
    except RuntimeError:
        state["caught"] = "yes"
        # swallowing here makes the underlying context manager`s __exit__
        # return True, i.e. request the exception to be suppressed.


@app.get("/value")
async def get_value(value: str = Depends(gen_value)) -> str:
    return value


@app.get("/setup-fail")
async def get_setup_fail(value: str = Depends(gen_raises_before_yield)) -> str:
    return value  # pragma: no cover


@app.get("/cleanup-fail")
async def get_cleanup_fail(value: str = Depends(gen_raises_after_yield)) -> str:
    return value


@app.get("/swallow")
async def get_swallow(value: str = Depends(gen_swallows_body_error)) -> str:
    raise RuntimeError("boom")


client = TestClient(app, raise_server_exceptions=False)


def test_sync_gen_dep_yields_value_and_finalizes() -> None:
    reset_state()
    response = client.get("/value")
    assert response.status_code == 200, response.text
    assert response.json() == "value"
    assert state["phase"] == "finalized"


def test_sync_gen_dep_setup_error_returns_500() -> None:
    reset_state()
    response = client.get("/setup-fail")
    assert response.status_code == 500, response.text


def test_sync_gen_dep_cleanup_error_after_success_does_not_break_response() -> None:
    reset_state()
    response = client.get("/cleanup-fail")
    assert response.status_code == 200, response.text
    assert state["phase"] == "finalized"


def test_sync_gen_dep_receives_body_error_in_teardown() -> None:
    reset_state()
    response = client.get("/swallow")
    # The endpoint error still surfaces as a server error (FastAPI`s error
    # middleware handles it before the exit-stack teardown runs), but the
    # dependency `except` clause proves the exception was delivered to the
    # context managers __exit__.
    assert response.status_code == 500, response.text
    assert state["caught"] == "yes"


# The suppression protocol of `contextmanager_in_threadpool` (whether __exit__
# returning True/False/None suppresses or re-raises the body exception) is not
# observable through the public API: FastAPI's error middleware converts the
# endpoint exception into a 500 before the dependency teardown's suppression
# decision can affect the response. A direct unit test is the only way to pin
# that part of the context manager protocol.


class ExitTracker:
    def __init__(self, exit_return: bool | None) -> None:
        self.exit_return = exit_return
        self.exit_called = False
        self.exit_args: tuple = ()

    def __enter__(self) -> str:
        return "value"

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool | None:
        self.exit_called = True
        self.exit_args = (exc_type, exc_val, exc_tb)
        return self.exit_return


@contextmanager
def raising_on_exit_cm() -> Generator[str, None, None]:
    yield "value"
    raise ValueError("error on exit")


@pytest.mark.anyio
async def test_exit_suppresses_exception_when_returns_true() -> None:
    tracker = ExitTracker(exit_return=True)
    async with contextmanager_in_threadpool(tracker):
        raise RuntimeError("should be suppressed")
    assert tracker.exit_called


@pytest.mark.anyio
@pytest.mark.parametrize("exit_return", [False, None])
async def test_exit_does_not_suppress(exit_return: bool | None) -> None:
    tracker = ExitTracker(exit_return=exit_return)
    with pytest.raises(RuntimeError, match="propagates"):
        async with contextmanager_in_threadpool(tracker):
            raise RuntimeError("propagates")
    assert tracker.exit_called


@pytest.mark.anyio
async def test_exception_raised_in_cm_after_yield_propagates() -> None:
    with pytest.raises(ValueError, match="error on exit"):
        async with contextmanager_in_threadpool(raising_on_exit_cm()):
            pass
