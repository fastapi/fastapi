import sys
from typing import Any, Dict, List, Literal, Sequence, Tuple, Union

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

    def get_definitions(
        *,
        fields: List[ModelField],
        model_name_map: ModelNameMap,
        separate_input_output_schemas: bool = True,
    ) -> Tuple[
        Dict[
            Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
        ],
        Dict[str, Dict[str, Any]],
    ]:
        return {}, {}

    def _normalize_errors(errors: Sequence[Any]) -> List[Dict[str, Any]]:
        return []

    def _regenerate_error_with_loc(
        *, errors: Sequence[Any], loc_prefix: Tuple[Union[str, int], ...]
    ) -> List[Dict[str, Any]]:
        return []


else:
    from .v1 import AnyUrl as AnyUrl  # type: ignore[assignment]
    from .v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
    from .v1 import BaseModel as BaseModel  # type: ignore[assignment]
    from .v1 import Color as Color  # type: ignore[assignment]
    from .v1 import CoreSchema as CoreSchema  # type: ignore[assignment]
    from .v1 import ErrorWrapper as ErrorWrapper  # type: ignore[assignment]
    from .v1 import FieldInfo as FieldInfo  # type: ignore[assignment]
    from .v1 import (
        GetJsonSchemaHandler as GetJsonSchemaHandler,  # type: ignore[assignment]
    )
    from .v1 import JsonSchemaValue as JsonSchemaValue  # type: ignore[assignment]
    from .v1 import (
        ModelField,  # type: ignore[assignment]
    )
    from .v1 import NameEmail as NameEmail  # type: ignore[assignment]
    from .v1 import RequiredParam as RequiredParam  # type: ignore[assignment]
    from .v1 import SecretBytes as SecretBytes  # type: ignore[assignment]
    from .v1 import SecretStr as SecretStr  # type: ignore[assignment]
    from .v1 import Undefined as Undefined  # type: ignore[assignment]
    from .v1 import UndefinedType as UndefinedType  # type: ignore[assignment]
    from .v1 import Url as Url  # type: ignore[assignment]
    from .v1 import _normalize_errors as _normalize_errors  # type: ignore[assignment]
