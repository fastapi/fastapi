import sys
from collections.abc import Sequence
from typing import Any, Literal, Union

from fastapi.types import ModelNameMap

if sys.version_info >= (3, 14):

    class AnyUrl:
        pass

    class BaseConfig:
        pass

    class BaseModel:
        pass

    class Color:
        pass

    class CoreSchema:
        pass

    class ErrorWrapper:
        pass

    class FieldInfo:
        pass

    class GetJsonSchemaHandler:
        pass

    class JsonSchemaValue:
        pass

    class ModelField:
        pass

    class NameEmail:
        pass

    class RequiredParam:
        pass

    class SecretBytes:
        pass

    class SecretStr:
        pass

    class Undefined:
        pass

    class UndefinedType:
        pass

    class Url:
        pass

    from .v2 import ValidationError, create_model

    def get_definitions(
        *,
        fields: list[ModelField],
        model_name_map: ModelNameMap,
        separate_input_output_schemas: bool = True,
    ) -> tuple[
        dict[
            tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
        ],
        dict[str, dict[str, Any]],
    ]:
        return {}, {}  # pragma: no cover


else:
    from .v1 import AnyUrl as AnyUrl
    from .v1 import BaseConfig as BaseConfig
    from .v1 import BaseModel as BaseModel
    from .v1 import Color as Color
    from .v1 import CoreSchema as CoreSchema
    from .v1 import ErrorWrapper as ErrorWrapper
    from .v1 import FieldInfo as FieldInfo
    from .v1 import GetJsonSchemaHandler as GetJsonSchemaHandler
    from .v1 import JsonSchemaValue as JsonSchemaValue
    from .v1 import ModelField as ModelField
    from .v1 import NameEmail as NameEmail
    from .v1 import RequiredParam as RequiredParam
    from .v1 import SecretBytes as SecretBytes
    from .v1 import SecretStr as SecretStr
    from .v1 import Undefined as Undefined
    from .v1 import UndefinedType as UndefinedType
    from .v1 import Url as Url
    from .v1 import ValidationError, create_model
    from .v1 import get_definitions as get_definitions


RequestErrorModel: type[BaseModel] = create_model("Request")


def _normalize_errors(errors: Sequence[Any]) -> list[dict[str, Any]]:
    use_errors: list[Any] = []
    for error in errors:
        if isinstance(error, ErrorWrapper):
            new_errors = ValidationError(
                errors=[error], model=RequestErrorModel
            ).errors()
            use_errors.extend(new_errors)
        elif isinstance(error, list):
            use_errors.extend(_normalize_errors(error))
        else:
            use_errors.append(error)
    return use_errors


def _regenerate_error_with_loc(
    *, errors: Sequence[Any], loc_prefix: tuple[Union[str, int], ...]
) -> list[dict[str, Any]]:
    updated_loc_errors: list[Any] = [
        {**err, "loc": loc_prefix + err.get("loc", ())}
        for err in _normalize_errors(errors)
    ]

    return updated_loc_errors
