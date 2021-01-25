from typing import Dict

from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.testclient import TestClient

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


async def asyncgen_state(
    state: Dict[str, str] = Depends(get_state, exit_before_response=True)
):
    state["/async"] = "asyncgen started"
    yield state["/async"]
    state["/async"] = "asyncgen completed"


def generator_state(
    state: Dict[str, str] = Depends(get_state, exit_before_response=True)
):
    state["/sync"] = "generator started"
    yield state["/sync"]
    state["/sync"] = "generator completed"


async def asyncgen_state_try(
    state: Dict[str, str] = Depends(get_state, exit_before_response=True)
):
    state["/async_raise"] = "asyncgen raise started"
    try:
        yield state["/async_raise"]
    except AsyncDependencyError:
        errors.append("/async_raise")
    finally:
        state["/async_raise"] = "asyncgen raise finalized"


def generator_state_try(
    state: Dict[str, str] = Depends(get_state, exit_before_response=True)
):
    state["/sync_raise"] = "generator raise started"
    try:
        yield state["/sync_raise"]
    except SyncDependencyError:
        errors.append("/sync_raise")
    finally:
        state["/sync_raise"] = "generator raise finalized"


async def context_a(state: dict = Depends(get_state, exit_before_response=True)):
    state["context_a"] = "started a"
    try:
        yield state
    finally:
        state["context_a"] = "finished a"


async def context_b(state: dict = Depends(context_a, exit_before_response=True)):
    state["context_b"] = "started b"
    try:
        yield state
    finally:
        state["context_b"] = f"finished b with a: {state['context_a']}"


@app.get("/async")
async def get_async(state: str = Depends(asyncgen_state, exit_before_response=True)):
    return state


@app.get("/sync")
async def get_sync(state: str = Depends(generator_state, exit_before_response=True)):
    return state


@app.get("/async_raise")
async def get_async_raise(
    state: str = Depends(asyncgen_state_try, exit_before_response=True)
):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_raise")
async def get_sync_raise(
    state: str = Depends(generator_state_try, exit_before_response=True)
):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/async_raise_other")
async def get_async_raise_other(
    state: str = Depends(asyncgen_state_try, exit_before_response=True)
):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_raise_other")
async def get_sync_raise_other(
    state: str = Depends(generator_state_try, exit_before_response=True)
):
    assert state == "generator raise started"
    raise OtherDependencyError()


@app.get("/context_b")
async def get_context_b(state: dict = Depends(context_b, exit_before_response=True)):
    return state


@app.get("/context_b_raise")
async def get_context_b_raise(
    state: dict = Depends(context_b, exit_before_response=True)
):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/context_b_bg")
async def get_context_b_bg(
    tasks: BackgroundTasks, state: dict = Depends(context_b, exit_before_response=True)
):
    async def bg(state: dict):
        state["bg"] = f"bg set - b: {state['context_b']} - a: {state['context_a']}"

    tasks.add_task(bg, state)
    return state


# Sync versions


@app.get("/sync_async")
def get_sync_async(state: str = Depends(asyncgen_state, exit_before_response=True)):
    return state


@app.get("/sync_sync")
def get_sync_sync(state: str = Depends(generator_state, exit_before_response=True)):
    return state


@app.get("/sync_async_raise")
def get_sync_async_raise(
    state: str = Depends(asyncgen_state_try, exit_before_response=True)
):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_sync_raise")
def get_sync_sync_raise(
    state: str = Depends(generator_state_try, exit_before_response=True)
):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/sync_async_raise_other")
def get_sync_async_raise_other(
    state: str = Depends(asyncgen_state_try, exit_before_response=True)
):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_sync_raise_other")
def get_sync_sync_raise_other(
    state: str = Depends(generator_state_try, exit_before_response=True)
):
    assert state == "generator raise started"
    raise OtherDependencyError()


@app.get("/sync_context_b")
def get_sync_context_b(state: dict = Depends(context_b, exit_before_response=True)):
    return state


