from typing import Any, Callable, Sequence, TypeVar, overload

from fastapi import params


def Path(  # noqa: N802
    default: Any,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    deprecated: bool = None,
    **extra: Any,
) -> Any:
    return params.Path(
        default=default,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        deprecated=deprecated,
        **extra,
    )


def Query(  # noqa: N802
    default: Any,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    deprecated: bool = None,
    **extra: Any,
) -> Any:
    return params.Query(
        default,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        deprecated=deprecated,
        **extra,
    )


def Header(  # noqa: N802
    default: Any,
    *,
    alias: str = None,
    convert_underscores: bool = True,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    deprecated: bool = None,
    **extra: Any,
) -> Any:
    return params.Header(
        default,
        alias=alias,
        convert_underscores=convert_underscores,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        deprecated=deprecated,
        **extra,
    )


def Cookie(  # noqa: N802
    default: Any,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    deprecated: bool = None,
    **extra: Any,
) -> Any:
    return params.Cookie(
        default,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        deprecated=deprecated,
        **extra,
    )


def Body(  # noqa: N802
    default: Any,
    *,
    embed: bool = False,
    media_type: str = "application/json",
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    **extra: Any,
) -> Any:
    return params.Body(
        default,
        embed=embed,
        media_type=media_type,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        **extra,
    )


def Form(  # noqa: N802
    default: Any,
    *,
    media_type: str = "application/x-www-form-urlencoded",
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    **extra: Any,
) -> Any:
    return params.Form(
        default,
        media_type=media_type,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        **extra,
    )


def File(  # noqa: N802
    default: Any,
    *,
    media_type: str = "multipart/form-data",
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    **extra: Any,
) -> Any:
    return params.File(
        default,
        media_type=media_type,
        alias=alias,
        title=title,
        description=description,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        min_length=min_length,
        max_length=max_length,
        regex=regex,
        **extra,
    )


T = TypeVar("T")


@overload
def Depends(dependency: Callable[..., T], *, use_cache: bool = True) -> T:
    ...


@overload
def Depends(dependency: None = None, *, use_cache: bool = True) -> Any:
    ...


def Depends(  # noqa: N802
    dependency: Callable = None, *, use_cache: bool = True
) -> Any:
    return params.Depends(dependency=dependency, use_cache=use_cache)


@overload
def Security(
    dependency: Callable[..., T],
    *,
    scopes: Sequence[str] = None,
    use_cache: bool = True,
) -> T:
    ...


@overload
def Security(
    dependency: None = None, *, scopes: Sequence[str] = None, use_cache: bool = True
) -> Any:
    ...


def Security(  # noqa: N802
    dependency: Callable = None, *, scopes: Sequence[str] = None, use_cache: bool = True
) -> Any:
    return params.Security(dependency=dependency, scopes=scopes, use_cache=use_cache)
