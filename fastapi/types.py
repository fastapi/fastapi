import types
from enum import Enum
from typing import Any, Callable, Dict, Optional, Set, Tuple, Type, TypeVar, Union

from pydantic import BaseModel

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = Dict[Union[Type[BaseModel], Type[Enum]], str]
IncEx = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any]]
DependencyCacheKey = Tuple[Optional[Callable[..., Any]], Tuple[str, ...], str]
