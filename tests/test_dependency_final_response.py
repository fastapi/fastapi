from typing import Union

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient


class Dep:
    response: Union[None, Response] = None


class SyncGenDep(Dep):

    def __call__(self, response: Response) -> "SyncGenDep":
        yield self
        self.response = response.final_response
        return


class AsyncGenDep(Dep):

    async def __call__(self, response: Response) -> "AsyncGenDep":
        yield self
        self.response = response.final_response
        return


@pytest.mark.parametrize(
    "dep", (SyncGenDep(), AsyncGenDep(),),
    ids=["sync-generator", "async-generator"]
)
def test_inject_response(dep: Dep):
    app = FastAPI()

    @app.get("/raw", dependencies=[Depends(dep)])
    def raw():
        return Response(status_code=400)

    @app.get("/json", dependencies=[Depends(dep)])
    def json():
        return "abcd"

    client = TestClient(app)
    client.get("/raw")
    assert dep.response.status_code == 400
    client.get("/json")
    assert dep.response.body == b'"abcd"'
