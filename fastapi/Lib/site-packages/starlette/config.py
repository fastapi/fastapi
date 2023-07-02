import os
import typing
from collections.abc import MutableMapping
from pathlib import Path


class undefined:
    pass


class EnvironError(Exception):
    pass


class Environ(MutableMapping):
    def __init__(self, environ: typing.MutableMapping = os.environ):
        self._environ = environ
        self._has_been_read: typing.Set[typing.Any] = set()

    def __getitem__(self, key: typing.Any) -> typing.Any:
        self._has_been_read.add(key)
        return self._environ.__getitem__(key)

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        if key in self._has_been_read:
            raise EnvironError(
                f"Attempting to set environ['{key}'], but the value has already been "
                "read."
            )
        self._environ.__setitem__(key, value)

    def __delitem__(self, key: typing.Any) -> None:
        if key in self._has_been_read:
            raise EnvironError(
                f"Attempting to delete environ['{key}'], but the value has already "
                "been read."
            )
        self._environ.__delitem__(key)

    def __iter__(self) -> typing.Iterator:
        return iter(self._environ)

    def __len__(self) -> int:
        return len(self._environ)


environ = Environ()

T = typing.TypeVar("T")


class Config:
    def __init__(
        self,
        env_file: typing.Optional[typing.Union[str, Path]] = None,
        environ: typing.Mapping[str, str] = environ,
        env_prefix: str = "",
    ) -> None:
        self.environ = environ
        self.env_prefix = env_prefix
        self.file_values: typing.Dict[str, str] = {}
        if env_file is not None and os.path.isfile(env_file):
            self.file_values = self._read_file(env_file)

    @typing.overload
    def __call__(self, key: str, *, default: None) -> typing.Optional[str]:
        ...

    @typing.overload
    def __call__(self, key: str, cast: typing.Type[T], default: T = ...) -> T:
        ...

    @typing.overload
    def __call__(
        self, key: str, cast: typing.Type[str] = ..., default: str = ...
    ) -> str:
        ...

    @typing.overload
    def __call__(
        self,
        key: str,
        cast: typing.Callable[[typing.Any], T] = ...,
        default: typing.Any = ...,
    ) -> T:
        ...

    @typing.overload
    def __call__(
        self, key: str, cast: typing.Type[str] = ..., default: T = ...
    ) -> typing.Union[T, str]:
        ...

    def __call__(
        self,
        key: str,
        cast: typing.Optional[typing.Callable] = None,
        default: typing.Any = undefined,
    ) -> typing.Any:
        return self.get(key, cast, default)

    def get(
        self,
        key: str,
        cast: typing.Optional[typing.Callable] = None,
        default: typing.Any = undefined,
    ) -> typing.Any:
        key = self.env_prefix + key
        if key in self.environ:
            value = self.environ[key]
            return self._perform_cast(key, value, cast)
        if key in self.file_values:
            value = self.file_values[key]
            return self._perform_cast(key, value, cast)
        if default is not undefined:
            return self._perform_cast(key, default, cast)
        raise KeyError(f"Config '{key}' is missing, and has no default.")

    def _read_file(self, file_name: typing.Union[str, Path]) -> typing.Dict[str, str]:
        file_values: typing.Dict[str, str] = {}
        with open(file_name) as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    file_values[key] = value
        return file_values

    def _perform_cast(
        self, key: str, value: typing.Any, cast: typing.Optional[typing.Callable] = None
    ) -> typing.Any:
        if cast is None or value is None:
            return value
        elif cast is bool and isinstance(value, str):
            mapping = {"true": True, "1": True, "false": False, "0": False}
            value = value.lower()
            if value not in mapping:
                raise ValueError(
                    f"Config '{key}' has value '{value}'. Not a valid bool."
                )
            return mapping[value]
        try:
            return cast(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"Config '{key}' has value '{value}'. Not a valid {cast.__name__}."
            )
