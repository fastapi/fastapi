import inspect
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property, partial
from typing import Any, Literal

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
    unwrapped = inspect.unwrap(_impartial(call))
    return unwrapped


def _impartial(func: Callable[..., Any]) -> Callable[..., Any]:
    while isinstance(func, partial):
        func = func.func
    return func


@dataclass
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
    # Lazy cached fields
    _oauth_scopes_cache: list[str] = field(default=None, init=False, repr=False)
    _cache_key_cache: DependencyCacheKey = field(default=None, init=False, repr=False)
    _uses_scopes_cache: bool = field(default=None, init=False, repr=False)
    _is_security_scheme_cache: bool = field(default=None, init=False, repr=False)
    _security_scheme_cache: SecurityBase = field(default=None, init=False, repr=False)
    _security_dependencies_cache: list["Dependant"] = field(default=None, init=False, repr=False)
    _is_gen_callable_cache: bool = field(default=None, init=False, repr=False)
    _is_async_gen_callable_cache: bool = field(default=None, init=False, repr=False)
    _is_coroutine_callable_cache: bool = field(default=None, init=False, repr=False)

    @property
    def oauth_scopes(self) -> list[str]:
        if self._oauth_scopes_cache is None:
            scopes = self.parent_oauth_scopes.copy() if self.parent_oauth_scopes else []
            # This doesn't use a set to preserve order, just in case
            for scope in self.own_oauth_scopes or []:
                if scope not in scopes:
                    scopes.append(scope)
            self._oauth_scopes_cache = scopes

        return self._oauth_scopes_cache

    @property
    def cache_key(self) -> DependencyCacheKey:
        if self._cache_key_cache is None:
            scopes_for_cache = (
                tuple(sorted(set(self.oauth_scopes or []))) if self._uses_scopes else ()
            )
            self._cache_key_cache = (
                self.call,
                scopes_for_cache,
                self.computed_scope or "",
            )

        return self._cache_key_cache

    @property
    def _uses_scopes(self) -> bool:
        if self._uses_scopes_cache is None:
            if self.own_oauth_scopes:
                self._uses_scopes_cache = True
            elif self.security_scopes_param_name is not None:
                self._uses_scopes_cache = True
            elif self._is_security_scheme:
                self._uses_scopes_cache = True

            for sub_dep in self.dependencies:
                if sub_dep._uses_scopes:
                    self._uses_scopes_cache = True
                    break

            if self._uses_scopes_cache is None:
                self._uses_scopes_cache = False

        return self._uses_scopes_cache

    @property
    def _is_security_scheme(self) -> bool:
        if self._is_security_scheme_cache is None:
            if self.call is None:
                self._is_security_scheme_cache = False  # pragma: no cover
            else:
                unwrapped = _unwrapped_call(self.call)
                self._is_security_scheme_cache = isinstance(unwrapped, SecurityBase)

        return self._is_security_scheme_cache

    # Mainly to get the type of SecurityBase, but it's the same self.call
    @property
    def _security_scheme(self) -> SecurityBase:
        if self._security_scheme_cache is None:
            unwrapped = _unwrapped_call(self.call)
            assert isinstance(unwrapped, SecurityBase)
            self._security_scheme_cache = unwrapped

        return self._security_scheme_cache

    @property
    def _security_dependencies(self) -> list["Dependant"]:
        if self._security_dependencies_cache is None:
            security_deps = [dep for dep in self.dependencies if dep._is_security_scheme]
            self._security_dependencies_cache = security_deps

        return self._security_dependencies_cache

    @property
    def is_gen_callable(self) -> bool:
        if self._is_gen_callable_cache is None:
            if self.call is None:
                self._is_gen_callable_cache = False  # pragma: no cover
            elif inspect.isgeneratorfunction(
                _impartial(self.call)
            ) or inspect.isgeneratorfunction(_unwrapped_call(self.call)):
                self._is_gen_callable_cache = True
            elif inspect.isclass(_unwrapped_call(self.call)):
                self._is_gen_callable_cache = False

            if self._is_gen_callable_cache is not None:
                return self._is_gen_callable_cache

            dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
            if dunder_call is None:
                self._is_gen_callable_cache = False  # pragma: no cover
            elif inspect.isgeneratorfunction(
                _impartial(dunder_call)
            ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_call)):
                self._is_gen_callable_cache = True

            if self._is_gen_callable_cache is not None:
                return self._is_gen_callable_cache

            dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
            if dunder_unwrapped_call is None:
                self._is_gen_callable_cache = False  # pragma: no cover
            if inspect.isgeneratorfunction(
                _impartial(dunder_unwrapped_call)
            ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_unwrapped_call)):
                self._is_gen_callable_cache = True
            else:
                self._is_gen_callable_cache = False

        return self._is_gen_callable_cache

    @property
    def is_async_gen_callable(self) -> bool:
        if self._is_async_gen_callable_cache is None:
            if self.call is None:
                self._is_async_gen_callable_cache = False  # pragma: no cover
            elif inspect.isasyncgenfunction(
                _impartial(self.call)
            ) or inspect.isasyncgenfunction(_unwrapped_call(self.call)):
                self._is_async_gen_callable_cache = True
            elif inspect.isclass(_unwrapped_call(self.call)):
                self._is_async_gen_callable_cache = False

            if self._is_async_gen_callable_cache is not None:
                return self._is_async_gen_callable_cache

            dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
            if dunder_call is None:
                self._is_async_gen_callable_cache = False  # pragma: no cover
            elif inspect.isasyncgenfunction(
                _impartial(dunder_call)
            ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_call)):
                self._is_async_gen_callable_cache = True

            if self._is_async_gen_callable_cache is not None:
                return self._is_async_gen_callable_cache

            dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
            if dunder_unwrapped_call is None:
                self._is_async_gen_callable_cache = False  # pragma: no cover
            elif inspect.isasyncgenfunction(
                _impartial(dunder_unwrapped_call)
            ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_unwrapped_call)):
                self._is_async_gen_callable_cache = True
            else:
                self._is_async_gen_callable_cache = False

        return self._is_async_gen_callable_cache

    @property
    def is_coroutine_callable(self) -> bool:
        if self._is_coroutine_callable_cache is None:
            if self.call is None:
                self._is_coroutine_callable_cache = False  # pragma: no cover
            elif inspect.isroutine(_impartial(self.call)) and iscoroutinefunction(
                _impartial(self.call)
            ):
                self._is_coroutine_callable_cache = True
            elif inspect.isroutine(_unwrapped_call(self.call)) and iscoroutinefunction(
                _unwrapped_call(self.call)
            ):
                self._is_coroutine_callable_cache = True
            elif inspect.isclass(_unwrapped_call(self.call)):
                self._is_coroutine_callable_cache = False

            if self._is_coroutine_callable_cache is not None:
                return self._is_coroutine_callable_cache

            dunder_call = getattr(_impartial(self.call), "__call__", None)  # noqa: B004
            if dunder_call is None:
                self._is_coroutine_callable_cache = False  # pragma: no cover
            elif iscoroutinefunction(_impartial(dunder_call)) or iscoroutinefunction(
                _unwrapped_call(dunder_call)
            ):
                self._is_coroutine_callable_cache = True

            if self._is_coroutine_callable_cache is not None:
                return self._is_coroutine_callable_cache

            dunder_unwrapped_call = getattr(_unwrapped_call(self.call), "__call__", None)  # noqa: B004
            if dunder_unwrapped_call is None:
                self._is_coroutine_callable_cache = False  # pragma: no cover
            elif iscoroutinefunction(
                _impartial(dunder_unwrapped_call)
            ) or iscoroutinefunction(_unwrapped_call(dunder_unwrapped_call)):
                self._is_coroutine_callable_cache = True
            else:
                self._is_coroutine_callable_cache = False
        
        return self._is_coroutine_callable_cache

    @cached_property
    def computed_scope(self) -> str | None:
        if self.scope:
            return self.scope
        if self.is_gen_callable or self.is_async_gen_callable:
            return "request"
        return None
