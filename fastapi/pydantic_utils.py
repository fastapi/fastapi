from types import GeneratorType
from typing import Set
from pydantic import BaseModel
from enum import Enum
from pydantic.json import pydantic_encoder


def jsonable_encoder(
    obj, include: Set[str] = None, exclude: Set[str] = set(), by_alias: bool = False, include_none=True,
):
    if isinstance(obj, BaseModel):
        return jsonable_encoder(
            obj.dict(include=include, exclude=exclude, by_alias=by_alias), include_none=include_none
        )
    elif isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        return {
            jsonable_encoder(
                key, by_alias=by_alias, include_none=include_none,
            ): jsonable_encoder(
                value, by_alias=by_alias, include_none=include_none,
            )
            for key, value in obj.items() if value is not None or include_none
        }
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
        return [
            jsonable_encoder(item, include=include, exclude=exclude, by_alias=by_alias, include_none=include_none)
            for item in obj
        ]
    return pydantic_encoder(obj)
