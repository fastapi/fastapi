from typing import Dict

from fastapi import Depends, FastAPI
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

async def asyncgen_state_try(state: Dict[str, str] = Depends(get_state)):
    state["/async_raise"] = "asyncgen raise started"
    try:
        yield state["/async_raise"]
    except AsyncDependencyError:
        errors.append("/async_raise")
    finally:
        state["/async_raise"] = "asyncgen raise finalized"



@app.get("/async_raise")
async def get_async_raise(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


client = TestClient(app)



def test_async_raise():
    response = client.get("/async_raise")
    assert response.status_code == 500, response.text
    assert state["/async_raise"] == "asyncgen raise finalized"
    assert "/async_raise" in errors
    errors.clear()
