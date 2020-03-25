from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class RecursiveItem(BaseModel):
    sub_items: List["RecursiveItem"] = []
    name: str


RecursiveItem.update_forward_refs()


class RecursiveSubitemInSubmodel(BaseModel):
    sub_items2: List["RecursiveItemViaSubmodel"] = []
    name: str


class RecursiveItemViaSubmodel(BaseModel):
    sub_items1: List[RecursiveSubitemInSubmodel] = []
    name: str


RecursiveSubitemInSubmodel.update_forward_refs()


@app.get("/items/recursive", response_model=RecursiveItem)
def get_recursive():
    return {"name": "item", "sub_items": [{"name": "subitem", "sub_items": []}]}


@app.get("/items/recursive-submodel", response_model=RecursiveItemViaSubmodel)
def get_recursive_submodel():
    return {
        "name": "item",
        "sub_items1": [
            {
                "name": "subitem",
                "sub_items2": [
                    {
                        "name": "subsubitem",
                        "sub_items1": [{"name": "subsubsubitem", "sub_items2": []}],
                    }
                ],
            }
        ],
    }


client = TestClient(app)


def test_recursive():
    response = client.get("/items/recursive")
    assert response.status_code == 200
    assert response.json() == {
        "sub_items": [{"name": "subitem", "sub_items": []}],
        "name": "item",
    }

    response = client.get("/items/recursive-submodel")
    assert response.status_code == 200
    assert response.json() == {
        "name": "item",
        "sub_items1": [
            {
                "name": "subitem",
                "sub_items2": [
                    {
                        "name": "subsubitem",
                        "sub_items1": [{"name": "subsubsubitem", "sub_items2": []}],
                    }
                ],
            }
        ],
    }
