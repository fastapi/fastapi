from typing import Callable, Union

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient
import pytest


class SyncGenDep:
    response: Union[None, Response] = None

    def __call__(self):
        self.response: Response = yield 1234
        return


class AsyncGenDep:
    response: Union[None, Response] = None
    
    async def __call__(self):
        self.response: Response = yield 1234
        return



@pytest.mark.parametrize(
    "gen", (SyncGenDep(), AsyncGenDep()),
    ids=["sync-generator", "async-generator"]
)
def test_inject_response(gen: Union[SyncGenDep, AsyncGenDep]):
    app = FastAPI()

    @app.get("/")
    def root(v: int = Depends(gen, inject_response=True)):
        assert v == 1234
        return Response(status_code=400)

    client = TestClient(app)
    client.get("/")
    assert gen.response is not None
    assert gen.response.status_code == 400


def sync_func():
    ...


async def async_func():
    ...


@pytest.mark.parametrize(
    "gen", (sync_func, async_func),
    ids=["sync-function", "async-function"]
)
def test_inject_response_not_a_generator(gen: Callable[[], None]):
    app = FastAPI()

    with pytest.raises(TypeError, match="can only be used with dependencies with `yield`"):
        @app.get("/")
        def root(v: int = Depends(gen, inject_response=True)):
            ...
