from functools import lru_cache
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Type,
)

from fastapi._compat import v1
from fastapi._compat.shared import lenient_issubclass
from fastapi.types import ModelNameMap
from fastapi.x_compat import PYDANTIC_V2
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
    from .v1 import BaseConfig as BaseConfig
    from .v1 import FieldInfo as FieldInfo
    from .v1 import PydanticSchemaGenerationError as PydanticSchemaGenerationError
    from .v1 import RequiredParam as RequiredParam
    from .v1 import Undefined as Undefined
    from .v1 import UndefinedType as UndefinedType
    from .v1 import Url as Url
    from .v1 import Validator as Validator
    from .v1 import evaluate_forwardref as evaluate_forwardref
    from .v1 import get_missing_field_error as get_missing_field_error
    from .v1 import (
        with_info_plain_validator_function as with_info_plain_validator_function,
    )


@lru_cache
def get_cached_model_fields(model: Type[BaseModel]) -> List[ModelField]:
    if lenient_issubclass(model, v1.BaseModel):
        return v1.get_model_fields(model)  # type: ignore[return-value]
    else:
        from . import v2

        return v2.get_model_fields(model)  # type: ignore[return-value]


def _is_undefined(value: object) -> bool:
    if isinstance(value, v1.UndefinedType):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(value, v2.UndefinedType)
    return False


def _get_model_config(model: BaseModel) -> Any:
    if isinstance(model, v1.BaseModel):
        return v1._get_model_config(model)
    elif PYDANTIC_V2:
        from . import v2

        return v2._get_model_config(model)


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    if isinstance(model, v1.BaseModel):
        return v1._model_dump(model, mode=mode, **kwargs)
    elif PYDANTIC_V2:
        from . import v2

        return v2._model_dump(model, mode=mode, **kwargs)


def _is_error_wrapper(exc: Exception) -> bool:
    if isinstance(exc, v1.ErrorWrapper):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(exc, v2.ErrorWrapper)
    return False


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if isinstance(field_info, v1.FieldInfo):
        return v1.copy_field_info(field_info=field_info, annotation=annotation)
    elif PYDANTIC_V2:
        from . import v2

        return v2.copy_field_info(field_info=field_info, annotation=annotation)
    raise TypeError("field_info must be an instance of FieldInfo")


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> Type[BaseModel]:
    if fields and isinstance(fields[0], v1.ModelField):
        return v1.create_body_model(fields=fields, model_name=model_name)  # type: ignore[return-value]
    elif PYDANTIC_V2:
        from . import v2

        return v2.create_body_model(fields=fields, model_name=model_name)  # type: ignore[return-value]
    raise TypeError("fields must be a sequence of ModelField instances")


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    if isinstance(field_info, v1.FieldInfo):
        return v1.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )
    elif PYDANTIC_V2:
        from . import v2

        return v2.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )
    raise TypeError("field_info must be an instance of FieldInfo")


def is_bytes_field(field: ModelField) -> bool:
    if isinstance(field, v1.ModelField):
        return v1.is_bytes_field(field)
    elif PYDANTIC_V2:
        from . import v2

        return v2.is_bytes_field(field)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def is_bytes_sequence_field(field: ModelField) -> bool:
    if isinstance(field, v1.ModelField):
        return v1.is_bytes_sequence_field(field)
    elif PYDANTIC_V2:
        from . import v2

        return v2.is_bytes_sequence_field(field)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def is_scalar_field(field: ModelField) -> bool:
    if isinstance(field, v1.ModelField):
        return v1.is_scalar_field(field)
    elif PYDANTIC_V2:
        from . import v2

        return v2.is_scalar_field(field)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def is_scalar_sequence_field(field: ModelField) -> bool:
    if isinstance(field, v1.ModelField):
        return v1.is_scalar_sequence_field(field)
    elif PYDANTIC_V2:
        from . import v2

        return v2.is_scalar_sequence_field(field)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def is_sequence_field(field: ModelField) -> bool:
    if isinstance(field, v1.ModelField):
        return v1.is_sequence_field(field)
    elif PYDANTIC_V2:
        from . import v2

        return v2.is_sequence_field(field)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    if isinstance(field, v1.ModelField):
        return v1.serialize_sequence_value(field=field, value=value)
    elif PYDANTIC_V2:
        from . import v2

        return v2.serialize_sequence_value(field=field, value=value)  # type: ignore[return-value]
    raise TypeError("field_info must be an instance of FieldInfo")


def _model_rebuild(model: Type[BaseModel]) -> None:
    if lenient_issubclass(model, v1.BaseModel):
        v1._model_rebuild(model)
    elif PYDANTIC_V2:
        from . import v2

        v2._model_rebuild(model)


def get_compat_model_name_map(fields: List[ModelField]) -> ModelNameMap:
    v1_models = [field for field in fields if isinstance(field, v1.ModelField)]
    if v1_models:
        models = v1.get_flat_models_from_fields(v1_models, known_models=set())
        return v1.get_model_name_map(models)  # type: ignore[no-any-return]
    return {}


def get_definitions(
    *,
    fields: List[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], v1.JsonSchemaValue],
    Dict[str, Dict[str, Any]],
]:
    v1_fields = [field for field in fields if isinstance(field, v1.ModelField)]
    v1_field_maps, v1_definitions = v1.get_definitions(
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
        # TODO: check for uniqueness
        all_definitions = {**v1_definitions, **v2_definitions}
        all_field_maps = {**v1_field_maps, **v2_field_maps}
        return all_field_maps, all_definitions


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], v1.JsonSchemaValue
    ],
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    if isinstance(field, v1.ModelField):
        return v1.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,  # type: ignore[arg-type]
            separate_input_output_schemas=separate_input_output_schemas,
        )
    elif PYDANTIC_V2:
        from . import v2

        return v2.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,  # type: ignore[arg-type]
            separate_input_output_schemas=separate_input_output_schemas,
        )
    raise TypeError("field must be an instance of ModelField")


def _is_model_field(value: Any) -> bool:
    if isinstance(value, v1.ModelField):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(value, v2.ModelField)
    return False


def _is_field_info(value: Any) -> bool:
    if isinstance(value, v1.FieldInfo):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return isinstance(value, v2.FieldInfo)
    return False


def _is_model_class(value: Any) -> bool:
    if lenient_issubclass(value, v1.BaseModel):
        return True
    elif PYDANTIC_V2:
        from . import v2

        return lenient_issubclass(value, v2.BaseModel)
    return False
