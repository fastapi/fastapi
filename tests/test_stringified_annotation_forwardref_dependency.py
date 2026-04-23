from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=10)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"color": potato.color, "size": potato.size}


@dataclass
class Potato:
    color: str
    size: int


client = TestClient(app)


def test_stringified_annotated_forwardref_dependency():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"color": "red", "size": 10}


def test_stringified_annotated_forwardref_dependency_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
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
