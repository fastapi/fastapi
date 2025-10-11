from typing import List, Union

from fastapi._compat.v1 import BaseModel


class SubItem(BaseModel):
    name: str


class Item(BaseModel):
    title: str
    size: int
    description: Union[str, None] = None
    sub: SubItem
    multi: List[SubItem] = []


class ItemInList(BaseModel):
    name1: str