@app.get("/sync_context_b_raise")
def get_sync_context_b_raise(
    state: dict = Depends(context_b, exit_before_response=True)
):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/sync_context_b_bg")
async def get_sync_context_b_bg(
    tasks: BackgroundTasks, state: dict = Depends(context_b, exit_before_response=True)
):
    async def bg(state: dict):
        print("asdas")
        state[
            "sync_bg"
        ] = f"sync_bg set - b: {state['context_b']} - a: {state['context_a']}"

    tasks.add_task(bg, state)
    return state


client = TestClient(app, raise_server_exceptions=False)


def test_async_state():
    assert state["/async"] == "asyncgen not started"
    response = client.get("/async")
    assert response.status_code == 200, response.text
    assert response.json() == "asyncgen started"
    assert state["/async"] == "asyncgen completed"


def test_sync_state():
    assert state["/sync"] == "generator not started"
    response = client.get("/sync")
    assert response.status_code == 200, response.text
    assert response.json() == "generator started"
    assert state["/sync"] == "generator completed"


def test_async_raise_other():
    assert state["/async_raise"] == "asyncgen raise not started"
    response = client.get("/async_raise_other")
    assert response.status_code == 500
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" not in errors


def test_sync_raise_other():
    assert state["/sync_raise"] == "generator raise not started"
    response = client.get("/sync_raise_other")
    assert response.status_code == 500
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" not in errors


def test_async_raise():
    response = client.get("/async_raise")
    assert response.status_code == 500, response.text
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" in errors
    errors.clear()


def test_context_b():
    response = client.get("/context_b")
    data = response.json()
    assert data["context_b"] == "finished b with a: started a"
    assert data["context_a"] == "finished a"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_context_b_raise():
    response = client.get("/context_b_raise")
    assert response.status_code == 500
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_background_tasks():
    response = client.get("/context_b_bg")
    data = response.json()
    assert data["context_b"] == "finished b with a: started a"
    assert data["context_a"] == "finished a"
    assert data["bg"] == "not set"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"
    assert state["bg"] == "bg set - b: finished b with a: started a - a: finished a"


def test_sync_raise():
    response = client.get("/sync_raise")
    assert response.status_code == 500, response.text
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" in errors
    errors.clear()


def test_sync_async_state():
    response = client.get("/sync_async")
    assert response.status_code == 200, response.text
    assert response.json() == "asyncgen started"
    assert state["/async"] == "asyncgen completed"


def test_sync_sync_state():
    response = client.get("/sync_sync")
    assert response.status_code == 200, response.text
    assert response.json() == "generator started"
    assert state["/sync"] == "generator completed"


def test_sync_async_raise_other():
    response = client.get("/sync_async_raise_other")
    assert response.status_code == 500
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" not in errors


def test_sync_sync_raise_other():
    response = client.get("/sync_sync_raise_other")
    assert response.status_code == 500
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" not in errors


def test_sync_async_raise():
    response = client.get("/sync_async_raise")
    assert response.status_code == 500, response.text
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" in errors
    errors.clear()


def test_sync_sync_raise():
    response = client.get("/sync_sync_raise")
    assert response.status_code == 500, response.text
    assert state["/sync_raise"] == "generator raise finalized"
    assert "/sync_raise" in errors
    errors.clear()


def test_sync_context_b():
    response = client.get("/sync_context_b")
    data = response.json()
    assert data["context_b"] == "finished b with a: started a"
    assert data["context_a"] == "finished a"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_sync_context_b_raise():
    response = client.get("/sync_context_b_raise")
    assert response.status_code == 500
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"


def test_sync_background_tasks():
    response = client.get("/sync_context_b_bg")
    data = response.json()
    assert data["context_b"] == "finished b with a: started a"
    assert data["context_a"] == "finished a"
    assert data["sync_bg"] == "not set"
    assert state["context_b"] == "finished b with a: started a"
    assert state["context_a"] == "finished a"
    assert (
        state["sync_bg"]
        == "sync_bg set - b: finished b with a: started a - a: finished a"
    )
