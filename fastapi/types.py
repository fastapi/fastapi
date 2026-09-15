import types
from collections.abc import Callable
from enum import Enum
from typing import Any, TypedDict, TypeVar, Union

from pydantic import BaseModel
from pydantic.main import IncEx as IncEx

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = dict[type[BaseModel] | type[Enum], str]
DependencyCacheKey = tuple[Callable[..., Any] | None, tuple[str, ...], str]


class _OpenAPIExternalDocsOptional(TypedDict, total=False):
    description: str


class OpenAPIExternalDocs(_OpenAPIExternalDocsOptional):
    url: str


class _OpenAPITagOptional(TypedDict, total=False):
    description: str
    externalDocs: OpenAPIExternalDocs


class OpenAPITag(_OpenAPITagOptional):
    name: str
