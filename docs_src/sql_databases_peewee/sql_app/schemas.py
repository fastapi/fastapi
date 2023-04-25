from typing import Any, List, Union

import peewee
from pydantic import BaseModel, model_serializer
from pydantic.validators import model_validator
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    model_config = dict(from_attributes=True, getter_dict=PeeweeGetterDict)
    # TODO: Fix: getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    model_config = {"from_attributes": True}
    # TODO: Fix: getter_dict = PeeweeGetterDict
