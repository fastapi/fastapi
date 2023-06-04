import types
from collections import deque
from copy import copy
from dataclasses import dataclass, is_dataclass
from enum import Enum
from typing import (
    Any,
    Deque,
    Dict,
    FrozenSet,
    List,
    Mapping,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from pydantic import BaseModel, create_model
from pydantic.version import VERSION as PYDANTIC_VERSION
from starlette.datastructures import UploadFile
from typing_extensions import Annotated, Literal, get_args, get_origin

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

UnionType = getattr(types, "UnionType", Union)
NoneType = getattr(types, "UnionType", None)
SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]
ModelNameMap = Dict[Union[Type[BaseModel], Type[Enum]], str]

sequence_types = (Sequence, tuple, set, frozenset, deque)

sequence_annotation_to_type = {
    Sequence: list,
    List: list,
    list: list,
    Tuple: tuple,
    tuple: tuple,
    Set: set,
    set: set,
    FrozenSet: frozenset,
    frozenset: frozenset,
    Deque: deque,
    deque: deque,
}

if PYDANTIC_V2:
    from pydantic import PydanticSchemaGenerationError as PydanticSchemaGenerationError
    from pydantic import TypeAdapter, ValidationError
    from pydantic._internal._fields import Undefined, _UndefinedType
    from pydantic._internal._schema_generation_shared import (
        GetJsonSchemaHandler as GetJsonSchemaHandler,
    )
    from pydantic._internal._typing_extra import eval_type_lenient
    from pydantic._internal._utils import lenient_issubclass as lenient_issubclass
    from pydantic.fields import FieldInfo
    from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
    from pydantic.json_schema import JsonSchemaValue as JsonSchemaValue
    from pydantic_core import ErrorDetails

    Required = Undefined
    UndefinedType = _UndefinedType
    evaluate_forwardref = eval_type_lenient
    Validator = Any

    class BaseConfig:
        pass

    class ErrorWrapper(Exception):
        pass

    @dataclass
    class ModelField:
        field_info: FieldInfo
        name: str

        @property
        def alias(self):
            a = self.field_info.alias
            return a if a is not None else self.name

        @property
        def required(self):
            return self.field_info.is_required()

        @property
        def default(self):
            return self.get_default()

        @property
        def type_(self):
            return self.field_info.annotation

        def __post_init__(self):
            self._type_adapter: TypeAdapter[Any] = TypeAdapter(
                Annotated[self.field_info.annotation, self.field_info]
            )

        def get_default(self) -> Any:
            if self.field_info.is_required():
                return Undefined
            return self.field_info.get_default(call_default_factory=True)

        def validate(
            self,
            value: Any,
            values: Dict[str, Any] = {},  # noqa: B006
            *,
            loc: Union[Tuple[Union[int, str], ...], str] = "",
        ) -> tuple[Any, Union[List[ErrorDetails], None]]:
            try:
                return (
                    self._type_adapter.validate_python(value, from_attributes=True),
                    None,
                )
            except ValidationError as exc:
                if isinstance(loc, tuple):
                    use_loc = loc
                elif loc == "":
                    use_loc = ()
                else:
                    use_loc = (loc,)
                return None, _regenerate_error_with_loc(
                    errors=exc.errors(), loc_prefix=use_loc
                )

        def serialize(
            self,
            value: Any,
            *,
            mode: Literal["json", "python"] = "json",
            include: Union[SetIntStr, DictIntStrAny, None] = None,
            exclude: Union[SetIntStr, DictIntStrAny, None] = None,
            by_alias: bool = True,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
        ) -> Any:
            # TODO: pv2 is this right?
            # To avoid accepting isinstance, and leaking data
            # This seems to break response_by_alias
            # use_value = TypeAdapter(Any).dump_python(value)
            # validated = self._type_adapter.validate_python(use_value)
            return self._type_adapter.dump_python(
                value,
                mode=mode,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )

        def __hash__(self) -> int:
            # Each ModelField is unique for our purposes, to allow making a dict from
            # ModelField to its JSON Schema.
            return id(self)

    def get_model_definitions(**kwargs) -> Dict[str, Any]:
        return {}

