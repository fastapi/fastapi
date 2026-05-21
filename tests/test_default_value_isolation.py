"""
Tests that mutable default values for request parameters are properly isolated
between requests (not shared), and that immutable defaults are returned directly
without unnecessary deepcopy calls.
"""

from typing import Annotated
from unittest.mock import patch

import pytest
from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

# ── Mutable list default ────────────────────────────────────────────────────

_mutable_default_list: list[str] = []


@app.get("/items")
async def read_items(
    tags: Annotated[list[str], Query()] = _mutable_default_list,
) -> dict[str, list[str]]:
    # Simulate in-place mutation that could bleed between requests
    tags.append("added-in-handler")
    return {"tags": tags}


client = TestClient(app)


def test_mutable_list_default_not_shared_across_requests() -> None:
    """Each request with no 'tags' param gets its own fresh list, not the module-level default."""
    r1 = client.get("/items")
    assert r1.status_code == 200
    assert r1.json() == {"tags": ["added-in-handler"]}

    r2 = client.get("/items")
    assert r2.status_code == 200
    # If the default was shared, r2 would see ["added-in-handler", "added-in-handler"]
    assert r2.json() == {"tags": ["added-in-handler"]}

    # The module-level list must remain untouched
    assert _mutable_default_list == []


# ── Immutable defaults ───────────────────────────────────────────────────────


@app.get("/greet")
async def greet(name: str | None = None) -> dict[str, str | None]:
    return {"name": name}


@app.get("/count")
async def count(n: int = 0) -> dict[str, int]:
    return {"n": n}


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/greet", {"name": None}),
        ("/count", {"n": 0}),
    ],
)
def test_immutable_defaults_returned_correctly(path: str, expected: dict) -> None:  # type: ignore[type-arg]
    """Immutable defaults (None, int) are returned correctly without deepcopy."""
    r = client.get(path)
    assert r.status_code == 200
    assert r.json() == expected


def test_immutable_defaults_skip_deepcopy() -> None:
    """deepcopy must NOT be called when the field default is an immutable type."""
    with patch("fastapi.dependencies.utils.deepcopy") as mock_deepcopy:
        client.get("/greet")  # default=None  — immutable
        client.get("/count")  # default=0     — immutable

    assert mock_deepcopy.call_count == 0, (
        f"deepcopy called {mock_deepcopy.call_count} time(s) for immutable defaults; "
        "should be 0"
    )


# ── default_factory on request params ────────────────────────────────────────

# List-based counter: thread-safe for append/len without needing a global int + lock.
_factory_calls: list[None] = []


def counting_list_factory() -> list[str]:
    _factory_calls.append(None)
    return []


@app.get("/factory-default")
async def factory_default(
    tags: Annotated[list[str], Query(default_factory=counting_list_factory)],
) -> dict[str, list[str]]:
    tags.append("added-in-handler")
    return {"tags": tags}


# Scalar (non-sequence) param with default_factory — exercises the
# _validate_value_with_model_field branch (value is None path).
@app.get("/factory-scalar")
async def factory_scalar(
    name: str = Query(default_factory=lambda: "world"),
) -> dict[str, str]:
    return {"name": name}


# Body field with default_factory — exercises _validate_value_with_model_field
# when body_to_process is None (no request body sent).
@app.post("/factory-body")
async def factory_body(
    tags: Annotated[list[str], Body(default_factory=list)],
) -> dict[str, list[str]]:
    tags.append("added-in-handler")
    return {"tags": tags}


def test_default_factory_on_query_param_gives_fresh_object_per_request() -> None:
    """default_factory is called each request; mutations don't bleed between requests."""
    r1 = client.get("/factory-default")
    assert r1.status_code == 200
    assert r1.json() == {"tags": ["added-in-handler"]}

    r2 = client.get("/factory-default")
    assert r2.status_code == 200
    assert r2.json() == {"tags": ["added-in-handler"]}


def test_default_factory_scalar_param() -> None:
    """default_factory works for scalar (non-sequence) params."""
    r = client.get("/factory-scalar")
    assert r.status_code == 200
    assert r.json() == {"name": "world"}


def test_default_factory_on_body_param_gives_fresh_object_per_request() -> None:
    """Body field with default_factory gives fresh object when no body is sent."""
    r1 = client.post("/factory-body")
    assert r1.status_code == 200
    assert r1.json() == {"tags": ["added-in-handler"]}

    r2 = client.post("/factory-body")
    assert r2.status_code == 200
    assert r2.json() == {"tags": ["added-in-handler"]}


def test_default_factory_skips_deepcopy() -> None:
    """When default_factory is set, deepcopy must NOT be called — factory already creates fresh object."""
    _factory_calls.clear()

    # Patch the name in the module's own namespace (not copy.deepcopy) so the mock
    # intercepts the already-bound reference used by the two call sites.
    with patch("fastapi.dependencies.utils.deepcopy") as mock_deepcopy:
        client.get("/factory-default")
        client.get("/factory-scalar")

    assert mock_deepcopy.call_count == 0, (
        f"deepcopy called {mock_deepcopy.call_count} time(s) for default_factory param; "
        "factory already produces a fresh object — deepcopy is redundant"
    )
    assert len(_factory_calls) >= 1, "factory must be called at least once per request"
