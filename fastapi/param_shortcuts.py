from typing import TYPE_CHECKING, Any, Callable, TypeVar

from fastapi import param_functions
from typing_extensions import Annotated


class ParamShortcut:
    def __init__(self, base_func: Callable) -> None:  # type: ignore
        self._base_func = base_func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._base_func(*args, **kwargs)

    def __getitem__(self, args: Any) -> Any:
        if isinstance(args, tuple):
            return Annotated[args[0], self._base_func(**args[1])]
        return Annotated[args, self._base_func()]


if TYPE_CHECKING:  # pragma: nocover
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
    # mypy does not like to extend already annotated params
    # with extra annotation (so need to cheat with these XXX-Ex types):
    from typing import Annotated as BodyEx
    from typing import Annotated as CookieEx
    from typing import Annotated as DependsEx
    from typing import Annotated as FileEx
    from typing import Annotated as FormEx
    from typing import Annotated as HeaderEx
    from typing import Annotated as PathEx
    from typing import Annotated as QueryEx
    from typing import Annotated as SecurityEx
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
    # mypy does not like to extend already annotated params
    # with extra annotation (so need to cheat with these XXX-Ex types):
    BodyEx = Body
    CookieEx = Cookie
    DependsEx = Depends
    FileEx = File
    FormEx = Form
    HeaderEx = Header
    PathEx = Path
    QueryEx = Query
    SecurityEx = Security