else:
    from fastapi.openapi.constants import REF_PREFIX as REF_PREFIX
    from pydantic import BaseConfig as BaseConfig  # noqa: F401
    from pydantic import ValidationError as ValidationError  # noqa: F401
    from pydantic.class_validators import Validator as Validator  # noqa: F401
    from pydantic.error_wrappers import ErrorWrapper as ErrorWrapper  # noqa: F401
    from pydantic.errors import MissingError
    from pydantic.fields import (
        SHAPE_FROZENSET,
        SHAPE_LIST,
        SHAPE_SEQUENCE,
        SHAPE_SET,
        SHAPE_SINGLETON,
        SHAPE_TUPLE,
        SHAPE_TUPLE_ELLIPSIS,
    )
    from pydantic.fields import FieldInfo as FieldInfo
    from pydantic.fields import ModelField as ModelField  # noqa: F401
    from pydantic.fields import Required as Required  # noqa: F401
    from pydantic.fields import Undefined as Undefined
    from pydantic.fields import UndefinedType as UndefinedType  # noqa: F401
    from pydantic.schema import (
        field_schema,
        get_flat_models_from_fields,
        get_model_name_map,
        model_process_schema,
    )
    from pydantic.typing import evaluate_forwardref as evaluate_forwardref  # noqa: F401
    from pydantic.utils import lenient_issubclass as lenient_issubclass  # noqa: F401

    ErrorDetails = Dict[str, Any]
    GetJsonSchemaHandler = Any
    JsonSchemaValue = Dict[str, Any]

    sequence_shapes = {
        SHAPE_LIST,
        SHAPE_SET,
        SHAPE_FROZENSET,
        SHAPE_TUPLE,
        SHAPE_SEQUENCE,
        SHAPE_TUPLE_ELLIPSIS,
    }
    sequence_shape_to_type = {
        SHAPE_LIST: list,
        SHAPE_SET: set,
        SHAPE_TUPLE: tuple,
        SHAPE_SEQUENCE: list,
        SHAPE_TUPLE_ELLIPSIS: list,
    }

    @dataclass
    class GenerateJsonSchema:
        ref_template: str

    class PydanticSchemaGenerationError(Exception):
        pass

    def get_model_definitions(
        *,
        flat_models: Set[Union[Type[BaseModel], Type[Enum]]],
        model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
    ) -> Dict[str, Any]:
        definitions: Dict[str, Dict[str, Any]] = {}
        for model in flat_models:
            m_schema, m_definitions, m_nested_models = model_process_schema(
                model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
            )
            definitions.update(m_definitions)
            model_name = model_name_map[model]
            if "description" in m_schema:
                m_schema["description"] = m_schema["description"].split("\f")[0]
            definitions[model_name] = m_schema
        return definitions

    def is_pv1_scalar_field(field: ModelField) -> bool:
        from fastapi import params

        field_info = field.field_info
        if not (
            field.shape == SHAPE_SINGLETON
            and not lenient_issubclass(field.type_, BaseModel)
            # and not lenient_issubclass(field.type_, sequence_types + (dict,))
            and not lenient_issubclass(field.type_, dict)
            and not field_annotation_is_sequence(field.type_)
            and not is_dataclass(field.type_)
            and not isinstance(field_info, params.Body)
        ):
            return False
        if field.sub_fields:
            if not all(is_pv1_scalar_field(f) for f in field.sub_fields):
                return False
        return True

    def is_pv1_scalar_sequence_field(field: ModelField) -> bool:
        if (field.shape in sequence_shapes) and not lenient_issubclass(
            field.type_, BaseModel
        ):
            if field.sub_fields is not None:
                for sub_field in field.sub_fields:
                    if not is_pv1_scalar_field(sub_field):
                        return False
            return True
        if lenient_issubclass(field.type_, sequence_types):
            return True
        return False


