from enum import Enum
from types import GeneratorType
from typing import Any, Set

from pydantic import BaseModel
from pydantic.json import pydantic_encoder


def jsonable_encoder(
    obj: Any,
    include: Set[str] = None,
    exclude: Set[str] = set(),
    by_alias: bool = False,
    include_none: bool = True,
    root_encoder: bool = True,
) -> Any:
    errors = []
    try:
        return known_data_encoder(
            obj,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            include_none=include_none,
        )
    except Exception as e:
        if not root_encoder:
            raise e
        errors.append(e)
    try:
        data = dict(obj)
        return jsonable_encoder(
            data,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            include_none=include_none,
            root_encoder=False,
        )
    except Exception as e:
        if not root_encoder:
            raise e
        errors.append(e)
    try:
        data = vars(obj)
        return jsonable_encoder(
            data,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            include_none=include_none,
            root_encoder=False,
        )
    except Exception as e:
        if not root_encoder:
            raise e
        errors.append(e)
        raise ValueError(errors)


def known_data_encoder(
    obj: Any,
    include: Set[str] = None,
    exclude: Set[str] = set(),
    by_alias: bool = False,
    include_none: bool = True,
) -> Any:
    if isinstance(obj, BaseModel):
        return jsonable_encoder(
            obj.dict(include=include, exclude=exclude, by_alias=by_alias),
            include_none=include_none,
            root_encoder=False,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        return {
            jsonable_encoder(
                key, by_alias=by_alias, include_none=include_none, root_encoder=False
            ): jsonable_encoder(
                value, by_alias=by_alias, include_none=include_none, root_encoder=False
            )
            for key, value in obj.items()
            if value is not None or include_none
        }
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
        return [
            jsonable_encoder(
                item,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                include_none=include_none,
                root_encoder=False,
            )
            for item in obj
        ]
    return pydantic_encoder(obj)
