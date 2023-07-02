from __future__ import annotations

from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncContextManager,
    Callable,
    ContextManager,
    Generator,
    Generic,
    Iterable,
    List,
    TypeVar,
    Union,
    overload,
)
from warnings import warn

if TYPE_CHECKING:
    from ._testing import TaskInfo
else:
    TaskInfo = object

T = TypeVar("T")
AnyDeprecatedAwaitable = Union[
    "DeprecatedAwaitable",
    "DeprecatedAwaitableFloat",
    "DeprecatedAwaitableList[T]",
    TaskInfo,
]


@overload
async def maybe_async(__obj: TaskInfo) -> TaskInfo:
    ...


@overload
async def maybe_async(__obj: DeprecatedAwaitableFloat) -> float:
    ...


@overload
async def maybe_async(__obj: DeprecatedAwaitableList[T]) -> list[T]:
    ...


@overload
async def maybe_async(__obj: DeprecatedAwaitable) -> None:
    ...


async def maybe_async(
    __obj: AnyDeprecatedAwaitable[T],
) -> TaskInfo | float | list[T] | None:
    """
    Await on the given object if necessary.

    This function is intended to bridge the gap between AnyIO 2.x and 3.x where some functions and
    methods were converted from coroutine functions into regular functions.

    Do **not** try to use this for any other purpose!

    :return: the result of awaiting on the object if coroutine, or the object itself otherwise

    .. versionadded:: 2.2

    """
    return __obj._unwrap()


class _ContextManagerWrapper:
    def __init__(self, cm: ContextManager[T]):
        self._cm = cm

    async def __aenter__(self) -> T:
        return self._cm.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        return self._cm.__exit__(exc_type, exc_val, exc_tb)


def maybe_async_cm(
    cm: ContextManager[T] | AsyncContextManager[T],
) -> AsyncContextManager[T]:
    """
    Wrap a regular context manager as an async one if necessary.

    This function is intended to bridge the gap between AnyIO 2.x and 3.x where some functions and
    methods were changed to return regular context managers instead of async ones.

    :param cm: a regular or async context manager
    :return: an async context manager

    .. versionadded:: 2.2

    """
    if not isinstance(cm, AbstractContextManager):
        raise TypeError("Given object is not an context manager")

    return _ContextManagerWrapper(cm)


def _warn_deprecation(
    awaitable: AnyDeprecatedAwaitable[Any], stacklevel: int = 1
) -> None:
    warn(
        f'Awaiting on {awaitable._name}() is deprecated. Use "await '
        f"anyio.maybe_async({awaitable._name}(...)) if you have to support both AnyIO 2.x "
        f'and 3.x, or just remove the "await" if you are completely migrating to AnyIO 3+.',
        DeprecationWarning,
        stacklevel=stacklevel + 1,
    )


class DeprecatedAwaitable:
    def __init__(self, func: Callable[..., DeprecatedAwaitable]):
        self._name = f"{func.__module__}.{func.__qualname__}"

    def __await__(self) -> Generator[None, None, None]:
        _warn_deprecation(self)
        if False:
            yield

    def __reduce__(self) -> tuple[type[None], tuple[()]]:
        return type(None), ()

    def _unwrap(self) -> None:
        return None


class DeprecatedAwaitableFloat(float):
    def __new__(
        cls, x: float, func: Callable[..., DeprecatedAwaitableFloat]
    ) -> DeprecatedAwaitableFloat:
        return super().__new__(cls, x)

    def __init__(self, x: float, func: Callable[..., DeprecatedAwaitableFloat]):
        self._name = f"{func.__module__}.{func.__qualname__}"

    def __await__(self) -> Generator[None, None, float]:
        _warn_deprecation(self)
        if False:
            yield

        return float(self)

    def __reduce__(self) -> tuple[type[float], tuple[float]]:
        return float, (float(self),)

    def _unwrap(self) -> float:
        return float(self)


class DeprecatedAwaitableList(List[T]):
    def __init__(
        self,
        iterable: Iterable[T] = (),
        *,
        func: Callable[..., DeprecatedAwaitableList[T]],
    ):
        super().__init__(iterable)
        self._name = f"{func.__module__}.{func.__qualname__}"

    def __await__(self) -> Generator[None, None, list[T]]:
        _warn_deprecation(self)
        if False:
            yield

        return list(self)

    def __reduce__(self) -> tuple[type[list[T]], tuple[list[T]]]:
        return list, (list(self),)

    def _unwrap(self) -> list[T]:
        return list(self)


class DeprecatedAsyncContextManager(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> T:
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        pass

    async def __aenter__(self) -> T:
        warn(
            f"Using {self.__class__.__name__} as an async context manager has been deprecated. "
            f'Use "async with anyio.maybe_async_cm(yourcontextmanager) as foo:" if you have to '
            f'support both AnyIO 2.x and 3.x, or just remove the "async" from "async with" if '
            f"you are completely migrating to AnyIO 3+.",
            DeprecationWarning,
        )
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        return self.__exit__(exc_type, exc_val, exc_tb)