# from pydantic.schema import get_annotation_from_field_info


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
):
    return annotation


def _regenerate_error_with_loc(
    *, errors: Sequence[ErrorDetails], loc_prefix: Tuple[Union[str, int], ...]
):
    updated_loc_errors: List[ErrorDetails] = [
        {**err, "loc": loc_prefix + err.get("loc", ())} for err in errors
    ]

    return updated_loc_errors


def _model_rebuild(model: Type[BaseModel]) -> None:
    if PYDANTIC_V2:
        model.model_rebuild()
    else:
        model.update_forward_refs()


def _model_dump(
    model: Type[BaseModel], mode: Literal["json", "python"] = "json", **kwargs
) -> Dict[str, Any]:
    if PYDANTIC_V2:
        return model.model_dump(mode=mode, **kwargs)
    else:
        return model.dict(**kwargs)


def _get_model_config(model: BaseModel) -> Any:
    if PYDANTIC_V2:
        return model.model_config
    else:
        return model.__config__


def get_schema_from_model_field(
    *,
    field: ModelField,
    schema_generator: GenerateJsonSchema,
    model_name_map: ModelNameMap,
) -> Dict[str, Any]:
    # This expects that GenerateJsonSchema was already used to generate the definitions
    # core_ref = field._type_adapter.core_schema.get("schema", {}).get("schema", {}).get("schema_ref")
    # core_ref = field._type_adapter.core_schema.get("schema", {}).get("schema_ref")
    # if core_ref:
    #     def_ref = schema_generator.core_to_defs_refs.get((core_ref, "validation"))
    #     json_schema = schema_generator.definitions[def_ref]
    # else:
    # json_schema = schema_generator.generate_inner(field._type_adapter.core_schema)
    if PYDANTIC_V2:
        json_schema = schema_generator.generate_inner(field._type_adapter.core_schema)
        if "$ref" not in json_schema:
            # TODO remove when deprecating Pydantic v1
            # Ref: https://github.com/pydantic/pydantic/blob/d61792cc42c80b13b23e3ffa74bc37ec7c77f7d1/pydantic/schema.py#L207
            json_schema[
                "title"
            ] = field.field_info.title or field.alias.title().replace("_", " ")
        return json_schema
    else:
        return field_schema(
            field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )[0]


def get_compat_model_name_map(fields: List[ModelField]) -> ModelNameMap:
    if PYDANTIC_V2:
        return {}
    else:
        models = get_flat_models_from_fields(fields, known_models=set())
        return get_model_name_map(models)


def get_definitions(
    *,
    fields: List[ModelField],
    schema_generator: GenerateJsonSchema,
    model_name_map: ModelNameMap,
) -> Dict[str, Any]:
    if PYDANTIC_V2:
        inputs = [
            (field, "validation", field._type_adapter.core_schema) for field in fields
        ]
        _, definitions = schema_generator.generate_definitions(inputs=inputs)
        return definitions
    else:
        models = get_flat_models_from_fields(fields, known_models=set())
        return get_model_definitions(flat_models=models, model_name_map=model_name_map)


def _annotation_is_sequence(annotation: type[Any] | None) -> bool:
    if lenient_issubclass(annotation, (str, bytes)):
        return False
    return lenient_issubclass(annotation, sequence_types)


def field_annotation_is_sequence(annotation: type[Any] | None) -> bool:
    return _annotation_is_sequence(annotation) or _annotation_is_sequence(
        get_origin(annotation)
    )


def value_is_sequence(value: Any) -> bool:
    return isinstance(value, sequence_types) and not isinstance(value, (str, bytes))


def _annotation_is_complex(annotation: Type[Any] | None) -> bool:
    return (
        lenient_issubclass(annotation, (BaseModel, Mapping, UploadFile))
        or _annotation_is_sequence(annotation)
        or is_dataclass(annotation)
    )


