import asyncio
import threading
import time
from typing import Generator

import httpx
from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


# Dummy pydantic model
class Item(BaseModel):
    name: str
    id: int


# Mutex, acting as our "connection pool" for a database for example
mutex_db_connection_pool = threading.Lock()


# Simulate a database class that uses a connection pool to manage
# active clients for a db. The client needs to perform blocking
# calls to connect and disconnect from the db
class MyDB:
    def __init__(self):
        self.lock_acquired = False

    def connect(self):
        mutex_db_connection_pool.acquire()
        self.lock_acquired = True
        # Sleep to simulate some blocking IO like connecting to a db
        time.sleep(0.001)

    def disconnect(self):
        if self.lock_acquired:
            # Use a sleep to simulate some blocking IO such as a db disconnect
            time.sleep(0.001)
            mutex_db_connection_pool.release()
            self.lock_acquired = False


# Simulate getting a connection to a database from a connection pool
# using the mutex to act as this limited resource
def get_db() -> Generator[MyDB, None, None]:
    my_db = MyDB()
    try:
        yield my_db
    finally:
        my_db.disconnect()


# An endpoint that uses Depends for resource management and also includes
# a response_model definition would previously deadlock in the validation
# of the model and the cleanup of the Depends
@app.get("/deadlock", response_model=Item)
def get_deadlock(db: MyDB = Depends(get_db)):
    db.connect()
    return Item(name="foo", id=1)


# Fire off 100 requests in parallel(ish) in order to create contention
# over the shared resource (simulating a fastapi server that interacts with
# a database connection pool). After the patch, each thread on the server is
# able to free the resource without deadlocking, allowing each request to
# be handled timely
def test_depends_deadlock_patch():
    async def make_request(client: httpx.AsyncClient):
        await client.get("/deadlock")

    async def run_requests():
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as aclient:
            tasks = [make_request(aclient) for _ in range(100)]
            await asyncio.gather(*tasks)

    asyncio.run(run_requests())
