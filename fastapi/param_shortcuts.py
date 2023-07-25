from typing import TYPE_CHECKING, Annotated, Any, Callable, TypeVar

from fastapi import param_functions


class ParamShortcut:
    def __init__(self, base_func: Callable) -> None:  # type: ignore
        self._base_func = base_func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._base_func(*args, **kwargs)

    def __getitem__(self, args: Any) -> Any:
        if isinstance(args, tuple):
            return Annotated[args[0], self._base_func(**args[1])]
        return Annotated[args, self._base_func()]


if TYPE_CHECKING:
    # mypy cheats
    T = TypeVar("T")
    Body = Annotated[T, param_functions.Body()]
    Cookie = Annotated[T, param_functions.Cookie()]
    Depends = Annotated[T, param_functions.Depends()]
    File = Annotated[T, param_functions.File()]
    Form = Annotated[T, param_functions.Form()]
    Header = Annotated[T, param_functions.Header()]
    Path = Annotated[T, param_functions.Path()]
    Query = Annotated[T, param_functions.Query()]
    Security = Annotated[T, param_functions.Security()]
else:
    Body = ParamShortcut(param_functions.Body)
    Cookie = ParamShortcut(param_functions.Cookie)
    Depends = ParamShortcut(param_functions.Depends)
    File = ParamShortcut(param_functions.File)
    Form = ParamShortcut(param_functions.Form)
    Header = ParamShortcut(param_functions.Header)
    Path = ParamShortcut(param_functions.Path)
    Query = ParamShortcut(param_functions.Query)
    Security = ParamShortcut(param_functions.Security)
