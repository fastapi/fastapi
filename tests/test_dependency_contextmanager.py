from typing import Dict

import pytest
from fastapi import BackgroundTasks, Depends, FastAPI
from starlette.testclient import TestClient

app = FastAPI()
state = {
    "/async": "asyncgen not started",
    "/sync": "generator not started",
    "/async_raise": "asyncgen raise not started",
    "/sync_raise": "generator raise not started",
    "context_a": "not started a",
    "context_b": "not started b",
    "bg": "not set",
    "sync_bg": "not set",
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


async def context_a(state: dict = Depends(get_state)):
    state["context_a"] = "started a"
    try:
        yield state
    finally:
        state["context_a"] = "finished a"


async def context_b(state: dict = Depends(context_a)):
    state["context_b"] = "started b"
    try:
        yield state
    finally:
        state["context_b"] = f"finished b with a: {state['context_a']}"


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


@app.get("/context_b")
async def get_context_b(state: dict = Depends(context_b)):
    return state


@app.get("/context_b_raise")
async def get_context_b_raise(state: dict = Depends(context_b)):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/context_b_bg")
async def get_context_b_bg(tasks: BackgroundTasks, state: dict = Depends(context_b)):
    async def bg(state: dict):
        state["bg"] = f"bg set - b: {state['context_b']} - a: {state['context_a']}"

    tasks.add_task(bg, state)
    return state


# Sync versions


@app.get("/sync_async")
def get_sync_async(state: str = Depends(asyncgen_state)):
    return state


@app.get("/sync_sync")
def get_sync_sync(state: str = Depends(generator_state)):
    return state


@app.get("/sync_async_raise")
def get_sync_async_raise(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_sync_raise")
def get_sync_sync_raise(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/sync_async_raise_other")
def get_sync_async_raise_other(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_sync_raise_other")
def get_sync_sync_raise_other(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise OtherDependencyError()


@app.get("/sync_context_b")
def get_sync_context_b(state: dict = Depends(context_b)):
    return state


@app.get("/sync_context_b_raise")
def get_sync_context_b_raise(state: dict = Depends(context_b)):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/sync_context_b_bg")
async def get_sync_context_b_bg(
    tasks: BackgroundTasks, state: dict = Depends(context_b)
):
    async def bg(state: dict):
        state[
            "sync_bg"
        ] = f"sync_bg set - b: {state['context_b']} - a: {state['context_a']}"

    tasks.add_task(bg, state)
    return state


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
    errors.clear()


def test_context_b():
    response = client.get("/context_b")
    data = response.json()
    assert data["context_b"] == "started b"
    assert data["context_a"] == "started a"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_context_b_raise():
    with pytest.raises(OtherDependencyError):
        client.get("/context_b_raise")
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_background_tasks():
    response = client.get("/context_b_bg")
    data = response.json()
    assert data["context_b"] == "started b"
    assert data["context_a"] == "started a"
    assert data["bg"] == "not set"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"
    assert state["bg"] == "bg set - b: started b - a: started a"


def test_sync_raise():
    response = client.get("/sync_raise")
    assert response.status_code == 500
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" in errors
    errors.clear()


def test_sync_async_state():
    response = client.get("/sync_async")
    assert response.status_code == 200
    assert response.json() == f"asyncgen started"
    assert state["/async"] == f"asyncgen completed"


def test_sync_sync_state():
    response = client.get("/sync_sync")
    assert response.status_code == 200
    assert response.json() == f"generator started"
    assert state["/sync"] == f"generator completed"


def test_sync_async_raise_other():
    with pytest.raises(OtherDependencyError):
        client.get("/sync_async_raise_other")
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" not in errors


def test_sync_sync_raise_other():
    with pytest.raises(OtherDependencyError):
        client.get("/sync_sync_raise_other")
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" not in errors


def test_sync_async_raise():
    response = client.get("/sync_async_raise")
    assert response.status_code == 500
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" in errors
    errors.clear()


def test_sync_sync_raise():
    response = client.get("/sync_sync_raise")
    assert response.status_code == 500
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" in errors
    errors.clear()


def test_sync_context_b():
    response = client.get("/sync_context_b")
    data = response.json()
    assert data["context_b"] == "started b"
    assert data["context_a"] == "started a"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_sync_context_b_raise():
    with pytest.raises(OtherDependencyError):
        client.get("/sync_context_b_raise")
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_sync_background_tasks():
    response = client.get("/sync_context_b_bg")
    data = response.json()
    assert data["context_b"] == "started b"
    assert data["context_a"] == "started a"
    assert data["sync_bg"] == "not set"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"
    assert state["sync_bg"] == "sync_bg set - b: started b - a: started a"
