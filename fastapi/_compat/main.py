from functools import lru_cache
from typing import (
    Any,
)

from fastapi.types import ModelNameMap
from pydantic import BaseModel
from typing_extensions import Literal

from . import v2
from .v2 import BaseConfig as BaseConfig
from .v2 import FieldInfo as FieldInfo
from .v2 import ModelField
from .v2 import PydanticSchemaGenerationError as PydanticSchemaGenerationError
from .v2 import RequiredParam as RequiredParam
from .v2 import Undefined as Undefined
from .v2 import UndefinedType as UndefinedType
from .v2 import Url as Url
from .v2 import Validator as Validator
from .v2 import evaluate_forwardref as evaluate_forwardref
from .v2 import get_missing_field_error as get_missing_field_error
from .v2 import get_model_fields as get_model_fields
from .v2 import (
    with_info_plain_validator_function as with_info_plain_validator_function,
)


@lru_cache
def get_cached_model_fields(model: type[BaseModel]) -> list[ModelField]:
    return get_model_fields(model)  # type: ignore[return-value]


def get_compat_model_name_map(fields: list[ModelField]) -> ModelNameMap:
    all_flat_models = set()

    v2_model_fields = [field for field in fields if isinstance(field, v2.ModelField)]
    v2_flat_models = v2.get_flat_models_from_fields(v2_model_fields, known_models=set())
    all_flat_models = all_flat_models.union(v2_flat_models)  # type: ignore[arg-type]

    model_name_map = v2.get_model_name_map(all_flat_models)  # type: ignore[arg-type]
    return model_name_map


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
    field_mapping: dict[
        tuple[ModelField, Literal["validation", "serialization"]],
        dict[str, Any],
    ],
    separate_input_output_schemas: bool = True,
) -> dict[str, Any]:
    return v2.get_schema_from_model_field(
        field=field,  # type: ignore[arg-type]
        model_name_map=model_name_map,
        field_mapping=field_mapping,  # type: ignore[arg-type]
        separate_input_output_schemas=separate_input_output_schemas,
    )
