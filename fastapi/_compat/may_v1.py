import sys
from typing import Any, Dict, List, Literal, Sequence, Tuple, Union
from fastapi.types import ModelNameMap


if sys.version_info >= (3, 14):
    class BaseConfig():
        pass

    class FieldInfo():
        pass

    class BaseModel():
        pass

    class UndefinedType():
        pass

    class ErrorWrapper():
        pass

    class ModelField():
        pass

    class JsonSchemaValue():
        pass

    class Color():
        pass

    class NameEmail():
        pass

    class SecretBytes():
        pass

    class SecretStr():
        pass

    class AnyUrl():
        pass

    class Url():
        pass

    class CoreSchema():
        pass

    class GetJsonSchemaHandler():
        pass

    class JsonSchemaValue():
        pass

    class Undefined():
        pass

    class RequiredParam():
        pass

    def get_definitions(
            *,
            fields: List[ModelField],
            model_name_map: ModelNameMap,
            separate_input_output_schemas: bool = True,
    ) -> Tuple[
        Dict[Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
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
    from fastapi._compat import v1
    from .v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
    from .v1 import FieldInfo as FieldInfo
    from .v1 import BaseModel
    from .v1 import UndefinedType as UndefinedType
    from .v1 import ErrorWrapper
    from .v1 import ModelField
    from .v1 import JsonSchemaValue
    from .v1 import Color
    from .v1 import NameEmail
    from .v1 import SecretBytes
    from .v1 import SecretStr
    from .v1 import AnyUrl
    from .v1 import Url
    from .v1 import get_definitions
    from .v1 import _regenerate_error_with_loc
    from .v1 import CoreSchema as CoreSchema
    from .v1 import GetJsonSchemaHandler as GetJsonSchemaHandler
    from .v1 import JsonSchemaValue as JsonSchemaValue
    from .v1 import _normalize_errors as _normalize_errors
    from .v1 import Undefined
    from .v1 import RequiredParam
