from typing import Any, Callable, Iterable, Type

from starlette.datastructures import URL  # noqa: F401
from starlette.datastructures import Address  # noqa: F401
from starlette.datastructures import FormData  # noqa: F401
from starlette.datastructures import Headers  # noqa: F401
from starlette.datastructures import QueryParams  # noqa: F401
from starlette.datastructures import State  # noqa: F401
from starlette.datastructures import UploadFile as StarletteUploadFile


class UploadFile(StarletteUploadFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], v: Any) -> Any:
        if not isinstance(v, StarletteUploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(v)}")
        return v
