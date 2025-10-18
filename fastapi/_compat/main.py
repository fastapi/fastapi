# mypy: ignore-errors
from functools import lru_cache
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Type,
)

from fastapi._compat.shared import PYDANTIC_V2, lenient_issubclass
from fastapi._compat.lazy_import import get_v1_if_loaded, v1_isinstance, v1_lenient_issubclass
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
    from .v2 import _get_model_config as _get_model_config
    from .v2 import _model_dump as _model_dump
    from .v2 import _model_rebuild as _model_rebuild
    from .v2 import copy_field_info as copy_field_info
    from .v2 import create_body_model as create_body_model
    from .v2 import evaluate_forwardref as evaluate_forwardref
    from .v2 import get_annotation_from_field_info as get_annotation_from_field_info
    from .v2 import get_definitions as get_definitions
    from .v2 import get_missing_field_error as get_missing_field_error
    from .v2 import get_schema_from_model_field as get_schema_from_model_field
    from .v2 import is_bytes_field as is_bytes_field
    from .v2 import is_bytes_sequence_field as is_bytes_sequence_field
    from .v2 import is_scalar_field as is_scalar_field
    from .v2 import is_scalar_sequence_field as is_scalar_sequence_field
    from .v2 import is_sequence_field as is_sequence_field
    from .v2 import serialize_sequence_value as serialize_sequence_value
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
    from .v1 import _get_model_config as _get_model_config
    from .v1 import _model_dump as _model_dump
    from .v1 import _model_rebuild as _model_rebuild
    from .v1 import copy_field_info as copy_field_info
    from .v1 import create_body_model as create_body_model
    from .v1 import evaluate_forwardref as evaluate_forwardref
    from .v1 import get_annotation_from_field_info as get_annotation_from_field_info
    from .v1 import get_definitions as get_definitions
    from .v1 import get_missing_field_error as get_missing_field_error
    from .v1 import get_schema_from_model_field as get_schema_from_model_field
    from .v1 import is_bytes_field as is_bytes_field
    from .v1 import is_bytes_sequence_field as is_bytes_sequence_field
    from .v1 import is_scalar_field as is_scalar_field
    from .v1 import is_scalar_sequence_field as is_scalar_sequence_field
    from .v1 import is_sequence_field as is_sequence_field
    from .v1 import serialize_sequence_value as serialize_sequence_value
    from .v1 import (
        with_info_plain_validator_function as with_info_plain_validator_function,
    )


