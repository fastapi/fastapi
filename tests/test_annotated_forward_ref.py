from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI
from inline_snapshot import snapshot

# Simulate the real-world bug: Potato is defined AFTER the route decorator
# under `from __future__ import annotations`.

app = FastAPI()


def get_potato():
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}


from dataclasses import dataclass  # noqa: E402


@dataclass
class Potato:
    color: str
    size: int


def test_forward_ref_annotated_depends():
    from fastapi.testclient import TestClient

    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"color": "red", "size": 10}


def test_forward_ref_annotated_depends_openapi():
    from fastapi.testclient import TestClient

    client = TestClient(app)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200, resp.text
    assert resp.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Read Root",
                        "operationId": "read_root__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                }
            },
        }
    )
