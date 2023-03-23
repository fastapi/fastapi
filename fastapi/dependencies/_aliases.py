from inspect import Parameter
from typing import Any, Dict, Optional, TypeVar, cast

from fastapi.params import Deferred, Depends
from fastapi.requests import Request
from typing_extensions import Annotated, get_args, get_origin

T = TypeVar("T")


LifespanState = Dict[str, Any]


def get_type(param: Parameter) -> type[Any]:
    annotation = param.annotation
    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


class _FromLifespan:
    def __init__(self, param: Parameter) -> None:
        self._type = get_type(param)
        self._key: Optional[str] = None

    def __call__(self, request: Request) -> Any:
        state = cast(LifespanState, request["state"])
        if self._key is None:
            for key, value in state.items():
                if isinstance(value, self._type):
                    self._key = key
                    break
        if self._key is None:
            raise RuntimeError(f"{self._type} not found in lifespan state")
        return state[self._key]


def _from_lifespan(param: Parameter) -> Depends:
    return Depends(_FromLifespan(param))


FromLifespan = Annotated[T, Deferred(_from_lifespan)]
