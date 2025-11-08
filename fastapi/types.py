import types
from enum import Enum
from typing import Any, Callable, Dict, Optional, Set, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import Literal, TypeAlias

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = Dict[Union[Type[BaseModel], Type[Enum]], str]
IncEx = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any]]

EndpointDependencyScope: TypeAlias = Union[Literal["request", "function"], None]
LifespanDependencyScope: TypeAlias = Literal["lifespan"]
DependencyScope: TypeAlias = Union[LifespanDependencyScope, EndpointDependencyScope]

LifespanDependencyCacheKey = Union[
    Tuple[Callable[..., Any], Union[str, int]], Callable[..., Any]
]
EndpointDependencyCacheKey = Tuple[Optional[Callable[..., Any]], Tuple[str, ...], str]
