from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from typing_extensions import Annotated

from .utils import needs_py310


class Dep:
    def __call__(self, request: Request):
        return "test"


@needs_py310
def test_stringified_annotations():
    app = FastAPI()

    client = TestClient(app)

    @app.get("/test/")
    def call(test: Annotated[str, Depends(Dep())]):
        return {"test": test}

    response = client.get("/test")
    assert response.status_code == 200
