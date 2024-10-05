from collections import deque
from copy import copy
from dataclasses import dataclass, is_dataclass
from functools import lru_cache
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

from fastapi.types import IncEx, UnionType
from pydantic import BaseModel, TypeAdapter, ValidationError, create_model
from pydantic._internal._typing_extra import eval_type_lenient
from pydantic._internal._utils import lenient_issubclass as lenient_issubclass
from pydantic.annotated_handlers import GetJsonSchemaHandler as GetJsonSchemaHandler
from pydantic.fields import FieldInfo
from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
from pydantic.json_schema import JsonSchemaValue as JsonSchemaValue
from pydantic.version import VERSION as P_VERSION
from pydantic_core import CoreSchema as CoreSchema
from pydantic_core import PydanticUndefined, PydanticUndefinedType
from pydantic_core import Url as Url
from pydantic_core.core_schema import (
    with_info_plain_validator_function as with_info_plain_validator_function,
)
from starlette.datastructures import UploadFile
from typing_extensions import Annotated, Literal, get_args, get_origin

# Reassign variable to make it reexported for mypy
PYDANTIC_VERSION = P_VERSION
PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")


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

sequence_types = tuple(sequence_annotation_to_type.keys())

Required = PydanticUndefined
Undefined = PydanticUndefined
UndefinedType = PydanticUndefinedType
evaluate_forwardref = eval_type_lenient
Validator = Any


@dataclass
class ModelField:
    field_info: FieldInfo
    name: str
    mode: Literal["validation", "serialization"] = "validation"

    @property
    def alias(self) -> str:
        a = self.field_info.alias
        return a if a is not None else self.name

    @property
    def required(self) -> bool:
        return self.field_info.is_required()

    @property
    def default(self) -> Any:
        return self.get_default()

    @property
    def type_(self) -> Any:
        return self.field_info.annotation

    def __post_init__(self) -> None:
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
        loc: Tuple[Union[int, str], ...] = (),
    ) -> Tuple[Any, Union[List[Dict[str, Any]], None]]:
        try:
            return (
                self._type_adapter.validate_python(value, from_attributes=True),
                None,
            )
        except ValidationError as exc:
            return None, _regenerate_error_with_loc(
                errors=exc.errors(include_url=False), loc_prefix=loc
            )

    def serialize(
        self,
        value: Any,
        *,
        mode: Literal["json", "python"] = "json",
        include: Union[IncEx, None] = None,
        exclude: Union[IncEx, None] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Any:
        # What calls this code passes a value that already called
        # self._type_adapter.validate_python(value)
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


def get_schema_from_model_field(
    *,
    field: ModelField,
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
    ],
    separate_input_output_schemas: bool = True,
) -> Dict[str, Any]:
    override_mode: Union[Literal["validation"], None] = (
        None if separate_input_output_schemas else "validation"
    )
    # This expects that GenerateJsonSchema was already used to generate the definitions
    json_schema = field_mapping[(field, override_mode or field.mode)]
    return json_schema


def get_definitions(
    *,
    fields: List[ModelField],
    schema_generator: GenerateJsonSchema,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
    Dict[str, Dict[str, Any]],
]:
    override_mode: Union[Literal["validation"], None] = (
        None if separate_input_output_schemas else "validation"
    )

    inputs: list[
        tuple[ModelField, Literal["validation", "serialization"], CoreSchema]
    ] = [
        (field, override_mode or field.mode, field._type_adapter.core_schema)
        for field in fields
    ]

    field_mapping, definitions = schema_generator.generate_definitions(inputs=inputs)
    return field_mapping, definitions  # type: ignore[return-value]


def is_scalar_field(field: ModelField) -> bool:
    from fastapi import params

    return field_annotation_is_scalar(field.field_info.annotation) and not isinstance(
        field.field_info, params.Body
    )


def is_sequence_field(field: ModelField) -> bool:
    return field_annotation_is_sequence(field.field_info.annotation)


def is_scalar_sequence_field(field: ModelField) -> bool:
    return field_annotation_is_scalar_sequence(field.field_info.annotation)


