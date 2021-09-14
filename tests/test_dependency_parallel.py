from asyncio import sleep
from time import time

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

client = TestClient(app)


async def dependency1():
    ts = time()
    await sleep(0.1)
    return ts


async def dependency2():
    ts = time()
    await sleep(0.1)
    return ts


@app.get("/parallel-dependencies")
async def parallel_dependencies(
    ts1=Depends(dependency1), ts2=Depends(dependency2),
):
    return abs(ts1 - ts2)


def test_dependencies_run_in_parallel():
    response = client.get('/parallel-dependencies')
    assert 200 == response.status_code, response.text
    assert response.json() < 0.1
