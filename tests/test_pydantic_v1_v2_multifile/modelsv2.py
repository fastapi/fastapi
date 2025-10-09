from typing import List, Union

from pydantic import BaseModel


class SubItem(BaseModel):
    new_sub_name: str


class Item(BaseModel):
    new_title: str
    new_size: int
    new_description: Union[str, None] = None
    new_sub: SubItem
    new_multi: List[SubItem] = []


class ItemInList(BaseModel):
    name2: str
