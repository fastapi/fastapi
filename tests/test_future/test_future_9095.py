from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request

from ..utils import needs_py310

app = FastAPI()

client = TestClient(app)


class Test:
    def __call__(self, request: Request):
        return "test"


@needs_py310
def test_call():
    @app.get("/test/")
    def call(test: str = Depends(Test())):
        return {"test": test}

    response = client.get("/test")
    assert response.status_code == 200