def is_bytes_field(field: ModelField) -> bool:
    return is_bytes_or_nonable_bytes_annotation(field.type_)


def is_bytes_sequence_field(field: ModelField) -> bool:
    return is_bytes_sequence_annotation(field.type_)


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    cls = type(field_info)
    merged_field_info = cls.from_annotation(annotation)
    new_field_info = copy(field_info)
    new_field_info.metadata = merged_field_info.metadata
    new_field_info.annotation = merged_field_info.annotation
    return new_field_info


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    origin_type = get_origin(field.field_info.annotation) or field.field_info.annotation
    assert issubclass(origin_type, sequence_types)  # type: ignore[arg-type]
    return sequence_annotation_to_type[origin_type](value)  # type: ignore[no-any-return]


def get_missing_field_error(loc: Tuple[str, ...]) -> Dict[str, Any]:
    error = ValidationError.from_exception_data(
        "Field required", [{"type": "missing", "loc": loc, "input": {}}]
    ).errors(include_url=False)[0]
    error["input"] = None
    return error  # type: ignore[return-value]


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> Type[BaseModel]:
    field_params = {f.name: (f.field_info.annotation, f.field_info) for f in fields}
    BodyModel: Type[BaseModel] = create_model(model_name, **field_params)  # type: ignore[call-overload]
    return BodyModel


def get_model_fields(model: Type[BaseModel]) -> List[ModelField]:
    return [
        ModelField(field_info=field_info, name=name)
        for name, field_info in model.model_fields.items()
    ]


def _regenerate_error_with_loc(
    *, errors: Sequence[Any], loc_prefix: Tuple[Union[str, int], ...]
) -> List[Dict[str, Any]]:
    updated_loc_errors: List[Any] = [
        {**err, "loc": loc_prefix + err.get("loc", ())} for err in errors
    ]

    return updated_loc_errors


def _annotation_is_sequence(annotation: Union[Type[Any], None]) -> bool:
    if lenient_issubclass(annotation, (str, bytes)):
        return False
    return lenient_issubclass(annotation, sequence_types)


def field_annotation_is_sequence(annotation: Union[Type[Any], None]) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        for arg in get_args(annotation):
            if field_annotation_is_sequence(arg):
                return True
        return False
    return _annotation_is_sequence(annotation) or _annotation_is_sequence(
        get_origin(annotation)
    )


def value_is_sequence(value: Any) -> bool:
    return isinstance(value, sequence_types) and not isinstance(value, (str, bytes))  # type: ignore[arg-type]


def _annotation_is_complex(annotation: Union[Type[Any], None]) -> bool:
    return (
        lenient_issubclass(annotation, (BaseModel, Mapping, UploadFile))
        or _annotation_is_sequence(annotation)
        or is_dataclass(annotation)
    )


def field_annotation_is_complex(annotation: Union[Type[Any], None]) -> bool:
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
    # handle Ellipsis here to make tuple[int, ...] work nicely
    return annotation is Ellipsis or not field_annotation_is_complex(annotation)


def field_annotation_is_scalar_sequence(annotation: Union[Type[Any], None]) -> bool:
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


def is_bytes_sequence_annotation(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one = False
        for arg in get_args(annotation):
            if is_bytes_sequence_annotation(arg):
                at_least_one = True
                continue
        return at_least_one
    return field_annotation_is_sequence(annotation) and all(
        is_bytes_or_nonable_bytes_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


def is_uploadfile_sequence_annotation(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union or origin is UnionType:
        at_least_one = False
        for arg in get_args(annotation):
            if is_uploadfile_sequence_annotation(arg):
                at_least_one = True
                continue
        return at_least_one
    return field_annotation_is_sequence(annotation) and all(
        is_uploadfile_or_nonable_uploadfile_annotation(sub_annotation)
        for sub_annotation in get_args(annotation)
    )


@lru_cache
def get_cached_model_fields(model: Type[BaseModel]) -> List[ModelField]:
    return get_model_fields(model)
