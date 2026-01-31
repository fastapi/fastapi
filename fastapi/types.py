import types
from enum import Enum
from typing import Any, Callable, Optional, TypeVar, Union

from pydantic import BaseModel
from pydantic.main import IncEx as IncEx

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = dict[Union[type[BaseModel], type[Enum]], str]
DependencyCacheKey = tuple[Optional[Callable[..., Any]], tuple[str, ...], str]
