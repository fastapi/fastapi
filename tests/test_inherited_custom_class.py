import uuid

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

app = FastAPI()


class MyUuid:
    def __init__(self, uuid_string: str):
        self.uuid = uuid_string

    def __str__(self):
        return self.uuid

    @property
    def __class__(self):
        return uuid.UUID

    @property
    def __dict__(self):
        """Spoof a missing __dict__ by raising TypeError, this is how
        asyncpg.pgroto.pgproto.UUID behaves"""
        raise TypeError("vars() argument must have __dict__ attribute")


@app.get("/fast_uuid")
def return_fast_uuid():
    # I don't want to import asyncpg for this test so I made my own UUID
    # Import asyncpg and uncomment the two lines below for the actual bug..

    # from asyncpg.pgproto import pgproto
    # asyncpg_uuid = pgproto.UUID("a10ff360-3b1e-4984-a26f-d3ab460bdb51")

    asyncpg_uuid = MyUuid("a10ff360-3b1e-4984-a26f-d3ab460bdb51")
    assert isinstance(asyncpg_uuid, uuid.UUID)
    assert type(asyncpg_uuid) != uuid.UUID
    with pytest.raises(TypeError):
        vars(asyncpg_uuid)
    return {"fast_uuid": asyncpg_uuid}


client = TestClient(app)


def test_dt():
    with client:
        response = client.get("/fast_uuid")
    assert response.json() == {"fast_uuid": "a10ff360-3b1e-4984-a26f-d3ab460bdb51"}
