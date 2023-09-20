from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from fastapi import params
from fastapi._compat import Undefined
from fastapi.openapi.models import Example
from typing_extensions import Annotated, deprecated

_Unset: Any = Undefined


def Path(  # noqa: N802
    default: Any = ...,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Path(
        default=default,
        default_factory=default_factory,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Query(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Query(
        default=default,
        default_factory=default_factory,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Header(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    convert_underscores: bool = True,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Header(
        default=default,
        default_factory=default_factory,
        alias=alias,
        alias_priority=alias_priority,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        convert_underscores=convert_underscores,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Cookie(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Cookie(
        default=default,
        default_factory=default_factory,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Body(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    embed: bool = False,
    media_type: str = "application/json",
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Body(
        default=default,
        default_factory=default_factory,
        embed=embed,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Form(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    media_type: str = "application/x-www-form-urlencoded",
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.Form(
        default=default,
        default_factory=default_factory,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def File(  # noqa: N802
    default: Any = Undefined,
    *,
    default_factory: Union[Callable[[], Any], None] = _Unset,
    media_type: str = "multipart/form-data",
    alias: Optional[str] = None,
    alias_priority: Union[int, None] = _Unset,
    # TODO: update when deprecating Pydantic v1, import these types
    # validation_alias: str | AliasPath | AliasChoices | None
    validation_alias: Union[str, None] = None,
    serialization_alias: Union[str, None] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    regex: Annotated[
        Optional[str],
        deprecated(
            "Deprecated in FastAPI 0.100.0 and Pydantic v2, use `pattern` instead."
        ),
    ] = None,
    discriminator: Union[str, None] = None,
    strict: Union[bool, None] = _Unset,
    multiple_of: Union[float, None] = _Unset,
    allow_inf_nan: Union[bool, None] = _Unset,
    max_digits: Union[int, None] = _Unset,
    decimal_places: Union[int, None] = _Unset,
    examples: Optional[List[Any]] = None,
    example: Annotated[
        Optional[Any],
        deprecated(
            "Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, "
            "although still supported. Use examples instead."
        ),
    ] = _Unset,
    openapi_examples: Optional[Dict[str, Example]] = None,
    deprecated: Optional[bool] = None,
    include_in_schema: bool = True,
    json_schema_extra: Union[Dict[str, Any], None] = None,
    **extra: Any,
) -> Any:
    return params.File(
        default=default,
        default_factory=default_factory,
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
        strict=strict,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        example=example,
        examples=examples,
        openapi_examples=openapi_examples,
        deprecated=deprecated,
        include_in_schema=include_in_schema,
        json_schema_extra=json_schema_extra,
        **extra,
    )


def Depends(  # noqa: N802
    dependency: Optional[Callable[..., Any]] = None, *, use_cache: bool = True
) -> Any:
    return params.Depends(dependency=dependency, use_cache=use_cache)


def Security(  # noqa: N802
    dependency: Optional[Callable[..., Any]] = None,
    *,
    scopes: Optional[Sequence[str]] = None,
    use_cache: bool = True,
) -> Any:
    return params.Security(dependency=dependency, scopes=scopes, use_cache=use_cache)
