import types
from enum import Enum
from typing import Any, Callable, Dict, Generic, Optional, Set, Tuple, Type, TypeVar, Union

from pydantic import BaseModel

DecoratedCallable = TypeVar("DecoratedCallable", bound=Callable[..., Any])
UnionType = getattr(types, "UnionType", Union)
ModelNameMap = Dict[Union[Type[BaseModel], Type[Enum]], str]
IncEx = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any]]


StateType = TypeVar("StateType", bound=Dict[str, Any])


class RequestState:
    pass


class TypedState(RequestState, Generic[StateType]):
    def __init__(self, _state: StateType) -> None:
        super().__init__()
        self._state = _state

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            # TODO: Restrict overriding of the _state attribute
            return object.__getattribute__(self, item)
        if item in self._state:
            return self._state[item]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._state[key] = value


DependencyCacheKey = Tuple[Optional[Callable[..., Any]], Tuple[str, ...], str]
