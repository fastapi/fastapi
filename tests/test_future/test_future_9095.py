from __future__ import annotations

import sys

from ..utils import needs_py310

if sys.version_info > (3, 10):
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient
    from starlette.requests import Request

    app = FastAPI()

    client = TestClient(app)

    class Test:
        def __call__(self, request: Request):
            return "test"

    @app.get("/test/")
    def call(test: str = Depends(Test())):
        return {"test": test}


@needs_py310
def test_call():
    response = client.get("/test")
    assert response.status_code == 200
