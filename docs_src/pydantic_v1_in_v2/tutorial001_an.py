from typing import Union

from pydantic.v1 import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float
