from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    cast,
)

from pydantic.fields import (
    FieldInfo,
    ModelField,
    NoArgAnyCallable,
    Undefined,
    Validator,
)
from starlette.datastructures import UploadFile as StarletteUploadFile

if TYPE_CHECKING:
    from pydantic.fields import BaseConfig, BoolUndefined, ReprArgs


class MultiAliasablModelField(ModelField):
    sub_fields: Optional[List["MultiAliasablModelField"]]  # type: ignore
    key_field: Optional["MultiAliasablModelField"]  # type: ignore

    def __init__(
        self,
        *,
        name: str,
        type_: Type[Any],
        class_validators: Optional[Dict[str, Validator]],
        model_config: Type["BaseConfig"],
        default: Any = None,
        default_factory: Optional[NoArgAnyCallable] = None,
        required: "BoolUndefined" = Undefined,
        alias: str = None,
        aliases: Optional[Tuple[str]] = None,
        field_info: Optional[FieldInfo] = None,
    ) -> None:
        self.aliases = aliases
        super().__init__(
            name=name,
            type_=type_,
            class_validators=class_validators,
            model_config=model_config,
            default=default,
            default_factory=default_factory,
            required=required,
            alias=alias,
            field_info=field_info,
        )

    def __repr_args__(self) -> "ReprArgs":
        args = cast(list, super().__repr_args__())
        if self.aliases:
            args.append(("aliases", self.aliases))
        return args


class UploadFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], v: Any) -> Any:
        if not isinstance(v, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        return v
