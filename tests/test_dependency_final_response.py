from typing import Union

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient


class SyncGenDep:
    response: Union[None, Response] = None

    def __call__(self, response: Response):
        yield 1234
        self.response = response.final_response
        return


class AsyncGenDep:
    response: Union[None, Response] = None

    async def __call__(self, response: Response):
        yield 1234
        self.response = response.final_response
        return


@pytest.mark.parametrize(
    "gen", (SyncGenDep(), AsyncGenDep()), ids=["sync-generator", "async-generator"]
)
def test_inject_response(gen: Union[SyncGenDep, AsyncGenDep]):
    app = FastAPI()

    @app.get("/raw")
    def raw(v: int = Depends(gen)):
        assert v == 1234
        return Response(status_code=400)

    @app.get("/json")
    def json(v: int = Depends(gen)):
        assert v == 1234
        return "abcd"

    client = TestClient(app)
    client.get("/raw")
    assert gen.response.status_code == 400
    client.get("/json")
    assert gen.response.body == b'"abcd"'
