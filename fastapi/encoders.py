from enum import Enum
from types import GeneratorType
from typing import Any, Set

from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE


def jsonable_encoder(
    obj: Any,
    include: Set[str] = None,
    exclude: Set[str] = set(),
    by_alias: bool = False,
    include_none: bool = True,
    custom_encoder: dict = {},
    sqlalchemy_safe: bool = True,
) -> Any:
    if isinstance(obj, BaseModel):
        encoder = getattr(obj.Config, "json_encoders", custom_encoder)
        return jsonable_encoder(
            obj.dict(include=include, exclude=exclude, by_alias=by_alias),
            include_none=include_none,
            custom_encoder=encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        encoded_dict = {}
        for key, value in obj.items():
            if (
                (
                    not sqlalchemy_safe
                    or (not isinstance(key, str))
                    or (not key.startswith("_sa"))
                )
                and (value is not None or include_none)
                and ((include and key in include) or key not in exclude)
            ):
                encoded_key = jsonable_encoder(
                    key,
                    by_alias=by_alias,
                    include_none=include_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    include_none=include_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    include_none=include_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list
    errors = []
    try:
        if custom_encoder and type(obj) in custom_encoder:
            encoder = custom_encoder[type(obj)]
        else:
            encoder = ENCODERS_BY_TYPE[type(obj)]
        return encoder(obj)
    except KeyError as e:
        errors.append(e)
        try:
            data = dict(obj)
        except Exception as e:
            errors.append(e)
            try:
                data = vars(obj)
            except Exception as e:
                errors.append(e)
                raise ValueError(errors)
    return jsonable_encoder(
        data,
        by_alias=by_alias,
        include_none=include_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )
