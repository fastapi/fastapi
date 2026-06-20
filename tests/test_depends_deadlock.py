import asyncio
import multiprocessing
import threading
import time
from collections.abc import Iterator

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel

# Mutex, and dependency acting as our "connection pool" for a database for example
mutex = threading.Lock()


# Simulate releasing a pooled resource in the teardown of a Depends,
# which in reality is usually a database connection or similar.
def release_resource() -> Iterator[None]:
    try:
        time.sleep(0.001)
        yield
    finally:
        time.sleep(0.001)
        mutex.release()


app = FastAPI()


class Item(BaseModel):
    name: str
    id: int


# An endpoint that uses Depends for resource management and also includes
# a response_model definition would previously deadlock in the validation
# of the model and the cleanup of the Depends
@app.get("/deadlock", response_model=Item)
def get_deadlock(dep: None = Depends(release_resource)) -> Item:
    mutex.acquire()
    return Item(name="foo", id=1)


# NOTE: the failure mode here can cause the test suite to hang.
# Since the default threadpool is a global which is not easily patched
# (and doing so would make the test somewhat fragile/pointless)
# we need to use a subprocess to isolate the bad behaviour.
# If you are struggling to debug, comment out this function and rename
# the impl_ version to test_depends_deadlock
def test_depends_deadlock() -> None:

    proc = multiprocessing.Process(target=impl_test_depends_deadlock, daemon=True)
    proc.start()
    proc.join(timeout=10)

    try:
        assert not proc.is_alive(), "Process is still alive after timeout, likely due to a deadlock"
    finally:
        proc.kill()  # Ensure the process is terminated if it's still alive

    assert proc.exitcode == 0, "Process did not exit cleanly, see logs for details"


# Fire off 100 requests in parallel(ish) in order to create contention
# over the shared resource (simulating a fastapi server that interacts with
# a database connection pool).
def impl_test_depends_deadlock() -> None:
    async def make_request(client: AsyncClient):
        await client.get("/deadlock")

    async def run_requests() -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as aclient:
            tasks = [make_request(aclient) for _ in range(100)]
            await asyncio.gather(*tasks)

    asyncio.run(run_requests())
