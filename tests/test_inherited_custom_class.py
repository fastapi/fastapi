import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .utils import needs_pydanticv1, needs_pydanticv2


class MyUuid:
    def __init__(self, uuid_string: str):
        self.uuid = uuid_string

    def __str__(self):
        return self.uuid

    @property  # type: ignore
    def __class__(self):
        return uuid.UUID

    @property
    def __dict__(self):
        """Spoof a missing __dict__ by raising TypeError, this is how
        asyncpg.pgroto.pgproto.UUID behaves"""
        raise TypeError("vars() argument must have __dict__ attribute")


@needs_pydanticv2
def test_pydanticv2():
    from pydantic import field_serializer

    app = FastAPI()

    @app.get("/fast_uuid")
    def return_fast_uuid():
        asyncpg_uuid = MyUuid("a10ff360-3b1e-4984-a26f-d3ab460bdb51")
        assert isinstance(asyncpg_uuid, uuid.UUID)
        assert type(asyncpg_uuid) is not uuid.UUID
        with pytest.raises(TypeError):
            vars(asyncpg_uuid)
        return {"fast_uuid": asyncpg_uuid}

    class SomeCustomClass(BaseModel):
        model_config = {"arbitrary_types_allowed": True}

        a_uuid: MyUuid

        @field_serializer("a_uuid")
        def serialize_a_uuid(self, v):
            return str(v)

    @app.get("/get_custom_class")
    def return_some_user():
        # Test that the fix also works for custom pydantic classes
        return SomeCustomClass(a_uuid=MyUuid("b8799909-f914-42de-91bc-95c819218d01"))

    client = TestClient(app)

    with client:
        response_simple = client.get("/fast_uuid")
        response_pydantic = client.get("/get_custom_class")

    assert response_simple.json() == {
        "fast_uuid": "a10ff360-3b1e-4984-a26f-d3ab460bdb51"
    }

    assert response_pydantic.json() == {
        "a_uuid": "b8799909-f914-42de-91bc-95c819218d01"
    }


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_pydanticv1():
    app = FastAPI()

    @app.get("/fast_uuid")
    def return_fast_uuid():
        asyncpg_uuid = MyUuid("a10ff360-3b1e-4984-a26f-d3ab460bdb51")
        assert isinstance(asyncpg_uuid, uuid.UUID)
        assert type(asyncpg_uuid) is not uuid.UUID
        with pytest.raises(TypeError):
            vars(asyncpg_uuid)
        return {"fast_uuid": asyncpg_uuid}

    class SomeCustomClass(BaseModel):
        class Config:
            arbitrary_types_allowed = True
            json_encoders = {uuid.UUID: str}

        a_uuid: MyUuid

    @app.get("/get_custom_class")
    def return_some_user():
        # Test that the fix also works for custom pydantic classes
        return SomeCustomClass(a_uuid=MyUuid("b8799909-f914-42de-91bc-95c819218d01"))

    client = TestClient(app)

    with client:
        response_simple = client.get("/fast_uuid")
        response_pydantic = client.get("/get_custom_class")

    assert response_simple.json() == {
        "fast_uuid": "a10ff360-3b1e-4984-a26f-d3ab460bdb51"
    }

    assert response_pydantic.json() == {
        "a_uuid": "b8799909-f914-42de-91bc-95c819218d01"
    }
