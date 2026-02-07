import re
import warnings
from collections.abc import Sequence
from copy import copy
from dataclasses import dataclass, is_dataclass
from enum import Enum
from functools import lru_cache
from typing import (
    Annotated,
    Any,
    Union,
    cast,
)

from fastapi._compat import lenient_issubclass, shared
from fastapi.openapi.constants import REF_TEMPLATE
from fastapi.types import IncEx, ModelNameMap, UnionType
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, create_model
from pydantic import PydanticSchemaGenerationError as PydanticSchemaGenerationError
from pydantic import PydanticUndefinedAnnotation as PydanticUndefinedAnnotation
from pydantic import ValidationError as ValidationError
from pydantic._internal._schema_generation_shared import (  # type: ignore[attr-defined]
    GetJsonSchemaHandler as GetJsonSchemaHandler,
)
from pydantic._internal._typing_extra import eval_type_lenient
from pydantic.fields import FieldInfo as FieldInfo
from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
from pydantic.json_schema import JsonSchemaValue as JsonSchemaValue
from pydantic_core import CoreSchema as CoreSchema
from pydantic_core import PydanticUndefined
from pydantic_core import Url as Url
from pydantic_core.core_schema import (
    with_info_plain_validator_function as with_info_plain_validator_function,
)
from typing_extensions import Literal, get_args, get_origin

RequiredParam = PydanticUndefined
Undefined = PydanticUndefined
evaluate_forwardref = eval_type_lenient

# TODO: remove when dropping support for Pydantic < v2.12.3
_Attrs = {
    "default": ...,
    "default_factory": None,
    "alias": None,
    "alias_priority": None,
    "validation_alias": None,
    "serialization_alias": None,
    "title": None,
    "field_title_generator": None,
    "description": None,
    "examples": None,
    "exclude": None,
    "exclude_if": None,
    "discriminator": None,
    "deprecated": None,
    "json_schema_extra": None,
    "frozen": None,
    "validate_default": None,
    "repr": True,
    "init": None,
    "init_var": None,
    "kw_only": None,
}


# TODO: remove when dropping support for Pydantic < v2.12.3
def asdict(field_info: FieldInfo) -> dict[str, Any]:
    attributes = {}
    for attr in _Attrs:
        value = getattr(field_info, attr, Undefined)
        if value is not Undefined:
            attributes[attr] = value
    return {
        "annotation": field_info.annotation,
        "metadata": field_info.metadata,
        "attributes": attributes,
    }


@dataclass
class ModelField:
    field_info: FieldInfo
    name: str
    mode: Literal["validation", "serialization"] = "validation"
    config: Union[ConfigDict, None] = None

    @property
    def alias(self) -> str:
        a = self.field_info.alias
        return a if a is not None else self.name

    @property
    def validation_alias(self) -> Union[str, None]:
        va = self.field_info.validation_alias
        if isinstance(va, str) and va:
            return va
        return None

    @property
    def serialization_alias(self) -> Union[str, None]:
        sa = self.field_info.serialization_alias
        return sa or None

    @property
    def default(self) -> Any:
        return self.get_default()

    def __post_init__(self) -> None:
        with warnings.catch_warnings():
            # Pydantic >= 2.12.0 warns about field specific metadata that is unused
            # (e.g. `TypeAdapter(Annotated[int, Field(alias='b')])`). In some cases, we
            # end up building the type adapter from a model field annotation so we
            # need to ignore the warning:
            if shared.PYDANTIC_VERSION_MINOR_TUPLE >= (2, 12):
                from pydantic.warnings import UnsupportedFieldAttributeWarning

                warnings.simplefilter(
                    "ignore", category=UnsupportedFieldAttributeWarning
                )
            # TODO: remove after setting the min Pydantic to v2.12.3
            # that adds asdict(), and use self.field_info.asdict() instead
            field_dict = asdict(self.field_info)
            annotated_args = (
                field_dict["annotation"],
                *field_dict["metadata"],
                # this FieldInfo needs to be created again so that it doesn't include
                # the old field info metadata and only the rest of the attributes
                Field(**field_dict["attributes"]),
            )
            self._type_adapter: TypeAdapter[Any] = TypeAdapter(
                Annotated[annotated_args],
                config=self.config,
            )

    def get_default(self) -> Any:
        if self.field_info.is_required():
            return Undefined
        return self.field_info.get_default(call_default_factory=True)

    def validate(
        self,
        value: Any,
        values: dict[str, Any] = {},  # noqa: B006
        *,
        loc: tuple[Union[int, str], ...] = (),
    ) -> tuple[Any, list[dict[str, Any]]]:
        try:
            return (
                self._type_adapter.validate_python(value, from_attributes=True),
                [],
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


def _has_computed_fields(field: ModelField) -> bool:
    computed_fields = field._type_adapter.core_schema.get("schema", {}).get(
        "computed_fields", []
    )
    return len(computed_fields) > 0


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
    field_mapping: dict[
        tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
    ],
    separate_input_output_schemas: bool = True,
) -> dict[str, Any]:
    override_mode: Union[Literal["validation"], None] = (
        None
        if (separate_input_output_schemas or _has_computed_fields(field))
        else "validation"
    )
    field_alias = (
        (field.validation_alias or field.alias)
        if field.mode == "validation"
        else (field.serialization_alias or field.alias)
    )

    # This expects that GenerateJsonSchema was already used to generate the definitions
    json_schema = field_mapping[(field, override_mode or field.mode)]
    if "$ref" not in json_schema:
        # TODO remove when deprecating Pydantic v1
        # Ref: https://github.com/pydantic/pydantic/blob/d61792cc42c80b13b23e3ffa74bc37ec7c77f7d1/pydantic/schema.py#L207
        json_schema["title"] = field.field_info.title or field_alias.title().replace(
            "_", " "
        )
    return json_schema


