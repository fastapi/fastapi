import re
import warnings
from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from fastapi._compat import may_v1, shared
from fastapi.openapi.constants import REF_TEMPLATE
from fastapi.types import IncEx, ModelNameMap
from pydantic import BaseModel, TypeAdapter, create_model
from pydantic import PydanticSchemaGenerationError as PydanticSchemaGenerationError
from pydantic import PydanticUndefinedAnnotation as PydanticUndefinedAnnotation
from pydantic import ValidationError as ValidationError
from pydantic._internal._schema_generation_shared import (  # type: ignore[attr-defined]
    GetJsonSchemaHandler as GetJsonSchemaHandler,
)
from pydantic._internal._typing_extra import eval_type_lenient
from pydantic._internal._utils import lenient_issubclass as lenient_issubclass
from pydantic.fields import FieldInfo as FieldInfo
from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
from pydantic.json_schema import JsonSchemaValue as JsonSchemaValue
from pydantic_core import CoreSchema as CoreSchema
from pydantic_core import PydanticUndefined, PydanticUndefinedType
from pydantic_core import Url as Url
from typing_extensions import Annotated, Literal, get_args, get_origin

try:
    from pydantic_core.core_schema import (
        with_info_plain_validator_function as with_info_plain_validator_function,
    )
except ImportError:  # pragma: no cover
    from pydantic_core.core_schema import (
        general_plain_validator_function as with_info_plain_validator_function,  # noqa: F401
    )

RequiredParam = PydanticUndefined
Undefined = PydanticUndefined
UndefinedType = PydanticUndefinedType
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
            return None, may_v1._regenerate_error_with_loc(
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


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
) -> Any:
    return annotation


def _model_rebuild(model: Type[BaseModel]) -> None:
    model.model_rebuild()


def _model_dump(
    model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    return model.model_dump(mode=mode, **kwargs)


def _get_model_config(model: BaseModel) -> Any:
    return model.model_config


def get_schema_from_model_field(
    *,
    field: ModelField,
    model_name_map: ModelNameMap,
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
    if "$ref" not in json_schema:
        # TODO remove when deprecating Pydantic v1
        # Ref: https://github.com/pydantic/pydantic/blob/d61792cc42c80b13b23e3ffa74bc37ec7c77f7d1/pydantic/schema.py#L207
        json_schema["title"] = field.field_info.title or field.alias.title().replace(
            "_", " "
        )
    return json_schema


def get_definitions(
    *,
    fields: Sequence[ModelField],
    model_name_map: ModelNameMap,
    separate_input_output_schemas: bool = True,
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
    Dict[str, Dict[str, Any]],
]:
    schema_generator = GenerateJsonSchema(ref_template=REF_TEMPLATE)
    override_mode: Union[Literal["validation"], None] = (
        None if separate_input_output_schemas else "validation"
    )
    flat_models = get_flat_models_from_fields(fields, known_models=set())
    flat_model_fields = [
        ModelField(field_info=FieldInfo(annotation=model), name=model.__name__)
        for model in flat_models
    ]
    input_types = {f.type_ for f in fields}
    unique_flat_model_fields = {
        f for f in flat_model_fields if f.type_ not in input_types
    }

    inputs = [
        (field, override_mode or field.mode, field._type_adapter.core_schema)
        for field in list(fields) + list(unique_flat_model_fields)
    ]
    field_mapping, definitions = schema_generator.generate_definitions(inputs=inputs)
    for item_def in cast(Dict[str, Dict[str, Any]], definitions).values():
        if "description" in item_def:
            item_description = cast(str, item_def["description"]).split("\f")[0]
            item_def["description"] = item_description
    new_mapping, new_definitions = _remap_definitions_and_field_mappings(
        model_name_map=model_name_map,
        definitions=definitions,  # type: ignore[arg-type]
        field_mapping=field_mapping,
    )
    return new_mapping, new_definitions


def _replace_refs(
    *,
    schema: Dict[str, Any],
    old_name_to_new_name_map: Dict[str, str],
) -> Dict[str, Any]:
    new_schema = deepcopy(schema)
    for key, value in new_schema.items():
        if key == "$ref":
            ref_name = schema["$ref"].split("/")[-1]
            if ref_name in old_name_to_new_name_map:
                new_name = old_name_to_new_name_map[ref_name]
                new_schema["$ref"] = REF_TEMPLATE.format(model=new_name)
            else:
                new_schema["$ref"] = schema["$ref"]
            continue
        if isinstance(value, dict):
            new_schema[key] = _replace_refs(
                schema=value,
                old_name_to_new_name_map=old_name_to_new_name_map,
            )
        elif isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict):
                    new_item = _replace_refs(
                        schema=item,
                        old_name_to_new_name_map=old_name_to_new_name_map,
                    )
                    new_value.append(new_item)

                else:
                    new_value.append(item)
            new_schema[key] = new_value
    return new_schema


def _remap_definitions_and_field_mappings(
    *,
    model_name_map: ModelNameMap,
    definitions: Dict[str, Any],
    field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
    ],
) -> Tuple[
    Dict[Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue],
    Dict[str, Any],
]:
    old_name_to_new_name_map = {}
    for field_key, schema in field_mapping.items():
        model = field_key[0].type_
        if model not in model_name_map:
            continue
        new_name = model_name_map[model]
        old_name = schema["$ref"].split("/")[-1]
        if old_name in {f"{new_name}-Input", f"{new_name}-Output"}:
            continue
        old_name_to_new_name_map[old_name] = new_name

    new_field_mapping: Dict[
        Tuple[ModelField, Literal["validation", "serialization"]], JsonSchemaValue
    ] = {}
    for field_key, schema in field_mapping.items():
        new_schema = _replace_refs(
            schema=schema,
            old_name_to_new_name_map=old_name_to_new_name_map,
        )
        new_field_mapping[field_key] = new_schema

    new_definitions = {}
    for key, value in definitions.items():
        if key in old_name_to_new_name_map:
            new_key = old_name_to_new_name_map[key]
        else:
            new_key = key
        new_value = _replace_refs(
            schema=value,
            old_name_to_new_name_map=old_name_to_new_name_map,
        )
        new_definitions[new_key] = new_value
    return new_field_mapping, new_definitions


