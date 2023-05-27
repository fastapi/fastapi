import types
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Set, Tuple, Union

from pydantic.version import VERSION as PYDANTIC_VERSION
from typing_extensions import Annotated, Literal

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

UnionType = getattr(types, "UnionType", Union)
NoneType = getattr(types, "UnionType", None)
SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]

if PYDANTIC_V2:
    from pydantic import TypeAdapter, ValidationError
    from pydantic._internal._fields import Undefined, _UndefinedType
    from pydantic._internal._typing_extra import eval_type_lenient
    from pydantic._internal._utils import lenient_issubclass as lenient_issubclass
    from pydantic.fields import FieldInfo
    from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
    from pydantic_core import ErrorDetails

    Required = Undefined
    UndefinedType = _UndefinedType
    evaluate_forwardref = eval_type_lenient

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

else:
    from pydantic.fields import FieldInfo as FieldInfo
    from pydantic.fields import ModelField as ModelField  # noqa: F401
    from pydantic.fields import Undefined as Undefined
    from pydantic.fields import UndefinedType as UndefinedType  # noqa: F401
    from pydantic.typing import evaluate_forwardref as evaluate_forwardref  # noqa: F401

    ErrorDetails = Dict[str, Any]

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
