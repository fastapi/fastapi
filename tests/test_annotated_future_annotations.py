"""Regression tests for Annotated forward refs with __future__ annotations.

See https://github.com/fastapi/fastapi/pull/15411
"""
from __future__ import annotations

from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


# ── Positive case: Annotated[ForwardRef, Depends()] before type definition ───


def _get_potato() -> Potato:
    return Potato(skin="brown", mass_g=300)


class Potato:
    def __init__(self, skin: str, mass_g: int):
        self.skin = skin
        self.mass_g = mass_g


@pytest.fixture(name="client_fwd_dep")
def client_fwd_dep_fixture() -> TestClient:
    app = FastAPI()

    @app.get("/potato")
    async def get_potato(
        potato: Annotated[Potato, Depends(_get_potato)],
    ) -> dict:
        # Potato must be resolved as a **dependency**, not a body field.
        return {"skin": potato.skin, "mass_g": potato.mass_g}

    @app.get("/potato-twice")
    async def get_potato_twice(
        a: Annotated[Potato, Depends(_get_potato)],
        b: Annotated[Potato, Depends(_get_potato)],
    ) -> dict:
        # Multiple deps with the same forward-ref'd type.
        return {"a_skin": a.skin, "b_skin": b.skin}

    return TestClient(app)


def test_annotated_fwd_ref_resolved_as_dependency(client_fwd_dep: TestClient):
    """Annotated[UndefinedType, Depends(...)] must be treated as a dep."""
    resp = client_fwd_dep.get("/potato")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"skin": "brown", "mass_g": 300}


def test_annotated_fwd_ref_no_body_required(client_fwd_dep: TestClient):
    """Sending no body must succeed (dep injection, not body parsing)."""
    resp = client_fwd_dep.get("/potato")
    assert resp.status_code == 200


def test_annotated_fwd_ref_multiple_deps(client_fwd_dep: TestClient):
    """Multiple forward-ref'd Annotated deps on the same route."""
    resp = client_fwd_dep.get("/potato-twice")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"a_skin": "brown", "b_skin": "brown"}


# ── OpenAPI schema sanity check ─────────────────────────────────────────────


def test_openapi_schema_no_body_params(client_fwd_dep: TestClient):
    """The dependency-injected param must NOT appear as a request body."""
    resp = client_fwd_dep.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    # /potato should have no requestBody (it's all dep-injected)
    pot_schema = schema["paths"]["/potato"]["get"]
    assert "requestBody" not in pot_schema
