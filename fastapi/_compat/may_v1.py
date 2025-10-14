import sys
from typing import Any, Dict, List, Literal, Sequence, Tuple, Union

from fastapi.types import ModelNameMap

if sys.version_info >= (3, 14):

    class BaseConfig:
        pass

    class FieldInfo:
        pass

    class BaseModel:
        pass

    class UndefinedType:
        pass

    class ErrorWrapper:
        pass

    class ModelField:
        pass

    class JsonSchemaValue:
        pass

    class Color:
        pass

    class NameEmail:
        pass

    class SecretBytes:
        pass

    class SecretStr:
        pass

    class AnyUrl:
        pass

    class Url:
        pass

    class CoreSchema:
        pass

    class GetJsonSchemaHandler:
        pass

    class JsonSchemaValue:
        pass

    class Undefined:
        pass

    class RequiredParam:
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

    def _regenerate_error_with_loc(
        *, errors: Sequence[Any], loc_prefix: Tuple[Union[str, int], ...]
    ) -> List[Dict[str, Any]]:
        return []

    def _normalize_errors(errors: Sequence[Any]) -> List[Dict[str, Any]]:
        return []

else:
    from .v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
    from .v1 import CoreSchema as CoreSchema
    from .v1 import FieldInfo as FieldInfo
    from .v1 import GetJsonSchemaHandler as GetJsonSchemaHandler
    from .v1 import (
        JsonSchemaValue,
        ModelField,
    )
    from .v1 import JsonSchemaValue as JsonSchemaValue
    from .v1 import UndefinedType as UndefinedType
    from .v1 import _normalize_errors as _normalize_errors
