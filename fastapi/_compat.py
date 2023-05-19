from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple, Union

from pydantic import TypeAdapter, ValidationError
from pydantic._internal._fields import Undefined, _UndefinedType
from pydantic._internal._typing_extra import eval_type_lenient
from pydantic._internal._utils import lenient_issubclass as lenient_issubclass
from pydantic.fields import FieldInfo
from pydantic.json_schema import GenerateJsonSchema as GenerateJsonSchema
from pydantic_core import ErrorDetails
from typing_extensions import Annotated

# from pydantic.schema import get_annotation_from_field_info

Required = Undefined
UndefinedType = _UndefinedType
evaluate_forwardref = eval_type_lenient


def get_annotation_from_field_info(
    annotation: Any, field_info: FieldInfo, field_name: str
):
    return annotation


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
        self._type_adapter = TypeAdapter(
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
            return self._type_adapter.validate_python(value), None
        except ValidationError as exc:
            return None, exc.errors()

    def __hash__(self) -> int:
        # Each ModelField is unique for our purposes, to allow making a dict from
        # ModelField to its JSON Schema.
        return id(self)


def _regenerate_error_with_loc(
    *, errors: Sequence[ErrorDetails], loc_prefix: Tuple[str, ...]
):
    # TODO (pv2): should the loc really be reversed?
    updated_loc_errors: List[ErrorDetails] = [
        {**err, "loc": tuple(reversed(loc_prefix + err.get("loc", ())))}
        for err in errors
    ]

    return updated_loc_errors
