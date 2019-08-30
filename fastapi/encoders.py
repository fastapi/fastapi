from enum import Enum
from functools import partial
from types import GeneratorType
from typing import Any, Dict, List, Set, Type, Union

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.json import ENCODERS_BY_TYPE
from pydantic.utils import lenient_issubclass


class SecureFieldValue:
    def __init__(self, model: BaseModel, secure_model_type: Type[BaseModel]):
        self.model = model
        self.secure_model_type = secure_model_type

    def dict(
        self,
        include: Set[str] = None,
        exclude: Set[str] = None,
        by_alias: bool = False,
        skip_defaults: bool = False,
    ) -> Dict[str, Any]:
        return secure_dict(
            self.model,
            self.secure_model_type,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
        )


def get_secure_field_value(v: Any, field: Field) -> Any:
    if isinstance(v, BaseModel) and lenient_issubclass(field.type_, BaseModel):
        return SecureFieldValue(v, field.type_)
    return v


def secure_dict(
    model: BaseModel,
    model_type: Type[BaseModel],
    *,
    include: Set[str] = None,
    exclude: Set[str] = None,
    by_alias: bool = False,
    skip_defaults: bool = False
) -> Dict[str, Any]:
    """
    Based on pydantic.BaseModel.dict
    """
    get_key = model._get_key_factory(by_alias)
    get_key = partial(get_key, model.fields)

    return_keys = model._calculate_keys(
        include=include, exclude=exclude, skip_defaults=skip_defaults
    )
    if return_keys is None:
        return_keys = set(model.__dict__.keys())
    return_keys = return_keys.intersection(model_type.__fields__.keys())
    response = {}
    for k, v in model.__dict__.items():
        if k not in return_keys:
            continue
        response[get_key(k)] = get_secure_field_value(v, model_type.__fields__[k])
    return response

SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]


def jsonable_encoder(
    obj: Any,
    include: Union[SetIntStr, DictIntStrAny] = None,
    exclude: Union[SetIntStr, DictIntStrAny] = set(),
    by_alias: bool = True,
    skip_defaults: bool = False,
    include_none: bool = True,
    custom_encoder: dict = {},
    sqlalchemy_safe: bool = True,
) -> Any:
    if include is not None and not isinstance(include, set):
        include = set(include)
    if exclude is not None and not isinstance(exclude, set):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        obj = SecureFieldValue(obj, type(obj))
    if isinstance(obj, SecureFieldValue):
        encoder = getattr(obj.model.Config, "json_encoders", custom_encoder)
        return jsonable_encoder(
            obj.dict(
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                skip_defaults=skip_defaults,
            ),
            skip_defaults=skip_defaults,
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
        if exclude is None:
            exclude = set()
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
                    skip_defaults=skip_defaults,
                    include_none=include_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    skip_defaults=skip_defaults,
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
                    skip_defaults=skip_defaults,
                    include_none=include_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list
    errors: List[Exception] = []
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
        skip_defaults=skip_defaults,
        include_none=include_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )
