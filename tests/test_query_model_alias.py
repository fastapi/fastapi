from typing import List

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from fastapi.utils import PYDANTIC_V2
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


def to_camel(string: str) -> str:
    output = "".join(word.capitalize() for word in string.split("_"))
    return output[0].lower() + output[1:]


class FilterParams(BaseModel):
    if PYDANTIC_V2:
        model_config = ConfigDict(alias_generator=to_camel)
    else:

        class Config:
            alias_generator = to_camel

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: List[str] = []


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
