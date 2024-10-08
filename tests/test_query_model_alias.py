from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Literal


class FilterParams(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


app = FastAPI()


@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query


client = TestClient(app)


def test_get_data_with_alias_default():
    response = client.get(
        "/items/?offset=1&orderBy=created_at",
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "limit": 100,
        "offset": 1,
        "orderBy": "created_at",
        "tags": [],
    }


def test_get_data_with_alias_non_default():
    response = client.get(
        "/items/?offset=1&orderBy=updated_at",
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "limit": 100,
        "offset": 1,
        "orderBy": "updated_at",
        "tags": [],
    }
