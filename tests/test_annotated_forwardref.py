# IMPORTANT: This future import MUST be at the top of the module.
# It is what causes annotations to be stored as strings (ForwardRef),
# which is exactly the bug scenario described in issue #13056.
from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


# ── App setup ─────────────────────────────────────────────────────────────────


app = FastAPI()


@dataclass
class Potato:
    color: str
    size: int


def get_potato() -> Potato:
    return Potato(color="red", size=10)


# The annotation "Potato" is a string here because of `from __future__ import
# annotations`.  Before the fix, FastAPI would fail to resolve it when it is
# wrapped inside Annotated[...].
@app.get("/")
def read_root(potato: Annotated[Potato, Depends(get_potato)]) -> dict:
    return {"color": potato.color, "size": potato.size}


client = TestClient(app)


# ── Tests ──────────────────────────────────────────────────────────────────────


def test_annotated_forwardref_response() -> None:
    """Endpoint using Annotated[ForwardRef, Depends(...)] must return 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"color": "red", "size": 10}


def test_annotated_forwardref_openapi_schema() -> None:
    """OpenAPI schema must be generated without errors and must not leak ForwardRef."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema_text = response.text
    assert "ForwardRef" not in schema_text, (
        "Unresolved ForwardRef leaked into the OpenAPI schema"
    )
