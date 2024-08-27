import asyncio
from contextlib import asynccontextmanager
from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@asynccontextmanager
async def lifespan(_: FastAPI):  # pragma: no cover
    loop = asyncio.get_event_loop()
    loop.set_task_factory(asyncio.eager_task_factory)
    yield


app = FastAPI(title="test", lifespan=lifespan, debug=True)


@app.get("/tst")
async def endpoint() -> Dict[str, str]:  # pragma: no cover
    return {"message": "Hello World"}


@pytest.mark.skip(
    reason="Currently causes segfaults in the tests, needs further investigation",
)
def test_eager_task_factory():  # pragma: no cover
    with TestClient(app=app) as client:
        client.get("/tst")
