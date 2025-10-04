from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
)

from fastapi.types import IncEx
from pydantic.fields import FieldInfo
from typing_extensions import Literal


@dataclass
class ModelField:
    field_info: "FieldInfo"
    name: str
    mode: Literal["validation", "serialization"] = "validation"
    _version: Literal["v1", "v2"] = "v1"

    @property
    def alias(self) -> str:
        return self._model_field.alias

    @property
    def required(self) -> bool:
        return self._model_field.required

    @property
    def default(self) -> Any:
        return self._model_field.default

    @property
    def type_(self) -> Any:
        return self._model_field.type_

    def __post_init__(self) -> None:
        if self._version == "v1":
            from . import v1

            self._model_field = v1.ModelField(
                field_info=self.field_info, name=self.name
            )
        else:
            assert self._version == "v2"
            from . import v2

            self._model_field = v2.ModelField(
                field_info=self.field_info, name=self.name, mode=self.mode
            )

    def get_default(self) -> Any:
        return self._model_field.get_default()

    def validate(
        self,
        value: Any,
        values: Dict[str, Any] = {},  # noqa: B006
        *,
        loc: Tuple[Union[int, str], ...] = (),
    ) -> Tuple[Any, Union[List[Dict[str, Any]], None]]:
        return self._model_field.validate(value=value, values=values, loc=loc)

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
        return self._model_field.serialize(
            value=value,
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
