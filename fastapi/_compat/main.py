from functools import lru_cache
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Type,
)

from fastapi._compat.lazy_import import (
    get_v1_if_loaded,
    v1_isinstance,
    v1_lenient_issubclass,
)
from fastapi._compat.shared import PYDANTIC_V2
from fastapi.types import ModelNameMap
from pydantic import BaseModel
from typing_extensions import Literal

from .model_field import ModelField

# Type aliases for compatibility
FieldInfo = Any

# Dynamic imports will be handled in functions


@lru_cache
def get_cached_model_fields(model: Type[BaseModel]) -> Any:
    if v1_lenient_issubclass(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return []
        return v1.get_model_fields(model)

    from . import v2

    return v2.get_model_fields(model)


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
        if v1 is None:
            return None
        return v1._get_model_config(model)

    if PYDANTIC_V2:
        from . import v2

        return v2._get_model_config(model)

    return getattr(model, "__config__", None)


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    if v1_isinstance(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return {}
        return v1._model_dump(model, mode=mode, **kwargs)

    if PYDANTIC_V2:
        from . import v2

        return v2._model_dump(model, mode=mode, **kwargs)

    return model.dict(**kwargs)


def _is_error_wrapper(exc: Exception) -> bool:
    if v1_isinstance(exc, "ErrorWrapper"):
        return True

    # Pydantic v2 doesn't have ErrorWrapper, so return False
    if PYDANTIC_V2:
        return False

    return False


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if v1_isinstance(field_info, "FieldInfo"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return field_info
        return v1.copy_field_info(field_info=field_info, annotation=annotation)

    from . import v2

    return v2.copy_field_info(field_info=field_info, annotation=annotation)


def create_body_model(*, fields: List[ModelField], model_name: str) -> Any:
    if fields and v1_isinstance(fields[0], "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return BaseModel
        return v1.create_body_model(fields=fields, model_name=model_name)

    from . import v2

    return v2.create_body_model(fields=fields, model_name=model_name)


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    if v1_isinstance(field_info, "FieldInfo"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return annotation
        return v1.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )
    else:
        from . import v2

        return v2.get_annotation_from_field_info(
            annotation=annotation, field_info=field_info, field_name=field_name
        )


def is_bytes_field(field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return False
        return v1.is_bytes_field(field)

    from . import v2

    return v2.is_bytes_field(field)


def is_bytes_sequence_field(field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return False
        return v1.is_bytes_sequence_field(field)

    from . import v2

    return v2.is_bytes_sequence_field(field)


def is_scalar_field(field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return False
        return v1.is_scalar_field(field)

    from . import v2

    return v2.is_scalar_field(field)


def is_scalar_sequence_field(field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return False
        return v1.is_scalar_sequence_field(field)

    from . import v2

    return v2.is_scalar_sequence_field(field)


def is_sequence_field(field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return False
        return v1.is_sequence_field(field)

    from . import v2

    return v2.is_sequence_field(field)


def serialize_sequence_value(*, field: ModelField, value: Any) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return []
        return v1.serialize_sequence_value(field=field, value=value)

    from . import v2

    return v2.serialize_sequence_value(field=field, value=value)


def get_compat_model_name_map(fields: List[ModelField]) -> Any:
    v1 = get_v1_if_loaded()
    v1_model_fields = (
        [field for field in fields if v1_isinstance(field, "ModelField")] if v1 else []
    )
    v1_flat_models = (
        v1.get_flat_models_from_fields(v1_model_fields, known_models=set())
        if v1 and v1_model_fields
        else set()
    )
    all_flat_models = v1_flat_models
    if PYDANTIC_V2:
        from . import v2

        v2_model_fields = [
            field for field in fields if not v1_isinstance(field, "ModelField")
        ]
        v2_flat_models = v2.get_flat_models_from_fields(
            v2_model_fields, known_models=set()
        )
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
    v1_fields = (
        [field for field in fields if v1_isinstance(field, "ModelField")] if v1 else []
    )
    if v1_fields and v1:
        v1_field_maps, v1_definitions = v1.get_definitions(
            fields=v1_fields,
            model_name_map=model_name_map,
            separate_input_output_schemas=separate_input_output_schemas,
        )
    else:
        v1_field_maps = {}
        v1_definitions = {}
    if PYDANTIC_V2:
        from . import v2

        v2_fields = [
            field for field in fields if not v1_isinstance(field, "ModelField")
        ]
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
) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return {}
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


def get_missing_field_error(loc: Tuple[str, ...], field: ModelField) -> Any:
    if v1_isinstance(field, "ModelField"):
        v1 = get_v1_if_loaded()
        if v1 is None:
            return {"type": "missing", "loc": loc, "msg": "field required"}
        return v1.get_missing_field_error(loc=loc, field=field)
    else:
        from . import v2

        return v2.get_missing_field_error(loc=loc, field=field)


def evaluate_forwardref(
    type_: Any, globalns: Dict[str, Any], localns: Dict[str, Any]
) -> Any:
    if PYDANTIC_V2:
        from . import v2

        return v2.evaluate_forwardref(type_, globalns, localns)
    else:
        v1 = get_v1_if_loaded()
        if v1 is None:
            return type_
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
        if v1 is None:
            return func
        return v1.with_info_plain_validator_function(
            func=func, info_argname=info_argname
        )


def _model_rebuild(model: Any) -> None:
    if v1_lenient_issubclass(model, "BaseModel"):
        v1 = get_v1_if_loaded()
        if v1 is not None:
            v1._model_rebuild(model)
    elif PYDANTIC_V2:
        from . import v2

        v2._model_rebuild(model)
    else:
        model.update_forward_refs()
