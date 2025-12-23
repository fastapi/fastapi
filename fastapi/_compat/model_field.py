from typing import (
    Any,
    Union,
)

from fastapi.types import IncEx
from pydantic.fields import FieldInfo
from typing_extensions import Literal, Protocol


class ModelField(Protocol):
    field_info: "FieldInfo"
    name: str
    mode: Literal["validation", "serialization"] = "validation"
    _version: Literal["v1", "v2"] = "v1"

    @property
    def alias(self) -> str: ...

    @property
    def required(self) -> bool: ...

    @property
    def default(self) -> Any: ...

    @property
    def type_(self) -> Any: ...

    def get_default(self) -> Any: ...

    def validate(
        self,
        value: Any,
        values: dict[str, Any] = {},  # noqa: B006
        *,
        loc: tuple[Union[int, str], ...] = (),
    ) -> tuple[Any, Union[list[dict[str, Any]], None]]: ...

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
    ) -> Any: ...
