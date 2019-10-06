from typing import Dict

import pytest
from fastapi import Depends, FastAPI
from starlette.testclient import TestClient

app = FastAPI()
state = {
    "/async": "asyncgen not started",
    "/sync": "generator not started",
    "/async_raise": "asyncgen raise not started",
    "/sync_raise": "generator raise not started",
}

errors = []


async def get_state():
    return state


class AsyncDependencyError(Exception):
    pass


class SyncDependencyError(Exception):
    pass


class OtherDependencyError(Exception):
    pass


async def asyncgen_state(state: Dict[str, str] = Depends(get_state)):
    state["/async"] = "asyncgen started"
    yield state["/async"]
    state["/async"] = "asyncgen completed"


def generator_state(state: Dict[str, str] = Depends(get_state)):
    state["/sync"] = "generator started"
    yield state["/sync"]
    state["/sync"] = "generator completed"


async def asyncgen_state_try(state: Dict[str, str] = Depends(get_state)):
    state["/async_raise"] = "asyncgen raise started"
    try:
        yield state["/async_raise"]
    except AsyncDependencyError:
        errors.append("/async_raise")
    finally:
        state["/async_raise"] = "asyncgen raise finalized"


def generator_state_try(state: Dict[str, str] = Depends(get_state)):
    state["/sync_raise"] = "generator raise started"
    try:
        yield state["/sync_raise"]
    except SyncDependencyError:
        errors.append("/sync_raise")
    finally:
        state["/sync_raise"] = "generator raise finalized"


@app.get("/async")
async def get_async(state: str = Depends(asyncgen_state)):
    return state


@app.get("/sync")
async def get_sync(state: str = Depends(generator_state)):
    return state


@app.get("/async_raise")
async def get_async_raise(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_raise")
async def get_sync_raise(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/async_raise_other")
async def get_async_raise_other(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_raise_other")
async def get_sync_raise_other(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise OtherDependencyError()


client = TestClient(app)


def test_async_state():
    assert state["/async"] == f"asyncgen not started"
    response = client.get("/async")
    assert response.status_code == 200
    assert response.json() == f"asyncgen started"
    assert state["/async"] == f"asyncgen completed"


def test_sync_state():
    assert state["/sync"] == f"generator not started"
    response = client.get("/sync")
    assert response.status_code == 200
    assert response.json() == f"generator started"
    assert state["/sync"] == f"generator completed"


def test_async_raise_other():
    assert state["/async_raise"] == "asyncgen raise not started"
    with pytest.raises(OtherDependencyError):
        client.get("/async_raise_other")
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" not in errors


def test_sync_raise_other():
    assert state["/sync_raise"] == "generator raise not started"
    with pytest.raises(OtherDependencyError):
        client.get("/sync_raise_other")
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" not in errors


def test_async_raise():
    response = client.get("/async_raise")
    assert response.status_code == 500
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" in errors


def test_sync_raise():
    response = client.get("/sync_raise")
    assert response.status_code == 500
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" in errors
