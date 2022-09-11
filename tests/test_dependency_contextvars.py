from contextvars import ContextVar
from typing import Any, Awaitable, Callable, Dict, Optional

from fastapi import Depends, FastAPI, Request, Response
from fastapi.testclient import TestClient

legacy_request_state_context_var: ContextVar[Optional[Dict[str, Any]]] = ContextVar(
    "legacy_request_state_context_var", default=None
)

app = FastAPI()


async def set_up_request_state_dependency():
    request_state = {"user": "deadpond"}
    contextvar_token = legacy_request_state_context_var.set(request_state)
    yield request_state
    legacy_request_state_context_var.reset(contextvar_token)


@app.middleware("http")
async def custom_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    response = await call_next(request)
    response.headers["custom"] = "foo"
    return response


@app.get("/user", dependencies=[Depends(set_up_request_state_dependency)])
def get_user():
    request_state = legacy_request_state_context_var.get()
    assert request_state
    return request_state["user"]


client = TestClient(app)


def test_dependency_contextvars():
    """
    Check that custom middlewares don't affect the contextvar context for dependencies.

    The code before yield and the code after yield should be run in the same contextvar
    context, so that request_state_context_var.reset(contextvar_token).

    If they are run in a different context, that raises an error.
    """
    response = client.get("/user")
    assert response.json() == "deadpond"
    assert response.headers["custom"] == "foo"
