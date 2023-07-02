import asyncio
import functools
import sys
import typing
from types import TracebackType

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Protocol
else:  # pragma: no cover
    from typing import Protocol


def is_async_callable(obj: typing.Any) -> bool:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


T_co = typing.TypeVar("T_co", covariant=True)


# TODO: once 3.8 is the minimum supported version (27 Jun 2023)
# this can just become
# class AwaitableOrContextManager(
#     typing.Awaitable[T_co],
#     typing.AsyncContextManager[T_co],
#     typing.Protocol[T_co],
# ):
#     pass
class AwaitableOrContextManager(Protocol[T_co]):
    def __await__(self) -> typing.Generator[typing.Any, None, T_co]:
        ...  # pragma: no cover

    async def __aenter__(self) -> T_co:
        ...  # pragma: no cover

    async def __aexit__(
        self,
        __exc_type: typing.Optional[typing.Type[BaseException]],
        __exc_value: typing.Optional[BaseException],
        __traceback: typing.Optional[TracebackType],
    ) -> typing.Union[bool, None]:
        ...  # pragma: no cover


class SupportsAsyncClose(Protocol):
    async def close(self) -> None:
        ...  # pragma: no cover


SupportsAsyncCloseType = typing.TypeVar(
    "SupportsAsyncCloseType", bound=SupportsAsyncClose, covariant=False
)


class AwaitableOrContextManagerWrapper(typing.Generic[SupportsAsyncCloseType]):
    __slots__ = ("aw", "entered")

    def __init__(self, aw: typing.Awaitable[SupportsAsyncCloseType]) -> None:
        self.aw = aw

    def __await__(self) -> typing.Generator[typing.Any, None, SupportsAsyncCloseType]:
        return self.aw.__await__()

    async def __aenter__(self) -> SupportsAsyncCloseType:
        self.entered = await self.aw
        return self.entered

    async def __aexit__(self, *args: typing.Any) -> typing.Union[None, bool]:
        await self.entered.close()
        return None