def is_scalar_field(field: ModelField) -> bool:
    from fastapi import params

    return shared.field_annotation_is_scalar(
        field.field_info.annotation
    ) and not isinstance(field.field_info, params.Body)


def is_sequence_field(field: ModelField) -> bool:
    return shared.field_annotation_is_sequence(field.field_info.annotation)


def is_scalar_sequence_field(field: ModelField) -> bool:
    return shared.field_annotation_is_scalar_sequence(field.field_info.annotation)


def is_bytes_field(field: ModelField) -> bool:
    return shared.is_bytes_or_nonable_bytes_annotation(field.type_)


def is_bytes_sequence_field(field: ModelField) -> bool:
    return shared.is_bytes_sequence_annotation(field.type_)


def copy_field_info(*, field_info: FieldInfo, annotation: Any) -> FieldInfo:
    cls = type(field_info)
    merged_field_info = cls.from_annotation(annotation)
    new_field_info = copy(field_info)
    new_field_info.metadata = merged_field_info.metadata
    new_field_info.annotation = merged_field_info.annotation
    return new_field_info


def serialize_sequence_value(*, field: ModelField, value: Any) -> Sequence[Any]:
    origin_type = get_origin(field.field_info.annotation) or field.field_info.annotation
    assert issubclass(origin_type, shared.sequence_types)  # type: ignore[arg-type]
    return shared.sequence_annotation_to_type[origin_type](value)  # type: ignore[no-any-return]


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


# Duplicate of several schema functions from Pydantic v1 to make them compatible with
# Pydantic v2 and allow mixing the models

TypeModelOrEnum = Union[Type["BaseModel"], Type[Enum]]
TypeModelSet = Set[TypeModelOrEnum]


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9.\-_]", "_", name)


def get_model_name_map(unique_models: TypeModelSet) -> Dict[TypeModelOrEnum, str]:
    name_model_map = {}
    conflicting_names: Set[str] = set()
    for model in unique_models:
        model_name = normalize_name(model.__name__)
        if model_name in conflicting_names:
            model_name = get_long_model_name(model)
            name_model_map[model_name] = model
        elif model_name in name_model_map:
            conflicting_names.add(model_name)
            conflicting_model = name_model_map.pop(model_name)
            name_model_map[get_long_model_name(conflicting_model)] = conflicting_model
            name_model_map[get_long_model_name(model)] = model
        else:
            name_model_map[model_name] = model
    return {v: k for k, v in name_model_map.items()}


def get_flat_models_from_model(
    model: Type["BaseModel"], known_models: Union[TypeModelSet, None] = None
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
            if lenient_issubclass(arg, (BaseModel, Enum)) and arg not in known_models:
                known_models.add(arg)
                if lenient_issubclass(arg, BaseModel):
                    get_flat_models_from_model(arg, known_models=known_models)
            else:
                get_flat_models_from_annotation(arg, known_models=known_models)
    return known_models


def get_flat_models_from_field(
    field: ModelField, known_models: TypeModelSet
) -> TypeModelSet:
    field_type = field.type_
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


def get_long_model_name(model: TypeModelOrEnum) -> str:
    return f"{model.__module__}__{model.__qualname__}".replace(".", "__")