@lru_cache
def get_cached_model_fields(model: Type[BaseModel]) -> List[ModelField]:
    if v1_lenient_issubclass(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        return v1.get_model_fields(model)
    else:
        from . import v2
        return v2.get_model_fields(model)  # type: ignore[return-value]


def _is_undefined(value: object) -> bool:
    if v1_isinstance(value, "UndefinedType"):
        return True
    elif PYDANTIC_V2:
        from pydantic_core import PydanticUndefined
        return value is PydanticUndefined
    else:
        return False


def _get_model_config(model: BaseModel) -> Any:
    if v1_isinstance(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        return v1._get_model_config(model)
    elif PYDANTIC_V2:
        from . import v2
        return v2._get_model_config(model)
    else:
        return getattr(model, "__config__", None)


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    if v1_isinstance(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        return v1._model_dump(model, mode=mode, **kwargs)
    if PYDANTIC_V2:
        from . import v2
        return v2._model_dump(model, mode=mode, **kwargs)
    else:
        return model.dict(**kwargs)


def _is_error_wrapper(exc: Exception) -> bool:
    if v1_isinstance(exc, "ErrorWrapper"):
        return True
    elif PYDANTIC_V2:
        from . import v2
        return v2._is_error_wrapper(exc)
    else:
        return False


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if v1_isinstance(field_info, "FieldInfo"):
        v1 = get_v1_if_loaded()
        return v1.copy_field_info(field_info=field_info, annotation=annotation)
    else:
        from . import v2
        return v2.copy_field_info(field_info=field_info, annotation=annotation)


def create_body_model(
    *, fields: List[ModelField], model_name: str
) -> Type[BaseModel]:
    if fields and v1_isinstance(fields[0], "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.create_body_model(fields=fields, model_name=model_name)
    else:
        from . import v2
        return v2.create_body_model(fields=fields, model_name=model_name)


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    if v1_isinstance(field_info, "FieldInfo"):
        v1 = get_v1_if_loaded()
        return v1.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )
    else:
        from . import v2
        return v2.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )


def is_bytes_field(field: ModelField) -> bool:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.is_bytes_field(field)
    else:
        from . import v2
        return v2.is_bytes_field(field)


def is_bytes_sequence_field(field: ModelField) -> bool:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.is_bytes_sequence_field(field)
    else:
        from . import v2
        return v2.is_bytes_sequence_field(field)


def is_scalar_field(field: ModelField) -> bool:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.is_scalar_field(field)
    else:
        from . import v2
        return v2.is_scalar_field(field)


def is_scalar_sequence_field(field: ModelField) -> bool:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.is_scalar_sequence_field(field)
    else:
        from . import v2
        return v2.is_scalar_sequence_field(field)


def is_sequence_field(field: ModelField) -> bool:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.is_sequence_field(field)
    else:
        from . import v2
        return v2.is_sequence_field(field)


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.serialize_sequence_value(field=field, value=value)
    else:
        from . import v2
        return v2.serialize_sequence_value(field=field, value=value)


def get_compat_model_name_map(fields: List[ModelField]) -> ModelNameMap:
    v1 = get_v1_if_loaded()
    v1_model_fields = [field for field in fields if v1_isinstance(field, "ModelField")] if v1 else []
    v1_flat_models = v1.get_flat_models_from_fields(v1_model_fields, known_models=set()) if v1 and v1_model_fields else set()
    all_flat_models = v1_flat_models
    if PYDANTIC_V2:
        from . import v2
        v2_model_fields = [field for field in fields if not v1_isinstance(field, "ModelField")]
        v2_flat_models = v2.get_flat_models_from_fields(v2_model_fields, known_models=set())
        all_flat_models = v1_flat_models | v2_flat_models
        model_name_map = v2.get_model_name_map(all_flat_models)
        return model_name_map
    model_name_map = v1.get_model_name_map(all_flat_models) if v1 else {}
    return model_name_map


def get_definitions(
    *,
    fields: List[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], Dict[str, Any]],
    Dict[str, Dict[str, Any]],
]:
    v1 = get_v1_if_loaded()
    v1_fields = [field for field in fields if v1_isinstance(field, "ModelField")] if v1 else []
    if v1_fields and v1:
        v1_field_maps, v1_definitions = v1.get_definitions(
            fields=v1_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
    else:
        v1_field_maps: Dict[Tuple[ModelField, Literal["validation", "serialization"]], Dict[str, Any]] = {}
        v1_definitions: Dict[str, Dict[str, Any]] = {}
    if PYDANTIC_V2:
        from . import v2
        v2_fields = [field for field in fields if not v1_isinstance(field, "ModelField")]
        v2_field_maps, v2_definitions = v2.get_definitions(
            fields=v2_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
        all_field_maps = {**v1_field_maps, **v2_field_maps}
        all_definitions = {**v1_definitions, **v2_definitions}
        return all_field_maps, all_definitions
    return v1_field_maps, v1_definitions


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], Dict[str, Any]
    ],
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,
            separate_input_output_schemas=separate_input_output_schemas,
        )
    else:
        from . import v2
        return v2.get_schema_from_model_field(
            field=field,
            model_name_map=model_name_map,
            field_mapping=field_mapping,
            separate_input_output_schemas=separate_input_output_schemas,
        )


def _is_model_field(value: Any) -> bool:
    if v1_isinstance(value, "ModelField"):
        return True
    elif PYDANTIC_V2:
        from . import v2
        return v2._is_model_field(value)
    else:
        return False


def _is_model_class(value: Any) -> bool:
    if v1_lenient_issubclass(value, "BaseModel"):
        return True
    elif PYDANTIC_V2:
        from . import v2
        return v2._is_model_class(value)
    else:
        return False


def get_missing_field_error(loc: Tuple[str, ...], field: ModelField) -> Dict[str, Any]:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        return v1.get_missing_field_error(loc=loc, field=field)
    else:
        from . import v2
        return v2.get_missing_field_error(loc=loc, field=field)


def evaluate_forwardref(type_: Any, globalns: Dict[str, Any], localns: Dict[str, Any]) -> Any:
    if PYDANTIC_V2:
        from . import v2
        return v2.evaluate_forwardref(type_, globalns, localns)
    else:
        v1 = get_v1_if_loaded()
        return v1.evaluate_forwardref(type_, globalns, localns)


def with_info_plain_validator_function(
    func: Any,
    info_argname: str = "info",
) -> Any:
    if PYDANTIC_V2:
        try:
            from pydantic_core.core_schema import (
                with_info_plain_validator_function as pydantic_core_with_info,
            )
        except ImportError:  # pragma: no cover
            from pydantic_core.core_schema import (
                general_plain_validator_function as pydantic_core_with_info,
            )
        return pydantic_core_with_info(func)
    else:
        v1 = get_v1_if_loaded()
        return v1.with_info_plain_validator_function(func=func, info_argname=info_argname)


def _model_rebuild(model) -> None:
    if v1_lenient_issubclass(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        v1._model_rebuild(model)
    elif PYDANTIC_V2:
        from . import v2
        v2._model_rebuild(model)
    else:
        model.update_forward_refs()