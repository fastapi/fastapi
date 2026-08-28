"""Tests for logging ResponseValidationError from streaming endpoint serializers.

Regression tests for the bug where ResponseValidationError raised during
serialization of a yielded item was silently swallowed with no log output.

Covers:
- SSE async generator
- SSE sync generator
- JSONL async generator
- JSONL sync generator

For each variant, verifies:
1. Valid streams are unaffected (no spurious ERROR logs, correct body).
2. Invalid items trigger an ERROR-level log entry with exc_info attached.
3. The exception still propagates (is not swallowed).
"""

import logging
from collections.abc import AsyncIterable, Iterable

import pytest

try:
    from builtins import ExceptionGroup
except ImportError:  # pragma: no cover
    from exceptiongroup import ExceptionGroup

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str


# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI()


@app.get("/sse/valid", response_class=EventSourceResponse)
async def sse_valid() -> AsyncIterable[Item]:
    yield Item(id=1, name="ok")
    yield Item(id=2, name="also-ok")


@app.get("/sse/valid-sync", response_class=EventSourceResponse)
def sse_valid_sync() -> Iterable[Item]:
    yield Item(id=1, name="ok")
    yield Item(id=2, name="also-ok")


@app.get("/sse/invalid", response_class=EventSourceResponse)
async def sse_invalid() -> AsyncIterable[Item]:
    # "id" must be an int; passing a non-coercible string causes
    # ResponseValidationError during serialization.
    yield {"id": "NOT_AN_INT", "name": "bad"}  # type: ignore[misc]


@app.get("/sse/invalid-sync", response_class=EventSourceResponse)
def sse_invalid_sync() -> Iterable[Item]:
    yield {"id": "NOT_AN_INT", "name": "bad"}  # type: ignore[misc]


@app.get("/jsonl/valid")
async def jsonl_valid() -> AsyncIterable[Item]:
    yield Item(id=1, name="ok")
    yield Item(id=2, name="also-ok")


@app.get("/jsonl/valid-sync")
def jsonl_valid_sync() -> Iterable[Item]:
    yield Item(id=1, name="ok")
    yield Item(id=2, name="also-ok")


@app.get("/jsonl/invalid")
async def jsonl_invalid() -> AsyncIterable[Item]:
    yield {"id": "NOT_AN_INT", "name": "bad"}  # type: ignore[misc]


@app.get("/jsonl/invalid-sync")
def jsonl_invalid_sync() -> Iterable[Item]:
    yield {"id": "NOT_AN_INT", "name": "bad"}  # type: ignore[misc]


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture(name="raising_client")
def raising_client_fixture():
    """Client that lets ResponseValidationError propagate into the test."""
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ── Valid stream tests (no regressions) ──────────────────────────────────────


def test_sse_valid_stream_unaffected(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """Valid SSE streams must still produce correct output and zero ERROR logs."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        response = client.get("/sse/valid")

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    data_lines = [
        line for line in response.text.splitlines() if line.startswith("data: ")
    ]
    assert len(data_lines) == 2
    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records == [], (
        f"Unexpected ERROR logs on valid stream: {error_records}"
    )


def test_jsonl_valid_stream_unaffected(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """Valid JSONL streams must still produce correct output and zero ERROR logs."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        response = client.get("/jsonl/valid")

    assert response.status_code == 200
    assert "application/jsonl" in response.headers["content-type"]
    lines = [line for line in response.text.splitlines() if line.strip()]
    assert len(lines) == 2
    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records == [], (
        f"Unexpected ERROR logs on valid stream: {error_records}"
    )


def test_valid_sse_produces_no_error_logs(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """Sync valid SSE produces no spurious ERROR log."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        response = client.get("/sse/valid-sync")
    assert response.status_code == 200
    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records == []


def test_valid_jsonl_produces_no_error_logs(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """Sync valid JSONL produces no spurious ERROR log."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        response = client.get("/jsonl/valid-sync")
    assert response.status_code == 200
    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records == []


# ── Invalid item logging tests ────────────────────────────────────────────────


def test_sse_invalid_item_is_logged(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """ResponseValidationError in async SSE serializer must emit an ERROR log with exc_info."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        client.get("/sse/invalid")

    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records, (
        "Expected at least one ERROR log record for SSE validation failure"
    )
    record = error_records[0]
    assert record.exc_info is not None, "ERROR log must carry exc_info (full traceback)"
    assert "ResponseValidationError" in record.getMessage() or issubclass(
        record.exc_info[0],
        ResponseValidationError,  # type: ignore[index]
    ), "ERROR log message or exc_info must reference ResponseValidationError"


def test_jsonl_invalid_item_is_logged(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """ResponseValidationError in async JSONL serializer must emit an ERROR log with exc_info."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        client.get("/jsonl/invalid")

    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records, (
        "Expected at least one ERROR log record for JSONL validation failure"
    )
    record = error_records[0]
    assert record.exc_info is not None, "ERROR log must carry exc_info (full traceback)"
    assert "ResponseValidationError" in record.getMessage() or issubclass(
        record.exc_info[0],
        ResponseValidationError,  # type: ignore[index]
    ), "ERROR log message or exc_info must reference ResponseValidationError"


def test_sse_invalid_item_logged_sync(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """ResponseValidationError in sync SSE serializer must emit an ERROR log with exc_info."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        client.get("/sse/invalid-sync")

    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records, "Expected ERROR log for sync SSE validation failure"
    assert error_records[0].exc_info is not None


def test_jsonl_invalid_item_logged_sync(
    client: TestClient, caplog: pytest.LogCaptureFixture
):
    """ResponseValidationError in sync JSONL serializer must emit an ERROR log with exc_info."""
    with caplog.at_level(logging.ERROR, logger="fastapi"):
        client.get("/jsonl/invalid-sync")

    error_records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert error_records, "Expected ERROR log for sync JSONL validation failure"
    assert error_records[0].exc_info is not None


# ── Exception propagation tests ───────────────────────────────────────────────


def test_sse_invalid_item_propagates(raising_client: TestClient):
    """ResponseValidationError from async SSE must still propagate (not be swallowed).

    The SSE _producer task runs inside an anyio task group, so the error is
    wrapped in an ExceptionGroup when it escapes the group boundary.
    """
    # anyio task group wraps the sub-task exception in an ExceptionGroup
    with pytest.raises((ResponseValidationError, ExceptionGroup)):
        raising_client.get("/sse/invalid")


def test_jsonl_invalid_item_propagates(raising_client: TestClient):
    """ResponseValidationError from async JSONL must still propagate (not be swallowed)."""
    with pytest.raises(ResponseValidationError):
        raising_client.get("/jsonl/invalid")
