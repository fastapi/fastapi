import pytest
from fastapi import FastAPI, Request
from fastapi.middleware import BodySizeLimitMiddleware
from starlette.testclient import TestClient


def make_app(limit: int) -> FastAPI:
    app = FastAPI()
    app.add_middleware(BodySizeLimitMiddleware, max_body_size=limit)

    @app.post("/echo")
    async def echo(request: Request):
        data = await request.body()
        return {"len": len(data)}

    return app


def test_small_body_passes():
    app = make_app(limit=16)
    client = TestClient(app)
    r = client.post("/echo", data=b"x" * 8)
    assert r.status_code == 200
    assert r.json()["len"] == 8


def test_large_body_rejected_with_413():
    app = make_app(limit=16)
    client = TestClient(app)
    r = client.post("/echo", data=b"x" * 64)
    assert r.status_code == 413
    assert b"Payload Too Large" in r.content
