from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: Union[int, None]
