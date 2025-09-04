from typing import List

from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from pydantic import BaseModel

app = FastAPI()


class RecursiveItem(BaseModel):
    sub_items: List["RecursiveItem"] = []
    name: str


class RecursiveSubitemInSubmodel(BaseModel):
    sub_items2: List["RecursiveItemViaSubmodel"] = []
    name: str


class RecursiveItemViaSubmodel(BaseModel):
    sub_items1: List[RecursiveSubitemInSubmodel] = []
    name: str


if PYDANTIC_V2:
    RecursiveItem.model_rebuild()
    RecursiveSubitemInSubmodel.model_rebuild()
    RecursiveItemViaSubmodel.model_rebuild()
else:
    RecursiveItem.update_forward_refs()
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