def field_annotation_is_complex(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        return any(field_annotation_is_complex(arg) for arg in get_args(annotation))

    return (
        _annotation_is_complex(annotation)
        or _annotation_is_complex(origin)
        or hasattr(origin, "__pydantic_core_schema__")
        or hasattr(origin, "__get_pydantic_core_schema__")
    )


def field_annotation_is_scalar(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        return all(field_annotation_is_scalar(arg) for arg in get_args(annotation))

    # handle Ellipsis here to make tuple[int, ...] work nicely
    return annotation is Ellipsis or not field_annotation_is_complex(annotation)


def field_annotation_is_scalar_sequence(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one_scalar_sequence = False
        for arg in get_args(annotation):
            if field_annotation_is_scalar_sequence(arg):
                at_least_one_scalar_sequence = True
                continue
            elif not field_annotation_is_scalar(arg):
                return False
        return at_least_one_scalar_sequence
    return field_annotation_is_sequence(annotation) and all(
        field_annotation_is_scalar(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_scalar_field(field: ModelField) -> bool:
    from fastapi import params

    if PYDANTIC_V2:
        return field_annotation_is_scalar(
            field.field_info.annotation
        ) and not isinstance(field.field_info, params.Body)
    else:
        return is_pv1_scalar_field(field)


def is_sequence_field(field: ModelField) -> bool:
    if PYDANTIC_V2:
        return field_annotation_is_sequence(field.field_info.annotation)
    else:
        return field.shape in sequence_shapes or field.type_ in sequence_types


def is_scalar_sequence_field(field: ModelField) -> bool:
    if PYDANTIC_V2:
        return field_annotation_is_scalar_sequence(field.field_info.annotation)
    else:
        return is_pv1_scalar_sequence_field(field)


def is_bytes_or_nonable_bytes_annotation(annotation: Any) -> bool:
    if lenient_issubclass(annotation, bytes):
        return True
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if lenient_issubclass(arg, bytes):
                return True
    return False


def is_uploadfile_or_nonable_uploadfile_annotation(annotation: Any) -> bool:
    if lenient_issubclass(annotation, UploadFile):
        return True
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if lenient_issubclass(arg, UploadFile):
                return True
    return False


def is_bytes_sequence_annotation(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one_bytes_sequence = False
        for arg in get_args(annotation):
            if is_bytes_sequence_annotation(arg):
                at_least_one_bytes_sequence = True
                continue
        return at_least_one_bytes_sequence
    return field_annotation_is_sequence(annotation) and all(
        is_bytes_or_nonable_bytes_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_uploadfile_sequence_annotation(annotation: type[Any] | None) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one_bytes_sequence = False
        for arg in get_args(annotation):
            if is_uploadfile_sequence_annotation(arg):
                at_least_one_bytes_sequence = True
                continue
        return at_least_one_bytes_sequence
    return field_annotation_is_sequence(annotation) and all(
        is_uploadfile_or_nonable_uploadfile_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    if PYDANTIC_V2:
        return type(field_info).from_annotation(annotation)
    else:
        return copy(field_info)


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    if PYDANTIC_V2:
        origin_type = (
            get_origin(field.field_info.annotation) or field.field_info.annotation
        )
        assert issubclass(origin_type, sequence_types)
        return sequence_annotation_to_type[origin_type](value)
    else:
        return sequence_shape_to_type[field.shape](value)


def get_missing_field_error(loc: Tuple[str, ...]) -> Dict[str, Any]:
    if PYDANTIC_V2:
        error = ValidationError.from_exception_data(
            "Field required", [{"type": "missing", "loc": loc, "input": {}}]
        ).errors()[0]
        error["input"] = None
        return error
    else:
        missing_field_error = ErrorWrapper(MissingError(), loc=loc)
        return missing_field_error


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> Type[BaseModel]:
    if PYDANTIC_V2:
        field_params = {f.name: (f.field_info.annotation, f.field_info) for f in fields}
        BodyModel: Type[BaseModel] = create_model(model_name, **field_params)
        return BodyModel
    else:
        BodyModel: Type[BaseModel] = create_model(model_name)
        for f in fields:
            BodyModel.__fields__[f.name] = f
        return BodyModel
