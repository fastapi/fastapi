import inspect
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Literal, cast

from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase
from fastapi.types import DependencyCacheKey

if sys.version_info >= (3, 13):  # pragma: no cover
    from inspect import iscoroutinefunction
else:  # pragma: no cover
    from asyncio import iscoroutinefunction


def _unwrapped_call(call: Callable[..., Any] | None) -> Any:
    if call is None:
        return call  # pragma: no cover
    unwrapped = inspect.unwrap(cast(Callable[..., Any], _impartial(call)))
    return unwrapped


def _impartial(func: Callable[..., Any] | None) -> Callable[..., Any] | None:
    while isinstance(func, partial):
        func = func.func
    return func


@dataclass(slots=True)
class Dependant:
    path_params: list[ModelField] = field(default_factory=list)
    query_params: list[ModelField] = field(default_factory=list)
    header_params: list[ModelField] = field(default_factory=list)
    cookie_params: list[ModelField] = field(default_factory=list)
    body_params: list[ModelField] = field(default_factory=list)
    dependencies: list["Dependant"] = field(default_factory=list)
    name: str | None = None
    call: Callable[..., Any] | None = None
    request_param_name: str | None = None
    websocket_param_name: str | None = None
    http_connection_param_name: str | None = None
    response_param_name: str | None = None
    background_tasks_param_name: str | None = None
    security_scopes_param_name: str | None = None
    own_oauth_scopes: list[str] | None = None
    parent_oauth_scopes: list[str] | None = None
    use_cache: bool = True
    path: str | None = None
    scope: Literal["function", "request"] | None = None

    @property
    def _oauth_scopes(self) -> list[str]:
        scopes = self.parent_oauth_scopes.copy() if self.parent_oauth_scopes else []
        # This doesn't use a set to preserve order, just in case
        for scope in self.own_oauth_scopes or []:
            if scope not in scopes:
                scopes.append(scope)
        return scopes

    @property
    def _cache_key(self) -> DependencyCacheKey:
        scopes_for_cache = (
            tuple(sorted(set(self.oauth_scopes or []))) if self._uses_scopes else ()
        )
        return (
            self.call,
            scopes_for_cache,
            self.computed_scope or "",
        )

    @property
    def __uses_scopes(self) -> bool:
        if self.own_oauth_scopes:
            return True
        if self.security_scopes_param_name is not None:
            return True
        if self._is_security_scheme:
            return True
        for sub_dep in self.dependencies:
            if sub_dep._uses_scopes:
                return True
        return False

    @property
    def __is_security_scheme(self) -> bool:
        if self.call is None:
            return False  # pragma: no cover
        unwrapped = _unwrapped_call(self.call)
        return isinstance(unwrapped, SecurityBase)

    # Mainly to get the type of SecurityBase, but it's the same self.call
    @property
    def __security_scheme(self) -> SecurityBase:
        unwrapped = _unwrapped_call(self.call)
        assert isinstance(unwrapped, SecurityBase)
        return unwrapped

    @property
    def __security_dependencies(self) -> list["Dependant"]:
        security_deps = [dep for dep in self.dependencies if dep._is_security_scheme]
        return security_deps

    @property
    def _is_gen_callable(self) -> bool:
        if self.call is None:
            return False  # pragma: no cover
        if inspect.isgeneratorfunction(
            _impartial(self.call)
        ) or inspect.isgeneratorfunction(_unwrapped_call(self.call)):
            return True
        if inspect.isclass(_unwrapped_call(self.call)):
            return False
        dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
        if dunder_call is None:
            return False  # pragma: no cover
        if inspect.isgeneratorfunction(
            _impartial(dunder_call)
        ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_call)):
            return True
        dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
        if dunder_unwrapped_call is None:
            return False  # pragma: no cover
        if inspect.isgeneratorfunction(
            _impartial(dunder_unwrapped_call)
        ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_unwrapped_call)):
            return True
        return False

    @property
    def _is_async_gen_callable(self) -> bool:
        if self.call is None:
            return False  # pragma: no cover
        if inspect.isasyncgenfunction(
            _impartial(self.call)
        ) or inspect.isasyncgenfunction(_unwrapped_call(self.call)):
            return True
        if inspect.isclass(_unwrapped_call(self.call)):
            return False
        dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
        if dunder_call is None:
            return False  # pragma: no cover
        if inspect.isasyncgenfunction(
            _impartial(dunder_call)
        ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_call)):
            return True
        dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
        if dunder_unwrapped_call is None:
            return False  # pragma: no cover
        if inspect.isasyncgenfunction(
            _impartial(dunder_unwrapped_call)
        ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_unwrapped_call)):
            return True
        return False

    @property
    def _is_coroutine_callable(self) -> bool:
        if self.call is None:
            return False  # pragma: no cover
        if inspect.isroutine(_impartial(self.call)) and iscoroutinefunction(
            _impartial(self.call)
        ):
            return True
        if inspect.isroutine(_unwrapped_call(self.call)) and iscoroutinefunction(
            _unwrapped_call(self.call)
        ):
            return True
        if inspect.isclass(_unwrapped_call(self.call)):
            return False
        dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
        if dunder_call is None:
            return False  # pragma: no cover
        if iscoroutinefunction(_impartial(dunder_call)) or iscoroutinefunction(
            _unwrapped_call(dunder_call)
        ):
            return True
        dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
        if dunder_unwrapped_call is None:
            return False  # pragma: no cover
        if iscoroutinefunction(
            _impartial(dunder_unwrapped_call)
        ) or iscoroutinefunction(_unwrapped_call(dunder_unwrapped_call)):
            return True
        return False

    @property
    def _computed_scope(self) -> str | None:
        if self.scope:
            return self.scope
        if self.is_gen_callable or self.is_async_gen_callable:
            return "request"
        return None

    # Lazy cached fields
    _oauth_scopes_cache: list[str] | None = field(default=None, init=False, repr=False)
    _cache_key_cache: DependencyCacheKey | None = field(
        default=None, init=False, repr=False
    )
    _uses_scopes_cache: bool | None = field(default=None, init=False, repr=False)
    _is_security_scheme_cache: bool | None = field(default=None, init=False, repr=False)
    _security_scheme_cache: SecurityBase | None = field(
        default=None, init=False, repr=False
    )
    _security_dependencies_cache: list["Dependant"] | None = field(
        default=None, init=False, repr=False
    )
    _is_gen_callable_cache: bool | None = field(default=None, init=False, repr=False)
    _is_async_gen_callable_cache: bool | None = field(
        default=None, init=False, repr=False
    )
    _is_coroutine_callable_cache: bool | None = field(
        default=None, init=False, repr=False
    )
    _computed_scope_cache: str | None = field(default=None, init=False, repr=False)

    @property
    def oauth_scopes(self) -> list[str]:
        if self._oauth_scopes_cache is None:
            self._oauth_scopes_cache = self._oauth_scopes

        return self._oauth_scopes_cache

    @property
    def cache_key(self) -> DependencyCacheKey:
        if self._cache_key_cache is None:
            self._cache_key_cache = self._cache_key

        return self._cache_key_cache

    @property
    def _uses_scopes(self) -> bool:
        if self._uses_scopes_cache is None:
            self._uses_scopes_cache = self.__uses_scopes

        return self._uses_scopes_cache

    @property
    def _is_security_scheme(self) -> bool:
        if self._is_security_scheme_cache is None:
            self._is_security_scheme_cache = self.__is_security_scheme

        return self._is_security_scheme_cache

    @property
    def _security_scheme(self) -> SecurityBase:
        if self._security_scheme_cache is None:
            self._security_scheme_cache = self.__security_scheme

        return self._security_scheme_cache

    @property
    def _security_dependencies(self) -> list["Dependant"]:
        if self._security_dependencies_cache is None:
            self._security_dependencies_cache = self.__security_dependencies

        return self._security_dependencies_cache

    @property
    def is_gen_callable(self) -> bool:
        if self._is_gen_callable_cache is None:
            self._is_gen_callable_cache = self._is_gen_callable

        return self._is_gen_callable_cache

    @property
    def is_async_gen_callable(self) -> bool:
        if self._is_async_gen_callable_cache is None:
            self._is_async_gen_callable_cache = self._is_async_gen_callable

        return self._is_async_gen_callable_cache

    @property
    def is_coroutine_callable(self) -> bool:
        if self._is_coroutine_callable_cache is None:
            self._is_coroutine_callable_cache = self._is_coroutine_callable

        return self._is_coroutine_callable_cache

    @property
    def computed_scope(self) -> str | None:
        if self._computed_scope_cache is None:
            self._computed_scope_cache = self._computed_scope

        return self._computed_scope_cache
