from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import partial
from inspect import getmro, isclass
from typing import TYPE_CHECKING, Generic, Type, TypeVar, cast, overload

if TYPE_CHECKING:
    from typing import Self

_BaseExceptionT_co = TypeVar("_BaseExceptionT_co", bound=BaseException, covariant=True)
_BaseExceptionT = TypeVar("_BaseExceptionT", bound=BaseException)
_ExceptionT_co = TypeVar("_ExceptionT_co", bound=Exception, covariant=True)
_ExceptionT = TypeVar("_ExceptionT", bound=Exception)


def check_direct_subclass(
    exc: BaseException, parents: tuple[type[BaseException]]
) -> bool:
    for cls in getmro(exc.__class__)[:-1]:
        if cls in parents:
            return True

    return False


def get_condition_filter(
    condition: type[_BaseExceptionT]
    | tuple[type[_BaseExceptionT], ...]
    | Callable[[_BaseExceptionT_co], bool]
) -> Callable[[_BaseExceptionT_co], bool]:
    if isclass(condition) and issubclass(
        cast(Type[BaseException], condition), BaseException
    ):
        return partial(check_direct_subclass, parents=(condition,))
    elif isinstance(condition, tuple):
        if all(isclass(x) and issubclass(x, BaseException) for x in condition):
            return partial(check_direct_subclass, parents=condition)
    elif callable(condition):
        return cast("Callable[[BaseException], bool]", condition)

    raise TypeError("expected a function, exception type or tuple of exception types")


class BaseExceptionGroup(BaseException, Generic[_BaseExceptionT_co]):
    """A combination of multiple unrelated exceptions."""

    def __new__(
        cls, __message: str, __exceptions: Sequence[_BaseExceptionT_co]
    ) -> Self:
        if not isinstance(__message, str):
            raise TypeError(f"argument 1 must be str, not {type(__message)}")
        if not isinstance(__exceptions, Sequence):
            raise TypeError("second argument (exceptions) must be a sequence")
        if not __exceptions:
            raise ValueError(
                "second argument (exceptions) must be a non-empty sequence"
            )

        for i, exc in enumerate(__exceptions):
            if not isinstance(exc, BaseException):
                raise ValueError(
                    f"Item {i} of second argument (exceptions) is not an " f"exception"
                )

        if cls is BaseExceptionGroup:
            if all(isinstance(exc, Exception) for exc in __exceptions):
                cls = ExceptionGroup

        if issubclass(cls, Exception):
            for exc in __exceptions:
                if not isinstance(exc, Exception):
                    if cls is ExceptionGroup:
                        raise TypeError(
                            "Cannot nest BaseExceptions in an ExceptionGroup"
                        )
                    else:
                        raise TypeError(
                            f"Cannot nest BaseExceptions in {cls.__name__!r}"
                        )

        instance = super().__new__(cls, __message, __exceptions)
        instance._message = __message
        instance._exceptions = __exceptions
        return instance

    def add_note(self, note: str) -> None:
        if not isinstance(note, str):
            raise TypeError(
                f"Expected a string, got note={note!r} (type {type(note).__name__})"
            )

        if not hasattr(self, "__notes__"):
            self.__notes__: list[str] = []

        self.__notes__.append(note)

    @property
    def message(self) -> str:
        return self._message

    @property
    def exceptions(
        self,
    ) -> tuple[_BaseExceptionT_co | BaseExceptionGroup[_BaseExceptionT_co], ...]:
        return tuple(self._exceptions)

    @overload
    def subgroup(
        self, __condition: type[_BaseExceptionT] | tuple[type[_BaseExceptionT], ...]
    ) -> BaseExceptionGroup[_BaseExceptionT] | None:
        ...

    @overload
    def subgroup(
        self: Self, __condition: Callable[[_BaseExceptionT_co], bool]
    ) -> Self | None:
        ...

    def subgroup(
        self: Self,
        __condition: type[_BaseExceptionT]
        | tuple[type[_BaseExceptionT], ...]
        | Callable[[_BaseExceptionT_co], bool],
    ) -> BaseExceptionGroup[_BaseExceptionT] | Self | None:
        condition = get_condition_filter(__condition)
        modified = False
        if condition(self):
            return self

        exceptions: list[BaseException] = []
        for exc in self.exceptions:
            if isinstance(exc, BaseExceptionGroup):
                subgroup = exc.subgroup(__condition)
                if subgroup is not None:
                    exceptions.append(subgroup)

                if subgroup is not exc:
                    modified = True
            elif condition(exc):
                exceptions.append(exc)
            else:
                modified = True

        if not modified:
            return self
        elif exceptions:
            group = self.derive(exceptions)
            group.__cause__ = self.__cause__
            group.__context__ = self.__context__
            group.__traceback__ = self.__traceback__
            return group
        else:
            return None

    @overload
    def split(
        self: Self,
        __condition: type[_BaseExceptionT] | tuple[type[_BaseExceptionT], ...],
    ) -> tuple[BaseExceptionGroup[_BaseExceptionT] | None, Self | None]:
        ...

    @overload
    def split(
        self: Self, __condition: Callable[[_BaseExceptionT_co], bool]
    ) -> tuple[Self | None, Self | None]:
        ...

    def split(
        self: Self,
        __condition: type[_BaseExceptionT]
        | tuple[type[_BaseExceptionT], ...]
        | Callable[[_BaseExceptionT_co], bool],
    ) -> (
        tuple[BaseExceptionGroup[_BaseExceptionT] | None, Self | None]
        | tuple[Self | None, Self | None]
    ):
        condition = get_condition_filter(__condition)
        if condition(self):
            return self, None

        matching_exceptions: list[BaseException] = []
        nonmatching_exceptions: list[BaseException] = []
        for exc in self.exceptions:
            if isinstance(exc, BaseExceptionGroup):
                matching, nonmatching = exc.split(condition)
                if matching is not None:
                    matching_exceptions.append(matching)

                if nonmatching is not None:
                    nonmatching_exceptions.append(nonmatching)
            elif condition(exc):
                matching_exceptions.append(exc)
            else:
                nonmatching_exceptions.append(exc)

        matching_group: Self | None = None
        if matching_exceptions:
            matching_group = self.derive(matching_exceptions)
            matching_group.__cause__ = self.__cause__
            matching_group.__context__ = self.__context__
            matching_group.__traceback__ = self.__traceback__

        nonmatching_group: Self | None = None
        if nonmatching_exceptions:
            nonmatching_group = self.derive(nonmatching_exceptions)
            nonmatching_group.__cause__ = self.__cause__
            nonmatching_group.__context__ = self.__context__
            nonmatching_group.__traceback__ = self.__traceback__

        return matching_group, nonmatching_group

    def derive(self: Self, __excs: Sequence[_BaseExceptionT_co]) -> Self:
        eg = BaseExceptionGroup(self.message, __excs)
        if hasattr(self, "__notes__"):
            # Create a new list so that add_note() only affects one exceptiongroup
            eg.__notes__ = list(self.__notes__)

        return eg

    def __str__(self) -> str:
        suffix = "" if len(self._exceptions) == 1 else "s"
        return f"{self.message} ({len(self._exceptions)} sub-exception{suffix})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r}, {self._exceptions!r})"


