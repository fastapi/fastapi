from typing import Dict

import pytest
from fastapi import Depends
from starlette.testclient import TestClient

from dependencies.tutorial008 import app

state = {"/async": "asyncgen not started", "/sync": "generator not started"}


async def get_state():
    return state


async def asyncgen_state(state: Dict[str, str] = Depends(get_state)) -> str:
    state["/async"] = "asyncgen started"
    yield state["/async"]
    state["/async"] = "asyncgen completed"


async def generator_state(state: Dict[str, str] = Depends(get_state)) -> str:
    state["/sync"] = "generator started"
    yield state["/sync"]
    state["/sync"] = "generator completed"


async def invalid_asyncgen_no_yield() -> int:
    if False:
        yield
    return


async def invalid_asyncgen_multi_yield() -> int:
    yield 1
    yield 2


def invalid_generator_no_yield() -> int:
    if False:
        yield
    return


def invalid_generator_multi_yield() -> int:
    yield 1
    yield 2


@app.get("/async")
async def get_async(state: str = Depends(asyncgen_state)):
    return state


@app.get("/sync")
async def get_sync(state: str = Depends(generator_state)):
    return state


@app.get("/no-yield/async")
async def error_no_yield_async(invalid: int = Depends(invalid_asyncgen_no_yield)):
    pass  # pragma: no cover


@app.get("/multi-yield/async")
async def error_multi_yield_async(invalid: int = Depends(invalid_asyncgen_multi_yield)):
    pass  # pragma: no cover


@app.get("/no-yield/sync")
async def error_no_yield_sync(count: int = Depends(invalid_generator_no_yield)):
    pass  # pragma: no cover


@app.get("/multi-yield/sync")
async def error_multi_yield_sync(count: int = Depends(invalid_generator_multi_yield)):
    pass  # pragma: no cover


client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint,label", [("/async", "asyncgen"), ("/sync", "generator")]
)
def test_async_state(endpoint, label):
    assert state[endpoint] == f"{label} not started"

    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json() == f"{label} started"

    assert state[endpoint] == f"{label} completed"


@pytest.mark.parametrize(
    "endpoint,message",
    [
        ("/no-yield/async", "generator didn't yield"),
        ("/no-yield/sync", "generator didn't yield"),
        ("/multi-yield/async", "generator didn't stop"),
        ("/multi-yield/sync", "generator didn't stop"),
    ],
)
def test_invalid_context_dependency(endpoint, message):
    with pytest.raises(RuntimeError) as exc_info:
        client.get(endpoint)
    assert str(exc_info.value) == message


def test_docs():
    response = client.get("/get-db-check")
    assert response.status_code == 200
    assert response.content == b"true"
