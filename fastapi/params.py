import re
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Any, Literal

from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.openapi.models import Example
from pydantic import AliasChoices, AliasPath, Discriminator
from pydantic.fields import FieldInfo
from typing_extensions import deprecated

from ._compat import (
    Undefined,
)
from .datastructures import _Unset


class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Param(FieldInfo):  # type: ignore[misc]  # ty: ignore[subclass-of-final-class]
    in_: ParamTypes

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        if example is not _Unset:
            warnings.warn(
                "`example` has been deprecated, please use `examples` instead",
                category=FastAPIDeprecationWarning,
                stacklevel=4,
            )
        self.example = example
        self.include_in_schema = include_in_schema
        self.openapi_examples = openapi_examples
        kwargs = {
            "default": default,
            "default_factory": default_factory,
            "alias": alias,
            "title": title,
            "description": description,
            "examples": examples,
            "gt": gt,
            "ge": ge,
            "lt": lt,
            "le": le,
            "min_length": min_length,
            "max_length": max_length,
            "discriminator": discriminator,
            "validate_default": validate_default,
            "union_mode": union_mode,
            "fail_fast": fail_fast,
            "multiple_of": multiple_of,
            "allow_inf_nan": allow_inf_nan,
            "max_digits": max_digits,
            "decimal_places": decimal_places,
        }
        if regex is not None:
            warnings.warn(
                "`regex` has been deprecated, please use `pattern` instead",
                category=FastAPIDeprecationWarning,
                stacklevel=4,
            )
        kwargs["deprecated"] = deprecated

        if serialization_alias in (_Unset, None) and isinstance(alias, str):
            serialization_alias = alias
        if validation_alias in (_Unset, None):
            validation_alias = alias
        kwargs.update(
            {
                "annotation": annotation,
                "alias_priority": alias_priority,
                "validation_alias": validation_alias,
                "serialization_alias": serialization_alias,
                "strict": strict,
                "json_schema_extra": json_schema_extra,
            }
        )
        kwargs["pattern"] = pattern or regex

        use_kwargs = {k: v for k, v in kwargs.items() if v is not _Unset}

        super().__init__(**use_kwargs)  # ty: ignore[invalid-argument-type]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):  # type: ignore[misc]
    in_ = ParamTypes.path

    def __init__(
        self,
        default: Any = ...,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        assert default is ..., "Path parameters cannot have a default value"
        self.in_ = self.in_
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


class Query(Param):  # type: ignore[misc]
    in_ = ParamTypes.query

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


class Header(Param):  # type: ignore[misc]
    in_ = ParamTypes.header

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        convert_underscores: bool = True,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        self.convert_underscores = convert_underscores
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


class Cookie(Param):  # type: ignore[misc]
    in_ = ParamTypes.cookie

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


class Body(FieldInfo):  # type: ignore[misc]  # ty: ignore[subclass-of-final-class]
    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        embed: bool | None = None,
        media_type: str = "application/json",
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        self.embed = embed
        self.media_type = media_type
        if example is not _Unset:
            warnings.warn(
                "`example` has been deprecated, please use `examples` instead",
                category=FastAPIDeprecationWarning,
                stacklevel=4,
            )
        self.example = example
        self.include_in_schema = include_in_schema
        self.openapi_examples = openapi_examples
        kwargs = {
            "default": default,
            "default_factory": default_factory,
            "alias": alias,
            "title": title,
            "description": description,
            "examples": examples,
            "gt": gt,
            "ge": ge,
            "lt": lt,
            "le": le,
            "min_length": min_length,
            "max_length": max_length,
            "discriminator": discriminator,
            "validate_default": validate_default,
            "union_mode": union_mode,
            "fail_fast": fail_fast,
            "multiple_of": multiple_of,
            "allow_inf_nan": allow_inf_nan,
            "max_digits": max_digits,
            "decimal_places": decimal_places,
        }
        if regex is not None:
            warnings.warn(
                "`regex` has been deprecated, please use `pattern` instead",
                category=FastAPIDeprecationWarning,
                stacklevel=4,
            )
        kwargs["deprecated"] = deprecated
        if serialization_alias in (_Unset, None) and isinstance(alias, str):
            serialization_alias = alias
        if validation_alias in (_Unset, None):
            validation_alias = alias
        kwargs.update(
            {
                "annotation": annotation,
                "alias_priority": alias_priority,
                "validation_alias": validation_alias,
                "serialization_alias": serialization_alias,
                "strict": strict,
                "json_schema_extra": json_schema_extra,
            }
        )
        kwargs["pattern"] = pattern or regex

        use_kwargs = {k: v for k, v in kwargs.items() if v is not _Unset}

        super().__init__(**use_kwargs)  # ty: ignore[invalid-argument-type]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Form(Body):  # type: ignore[misc]
    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        media_type: str = "application/x-www-form-urlencoded",
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            media_type=media_type,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


class File(Form):  # type: ignore[misc]
    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        media_type: str = "multipart/form-data",
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        description: str | None = _Unset,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | re.Pattern[str] | None = None,
        regex: Annotated[
            str | None,
            deprecated(
                "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
            ),
        ] = None,
        discriminator: str | Discriminator | None = _Unset,
        strict: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        union_mode: Literal["smart", "left_to_right"] | None = _Unset,
        fail_fast: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = _Unset,
        example: Annotated[
            Any | None,
            deprecated(
                "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
                "although still supported. Use examples instead."
            ),
        ] = _Unset,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = _Unset,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any]
        | Callable[[dict[str, Any]], None]
        | None = _Unset,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            media_type=media_type,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            regex=regex,
            discriminator=discriminator,
            validate_default=validate_default,
            union_mode=union_mode,
            fail_fast=fail_fast,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            example=example,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
        )


@dataclass(frozen=True)
class Depends:
    dependency: Callable[..., Any] | None = None
    use_cache: bool = True
    scope: Literal["function", "request"] | None = None


@dataclass(frozen=True)
class Security(Depends):
    scopes: Sequence[str] | None = None
