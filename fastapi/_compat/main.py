import sys
from functools import lru_cache
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Type,
)

from fastapi._compat import may_v1
from fastapi._compat.shared import PYDANTIC_V2, lenient_issubclass
from fastapi.types import ModelNameMap
from pydantic import BaseModel
from typing_extensions import Literal

from .model_field import ModelField

if PYDANTIC_V2:
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
else:
    from .v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
    from .v1 import FieldInfo as FieldInfo
    from .v1 import (  # type: ignore[assignment]
        PydanticSchemaGenerationError as PydanticSchemaGenerationError,
    )
    from .v1 import RequiredParam as RequiredParam
    from .v1 import Undefined as Undefined
    from .v1 import UndefinedType as UndefinedType
    from .v1 import Url as Url  # type: ignore[assignment]
    from .v1 import Validator as Validator
    from .v1 import evaluate_forwardref as evaluate_forwardref
    from .v1 import get_missing_field_error as get_missing_field_error
    from .v1 import (  # type: ignore[assignment]
        with_info_plain_validator_function as with_info_plain_validator_function,
    )


@lru_cache
def get_cached_model_fields(model: Type[BaseModel]) -> List[ModelField]:
    if lenient_issubclass(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1.get_model_fields(model)
    else:
        from . import v2

        return v2.get_model_fields(model)  # type: ignore[return-value]


def _is_undefined(value: object) -> bool:
    if isinstance(value, may_v1.UndefinedType):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(value, v2.UndefinedType)
    return False


def _get_model_config(model: BaseModel) -> Any:
    if isinstance(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1._get_model_config(model)
    elif PYDANTIC_V2:
        from . import v2

        return v2._get_model_config(model)


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    if isinstance(model, may_v1.BaseModel):
        from fastapi._compat import v1

        return v1._model_dump(model, mode=mode, **kwargs)
    elif PYDANTIC_V2:
        from . import v2

        return v2._model_dump(model, mode=mode, **kwargs)


def _is_error_wrapper(exc: Exception) -> bool:
    if isinstance(exc, may_v1.ErrorWrapper):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(exc, v2.ErrorWrapper)
    return False


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if isinstance(field_info, may_v1.FieldInfo):
        from fastapi._compat import v1

        return v1.copy_field_info(field_info=field_info, annotation=annotation)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.copy_field_info(field_info=field_info, annotation=annotation)


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> Type[BaseModel]:
    if fields and isinstance(fields[0], may_v1.ModelField):
        from fastapi._compat import v1

        return v1.create_body_model(fields=fields, model_name=model_name)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.create_body_model(fields=fields, model_name=model_name)  # type: ignore[arg-type]


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    if isinstance(field_info, may_v1.FieldInfo):
        from fastapi._compat import v1

        return v1.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )


def is_bytes_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_bytes_field(field)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.is_bytes_field(field)  # type: ignore[arg-type]


def is_bytes_sequence_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_bytes_sequence_field(field)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.is_bytes_sequence_field(field)  # type: ignore[arg-type]


def is_scalar_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_scalar_field(field)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.is_scalar_field(field)  # type: ignore[arg-type]


def is_scalar_sequence_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_scalar_sequence_field(field)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.is_scalar_sequence_field(field)  # type: ignore[arg-type]


def is_sequence_field(field: ModelField) -> bool:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.is_sequence_field(field)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.is_sequence_field(field)  # type: ignore[arg-type]


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.serialize_sequence_value(field=field, value=value)
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.serialize_sequence_value(field=field, value=value)  # type: ignore[arg-type]


def _model_rebuild(model: Type[BaseModel]) -> None:
    if lenient_issubclass(model, may_v1.BaseModel):
        from fastapi._compat import v1

        v1._model_rebuild(model)
    elif PYDANTIC_V2:
        from . import v2

        v2._model_rebuild(model)


def get_compat_model_name_map(fields: List[ModelField]) -> ModelNameMap:
    v1_model_fields = [
        field for field in fields if isinstance(field, may_v1.ModelField)
    ]
    if v1_model_fields:
        from fastapi._compat import v1

        v1_flat_models = v1.get_flat_models_from_fields(
            v1_model_fields, known_models=set()
        )
        all_flat_models = v1_flat_models
    else:
        all_flat_models = set()
    if PYDANTIC_V2:
        from . import v2

        v2_model_fields = [
            field for field in fields if isinstance(field, v2.ModelField)
        ]
        v2_flat_models = v2.get_flat_models_from_fields(
            v2_model_fields, known_models=set()
        )
        all_flat_models = all_flat_models.union(v2_flat_models)

        model_name_map = v2.get_model_name_map(all_flat_models)
        return model_name_map
    from fastapi._compat import v1

    model_name_map = v1.get_model_name_map(all_flat_models)
    return model_name_map


def get_definitions(
    *,
    fields: List[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[
        Tuple[ModelField, Literal["validation", "serialization"]],
        may_v1.JsonSchemaValue,
    ],
    Dict[str, Dict[str, Any]],
]:
    if sys.version_info < (3, 14):
        v1_fields = [field for field in fields if isinstance(field, may_v1.ModelField)]
        v1_field_maps, v1_definitions = may_v1.get_definitions(
            fields=v1_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
        if not PYDANTIC_V2:
            return v1_field_maps, v1_definitions
        else:
            from . import v2

            v2_fields = [field for field in fields if isinstance(field, v2.ModelField)]
            v2_field_maps, v2_definitions = v2.get_definitions(
                fields=v2_fields,
                model_name_map=model_name_map,
                separate_input_output_schemas=separate_input_output_schemas,
            )
            all_definitions = {**v1_definitions, **v2_definitions}
            all_field_maps = {**v1_field_maps, **v2_field_maps}
            return all_field_maps, all_definitions

    # Pydantic v1 is not supported since Python 3.14
    else:
        from . import v2

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
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]],
        may_v1.JsonSchemaValue,
    ],
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    if isinstance(field, may_v1.ModelField):
        from fastapi._compat import v1

        return v1.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,
            separate_input_output_schemas=separate_input_output_schemas,
        )
    else:
        assert PYDANTIC_V2
        from . import v2

        return v2.get_schema_from_model_field(
            field=field,  # type: ignore[arg-type]
            model_name_map=model_name_map,
            field_mapping=field_mapping,  # type: ignore[arg-type]
            separate_input_output_schemas=separate_input_output_schemas,
        )


def _is_model_field(value: Any) -> bool:
    if isinstance(value, may_v1.ModelField):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(value, v2.ModelField)
    return False


def _is_model_class(value: Any) -> bool:
    if lenient_issubclass(value, may_v1.BaseModel):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return lenient_issubclass(value, v2.BaseModel)  # type: ignore[attr-defined]
    return False
