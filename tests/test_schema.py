from pprint import pprint
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.testclient import TestClient

app = FastAPI()


class Items(BaseModel):
    items: Dict[str, int]


@app.post("/foo")
def foo(items: Items):
    return items.items


def test_dict():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_schema = response.json()

        data = Items(items={"str0": 0})
        assert data.schema() == openapi_schema.get("components").get("schemas").get(
            "Items"
        )
        pprint(data.schema())
