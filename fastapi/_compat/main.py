import sys
from collections.abc import Sequence
from functools import lru_cache
from typing import (
    Any,
)

from fastapi._compat import may_v1
from fastapi._compat.shared import lenient_issubclass
from fastapi.types import ModelNameMap
from pydantic import BaseModel
from typing_extensions import Literal

from . import v2
from .model_field import ModelField
from .v2 import BaseConfig as BaseConfig
from .v2 import FieldInfo as FieldInfo
from .v2 import PydanticSchemaGenerationError as PydanticSchemaGenerationError
from .v2 import RequiredParam as RequiredParam
from .v2 import Undefined as Undefined
from .v2 import UndefinedType as UndefinedType
from .v2 import Url as Url
from .v2 import Validator as Validator
from .v2 import evaluate_forwardref as evaluate_forwardref
from .v2 import get_missing_field_error as get_missing_field_error
from .v2 import (
    with_info_plain_validator_function as with_info_plain_validator_function,
)


@lru_cache
def get_cached_model_fields(model: type[BaseModel]) -> list[ModelField]:
    if lenient_issubclass(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1.get_model_fields(model)  # type: ignore[arg-type,return-value]
    else:
        from . import v2

        return v2.get_model_fields(model)  # type: ignore[return-value]


def _is_undefined(value: object) -> bool:
    if isinstance(value, may_v1.UndefinedType):
        return True

    return isinstance(value, v2.UndefinedType)


def _get_model_config(model: BaseModel) -> Any:
    if isinstance(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1._get_model_config(model)

    return v2._get_model_config(model)


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    if isinstance(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1._model_dump(model, mode=mode, **kwargs)

    return v2._model_dump(model, mode=mode, **kwargs)


def _is_error_wrapper(exc: Exception) -> bool:
    if isinstance(exc, may_v1.ErrorWrapper):
        return True

    return isinstance(exc, v2.ErrorWrapper)


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if isinstance(field_info, may_v1.FieldInfo):
        from fastapi._compat import v1

        return v1.copy_field_info(field_info=field_info, annotation=annotation)

    return v2.copy_field_info(field_info=field_info, annotation=annotation)


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> type[BaseModel]:
    if fields and isinstance(fields[0], may_v1.ModelField):
        from fastapi._compat import v1

        return v1.create_body_model(fields=fields, model_name=model_name)

    return v2.create_body_model(fields=fields, model_name=model_name)  # type: ignore[arg-type]


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    if isinstance(field_info, may_v1.FieldInfo):
        from fastapi._compat import v1

        return v1.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )

    return v2.get_annotation_from_field_info(
        annotation=annotation, field_info=field_info, field_name=field_name
    )


def is_bytes_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_bytes_field(field)

    return v2.is_bytes_field(field)  # type: ignore[arg-type]


def is_bytes_sequence_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_bytes_sequence_field(field)

    return v2.is_bytes_sequence_field(field)  # type: ignore[arg-type]


def is_scalar_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_scalar_field(field)

    return v2.is_scalar_field(field)  # type: ignore[arg-type]


def is_scalar_sequence_field(field: ModelField) -> bool:
    return v2.is_scalar_sequence_field(field)  # type: ignore[arg-type]


def is_sequence_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_sequence_field(field)

    return v2.is_sequence_field(field)  # type: ignore[arg-type]


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.serialize_sequence_value(field=field, value=value)

    return v2.serialize_sequence_value(field=field, value=value)  # type: ignore[arg-type]


def get_compat_model_name_map(fields: list[ModelField]) -> ModelNameMap:
    v1_model_fields = [
        field for field in fields if isinstance(field, may_v1.ModelField)
    ]
    if v1_model_fields:
        from fastapi._compat import v1

        v1_flat_models = v1.get_flat_models_from_fields(
            v1_model_fields,  # type: ignore[arg-type]
            known_models=set(),
        )
        all_flat_models = v1_flat_models
    else:
        all_flat_models = set()

    v2_model_fields = [field for field in fields if isinstance(field, v2.ModelField)]
    v2_flat_models = v2.get_flat_models_from_fields(v2_model_fields, known_models=set())
    all_flat_models = all_flat_models.union(v2_flat_models)  # type: ignore[arg-type]

    model_name_map = v2.get_model_name_map(all_flat_models)  # type: ignore[arg-type]
    return model_name_map


def get_definitions(
    *,
    fields: list[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> tuple[
    dict[
        tuple[ModelField, Literal["validation", "serialization"]],
        may_v1.JsonSchemaValue,
    ],
    dict[str, dict[str, Any]],
]:
    if sys.version_info < (3, 14):
        v1_fields = [field for field in fields if isinstance(field, may_v1.ModelField)]
        v1_field_maps, v1_definitions = may_v1.get_definitions(
            fields=v1_fields,  # type: ignore[arg-type]
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )

        v2_fields = [field for field in fields if isinstance(field, v2.ModelField)]
        v2_field_maps, v2_definitions = v2.get_definitions(
            fields=v2_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
        all_definitions = {**v1_definitions, **v2_definitions}
        all_field_maps = {**v1_field_maps, **v2_field_maps}  # type: ignore[misc]
        return all_field_maps, all_definitions

    # Pydantic v1 is not supported since Python 3.14
    else:
        v2_fields = [field for field in fields if isinstance(field, v2.ModelField)]
        v2_field_maps, v2_definitions = v2.get_definitions(
            fields=v2_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
        return v2_field_maps, v2_definitions


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
    field_mapping: dict[
        tuple[ModelField, Literal["validation", "serialization"]],
        may_v1.JsonSchemaValue,
    ],
    separate_input_output_schemas: bool = True,
) -> dict[str, Any]:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,
            separate_input_output_schemas=separate_input_output_schemas,
        )

    return v2.get_schema_from_model_field(
        field=field,  # type: ignore[arg-type]
        model_name_map=model_name_map,
        field_mapping=field_mapping,  # type: ignore[arg-type]
        separate_input_output_schemas=separate_input_output_schemas,
    )


def _is_model_field(value: Any) -> bool:
    if isinstance(value, may_v1.ModelField):
        return True

    return isinstance(value, v2.ModelField)


def _is_model_class(value: Any) -> bool:
    if lenient_issubclass(value, may_v1.BaseModel):
        return True

    return lenient_issubclass(value, v2.BaseModel)  # type: ignore[attr-defined]