class ExceptionGroup(BaseExceptionGroup[_ExceptionT_co], Exception):
    def __new__(cls, __message: str, __exceptions: Sequence[_ExceptionT_co]) -> Self:
        return super().__new__(cls, __message, __exceptions)

    if TYPE_CHECKING:

        @property
        def exceptions(
            self,
        ) -> tuple[_ExceptionT_co | ExceptionGroup[_ExceptionT_co], ...]:
            ...

        @overload  # type: ignore[override]
        def subgroup(
            self, __condition: type[_ExceptionT] | tuple[type[_ExceptionT], ...]
        ) -> ExceptionGroup[_ExceptionT] | None:
            ...

        @overload
        def subgroup(
            self: Self, __condition: Callable[[_ExceptionT_co], bool]
        ) -> Self | None:
            ...

        def subgroup(
            self: Self,
            __condition: type[_ExceptionT]
            | tuple[type[_ExceptionT], ...]
            | Callable[[_ExceptionT_co], bool],
        ) -> ExceptionGroup[_ExceptionT] | Self | None:
            return super().subgroup(__condition)

        @overload  # type: ignore[override]
        def split(
            self: Self, __condition: type[_ExceptionT] | tuple[type[_ExceptionT], ...]
        ) -> tuple[ExceptionGroup[_ExceptionT] | None, Self | None]:
            ...

        @overload
        def split(
            self: Self, __condition: Callable[[_ExceptionT_co], bool]
        ) -> tuple[Self | None, Self | None]:
            ...

        def split(
            self: Self,
            __condition: type[_ExceptionT]
            | tuple[type[_ExceptionT], ...]
            | Callable[[_ExceptionT_co], bool],
        ) -> (
            tuple[ExceptionGroup[_ExceptionT] | None, Self | None]
            | tuple[Self | None, Self | None]
        ):
            return super().split(__condition)
