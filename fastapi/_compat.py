import types
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Sequence, Set, Tuple, Type, Union

from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION
from typing_extensions import Annotated, Literal

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

UnionType = getattr(types, "UnionType", Union)
NoneType = getattr(types, "UnionType", None)
SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]

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
                # TODO: pv2 is this right?
                # To be able to validate a non-dict (e.g. another Pydantic model) it
                # has to first be converted to a dict

                # Doing this breaks orm_mode with properties
                # use_value = TypeAdapter(Any).dump_python(value)
                # validated = self._type_adapter.validate_python(use_value)
                return self._type_adapter.validate_python(value), None
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
    from pydantic.fields import FieldInfo as FieldInfo
    from pydantic.fields import ModelField as ModelField  # noqa: F401
    from pydantic.fields import Required as Required  # noqa: F401
    from pydantic.fields import Undefined as Undefined
    from pydantic.fields import UndefinedType as UndefinedType  # noqa: F401
    from pydantic.schema import model_process_schema
    from pydantic.typing import evaluate_forwardref as evaluate_forwardref  # noqa: F401
    from pydantic.utils import lenient_issubclass as lenient_issubclass  # noqa: F401

    ErrorDetails = Dict[str, Any]
    GetJsonSchemaHandler = Any
    JsonSchemaValue = Dict[str, Any]

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


def _model_dump(model: Type[BaseModel], **kwargs) -> Dict[str, Any]:
    if PYDANTIC_V2:
        return model.model_dump(**kwargs)
    else:
        return model.dict(**kwargs)


def _get_model_config(model: BaseModel) -> Any:
    if PYDANTIC_V2:
        return model.model_config
    else:
        return model.__config__
