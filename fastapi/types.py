import types
from enum import Enum
from typing import Any, Callable, Optional, TypeVar, Union

from pydantic import BaseModel

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = dict[Union[type[BaseModel], type[Enum]], str]
IncEx = Union[set[int], set[str], dict[int, Any], dict[str, Any]]
DependencyCacheKey = tuple[Optional[Callable[..., Any]], tuple[str, ...], str]
