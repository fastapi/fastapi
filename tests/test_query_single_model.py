from typing import List, Optional

from dirty_equals import IsDict
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing_extensions import Annotated

app = FastAPI()


class QueryModel(BaseModel):
    item: List[int] = []
    with_alias: Optional[str] = Field(alias="withAlias", default=None)
    without_alias: str = "default"


@app.get("/query")
def get_query(query: Annotated[QueryModel, Query()]):
    return query


client = TestClient(app)


def test_query():
    response = client.get(
        "/query",
        params={
            "item": [1, 2],
            "withAlias": "abc123",
            "without_alias": "custom",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "item": [1, 2],
        "withAlias": "abc123",
        "without_alias": "custom",
    }


def test_defaults():
    response = client.get("/query", params={"item": [1, 2]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "item": [1, 2],
        "withAlias": None,
        "without_alias": "default",
    }


def test_invalid_data():
    response = client.get(
        "/query",
        params={
            "item": ["invalid"],
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "item", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "invalid",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["query", "item", 0],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "type_error.int_parsing",
                }
            ]
        }
    )