def get_definitions(
    *,
    fields: Sequence[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> tuple[
    dict[tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
    dict[str, dict[str, Any]],
]:
    schema_generator = GenerateJsonSchema(ref_template=REF_TEMPLATE)
    validation_fields = [field for field in fields if field.mode == "validation"]
    serialization_fields = [field for field in fields if field.mode == "serialization"]
    flat_validation_models = get_flat_models_from_fields(
        validation_fields, known_models=set()
    )
    flat_serialization_models = get_flat_models_from_fields(
        serialization_fields, known_models=set()
    )
    flat_validation_model_fields = [
        ModelField(
            field_info=FieldInfo(annotation=model),
            name=model.__name__,
            mode="validation",
        )
        for model in flat_validation_models
    ]
    flat_serialization_model_fields = [
        ModelField(
            field_info=FieldInfo(annotation=model),
            name=model.__name__,
            mode="serialization",
        )
        for model in flat_serialization_models
    ]
    flat_model_fields = flat_validation_model_fields + flat_serialization_model_fields
    input_types = {f.field_info.annotation for f in fields}
    unique_flat_model_fields = {
        f for f in flat_model_fields if f.field_info.annotation not in input_types
    }
    inputs = [
        (
            field,
            (
                field.mode
                if (separate_input_output_schemas or _has_computed_fields(field))
                else "validation"
            ),
            field._type_adapter.core_schema,
        )
        for field in list(fields) + list(unique_flat_model_fields)
    ]
    field_mapping, definitions = schema_generator.generate_definitions(inputs=inputs)
    for item_def in cast(dict[str, dict[str, Any]], definitions).values():
        if "description" in item_def:
            item_description = cast(str, item_def["description"]).split("\f")[0]
            item_def["description"] = item_description
    # definitions: dict[DefsRef, dict[str, Any]]
    # but mypy complains about general str in other places that are not declared as
    # DefsRef, although DefsRef is just str:
    # DefsRef = NewType('DefsRef', str)
    # So, a cast to simplify the types here
    return field_mapping, cast(dict[str, dict[str, Any]], definitions)


def is_scalar_field(field: ModelField) -> bool:
    from fastapi import params

    return shared.field_annotation_is_scalar(
        field.field_info.annotation
    ) and not isinstance(field.field_info, params.Body)


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    cls = type(field_info)
    merged_field_info = cls.from_annotation(annotation)
    new_field_info = copy(field_info)
    new_field_info.metadata = merged_field_info.metadata
    new_field_info.annotation = merged_field_info.annotation
    return new_field_info


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    origin_type = get_origin(field.field_info.annotation) or field.field_info.annotation
    if origin_type is Union or origin_type is UnionType:  # Handle optional sequences
        union_args = get_args(field.field_info.annotation)
        for union_arg in union_args:
            if union_arg is type(None):
                continue
            origin_type = get_origin(union_arg) or union_arg
            break
    assert issubclass(origin_type, shared.sequence_types)  # type: ignore[arg-type]
    return shared.sequence_annotation_to_type[origin_type](value)  # type: ignore[no-any-return,index]


def get_missing_field_error(loc: tuple[Union[int, str], ...]) -> dict[str, Any]:
    error = ValidationError.from_exception_data(
        "Field required", [{"type": "missing", "loc": loc, "input": {}}]
    ).errors(include_url=False)[0]
    error["input"] = None
    return error  # type: ignore[return-value]


def create_body_model(
    *, fields: Sequence[ModelField], model_name: str
) -> type[BaseModel]:
    field_params = {f.name: (f.field_info.annotation, f.field_info) for f in fields}
    BodyModel: type[BaseModel] = create_model(model_name, **field_params)  # type: ignore[call-overload]
    return BodyModel


def get_model_fields(model: type[BaseModel]) -> list[ModelField]:
    model_fields: list[ModelField] = []
    for name, field_info in model.model_fields.items():
        type_ = field_info.annotation
        if lenient_issubclass(type_, (BaseModel, dict)) or is_dataclass(type_):
            model_config = None
        else:
            model_config = model.model_config
        model_fields.append(
            ModelField(
                field_info=field_info,
                name=name,
                config=model_config,
            )
        )
    return model_fields


@lru_cache
def get_cached_model_fields(model: type[BaseModel]) -> list[ModelField]:
    return get_model_fields(model)


# Duplicate of several schema functions from Pydantic v1 to make them compatible with
# Pydantic v2 and allow mixing the models

TypeModelOrEnum = Union[type["BaseModel"], type[Enum]]
TypeModelSet = set[TypeModelOrEnum]


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9.\-_]", "_", name)


def get_model_name_map(unique_models: TypeModelSet) -> dict[TypeModelOrEnum, str]:
    name_model_map = {}
    for model in unique_models:
        model_name = normalize_name(model.__name__)
        name_model_map[model_name] = model
    return {v: k for k, v in name_model_map.items()}


def get_flat_models_from_model(
    model: type["BaseModel"], known_models: Union[TypeModelSet, None] = None
) -> TypeModelSet:
    known_models = known_models or set()
    fields = get_model_fields(model)
    get_flat_models_from_fields(fields, known_models=known_models)
    return known_models


def get_flat_models_from_annotation(
    annotation: Any, known_models: TypeModelSet
) -> TypeModelSet:
    origin = get_origin(annotation)
    if origin is not None:
        for arg in get_args(annotation):
            if lenient_issubclass(arg, (BaseModel, Enum)):
                if arg not in known_models:
                    known_models.add(arg)  # type: ignore[arg-type]
                    if lenient_issubclass(arg, BaseModel):
                        get_flat_models_from_model(arg, known_models=known_models)
            else:
                get_flat_models_from_annotation(arg, known_models=known_models)
    return known_models


def get_flat_models_from_field(
    field: ModelField, known_models: TypeModelSet
) -> TypeModelSet:
    field_type = field.field_info.annotation
    if lenient_issubclass(field_type, BaseModel):
        if field_type in known_models:
            return known_models
        known_models.add(field_type)
        get_flat_models_from_model(field_type, known_models=known_models)
    elif lenient_issubclass(field_type, Enum):
        known_models.add(field_type)
    else:
        get_flat_models_from_annotation(field_type, known_models=known_models)
    return known_models


def get_flat_models_from_fields(
    fields: Sequence[ModelField], known_models: TypeModelSet
) -> TypeModelSet:
    for field in fields:
        get_flat_models_from_field(field, known_models=known_models)
    return known_models


def _regenerate_error_with_loc(
    *, errors: Sequence[Any], loc_prefix: tuple[Union[str, int], ...]
) -> list[dict[str, Any]]:
    updated_loc_errors: list[Any] = [
        {**err, "loc": loc_prefix + err.get("loc", ())} for err in errors
    ]

    return updated_loc_errors
