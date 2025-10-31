from typing import List, Union

from pydantic import BaseModel


class SubItem(BaseModel):
    dup_sub_name: str


class Item(BaseModel):
    dup_title: str
    dup_size: int
    dup_description: Union[str, None] = None
    dup_sub: SubItem
    dup_multi: List[SubItem] = []


class ItemInList(BaseModel):
    dup_name2: str
