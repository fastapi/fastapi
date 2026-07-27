import inspect
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import lru_cache, partial
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


_UsesScopesCache = dict[int, tuple[Dependant, bool]]


class _CallIdentity:
    __slots__ = ("call",)

    def __init__(self, call: Callable[..., Any]) -> None:
        self.call = call

    def __hash__(self) -> int:
        return id(self.call)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _CallIdentity) and self.call is other.call


def _get_oauth_scopes(*, dependant: Dependant) -> list[str]:
    scopes = (
        dependant.parent_oauth_scopes.copy() if dependant.parent_oauth_scopes else []
    )
    # This doesn't use a set to preserve order, just in case
    for scope in dependant.own_oauth_scopes or []:
        if scope not in scopes:
            scopes.append(scope)
    return scopes


def _get_cache_key(
    *,
    dependant: Dependant,
    uses_scopes_cache: _UsesScopesCache | None = None,
) -> DependencyCacheKey:
    scopes_for_cache = (
        tuple(sorted(set(_get_oauth_scopes(dependant=dependant))))
        if _uses_scopes(dependant=dependant, cache=uses_scopes_cache)
        else ()
    )
    return (
        dependant.call,
        scopes_for_cache,
        _get_computed_scope(dependant=dependant) or "",
    )


def _uses_scopes(
    *, dependant: Dependant, cache: _UsesScopesCache | None = None
) -> bool:
    if cache is None:
        cache = {}
    cache_key = id(dependant)
    cached = cache.get(cache_key)
    if cached is not None and cached[0] is dependant:
        return cached[1]
    if dependant.own_oauth_scopes:
        result = True
    elif dependant.security_scopes_param_name is not None:
        result = True
    elif _is_security_scheme(dependant=dependant):
        result = True
    else:
        result = any(
            _uses_scopes(dependant=sub_dep, cache=cache)
            for sub_dep in dependant.dependencies
        )
    cache[cache_key] = (dependant, result)
    return result


def _is_security_scheme(*, dependant: Dependant) -> bool:
    if dependant.call is None:
        return False  # pragma: no cover
    unwrapped = _unwrapped_call(dependant.call)
    return isinstance(unwrapped, SecurityBase)


def _get_security_scheme(*, dependant: Dependant) -> SecurityBase:
    # Mainly to get the type of SecurityBase, but it's the same dependant.call
    unwrapped = _unwrapped_call(dependant.call)
    assert isinstance(unwrapped, SecurityBase)
    return unwrapped


def _get_security_dependencies(*, dependant: Dependant) -> list[Dependant]:
    return [dep for dep in dependant.dependencies if _is_security_scheme(dependant=dep)]


@lru_cache(maxsize=1024)
def _is_gen_callable_cached(call_identity: _CallIdentity) -> bool:
    call = call_identity.call
    if inspect.isgeneratorfunction(_impartial(call)) or inspect.isgeneratorfunction(
        _unwrapped_call(call)
    ):
        return True
    if inspect.isclass(_unwrapped_call(call)):
        return False
    dunder_call = getattr(_impartial(call), "__call__", None)  # noqa: B004
    if dunder_call is None:
        return False  # pragma: no cover
    if inspect.isgeneratorfunction(
        _impartial(dunder_call)
    ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_call)):
        return True
    dunder_unwrapped_call = getattr(_unwrapped_call(call), "__call__", None)  # noqa: B004
    if dunder_unwrapped_call is None:
        return False  # pragma: no cover
    return inspect.isgeneratorfunction(
        _impartial(dunder_unwrapped_call)
    ) or inspect.isgeneratorfunction(_unwrapped_call(dunder_unwrapped_call))


def _is_gen_callable(call: Callable[..., Any] | None) -> bool:
    if call is None:
        return False  # pragma: no cover
    return _is_gen_callable_cached(_CallIdentity(call))


@lru_cache(maxsize=1024)
def _is_async_gen_callable_cached(call_identity: _CallIdentity) -> bool:
    call = call_identity.call
    if inspect.isasyncgenfunction(_impartial(call)) or inspect.isasyncgenfunction(
        _unwrapped_call(call)
    ):
        return True
    if inspect.isclass(_unwrapped_call(call)):
        return False
    dunder_call = getattr(_impartial(call), "__call__", None)  # noqa: B004
    if dunder_call is None:
        return False  # pragma: no cover
    if inspect.isasyncgenfunction(
        _impartial(dunder_call)
    ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_call)):
        return True
    dunder_unwrapped_call = getattr(_unwrapped_call(call), "__call__", None)  # noqa: B004
    if dunder_unwrapped_call is None:
        return False  # pragma: no cover
    return inspect.isasyncgenfunction(
        _impartial(dunder_unwrapped_call)
    ) or inspect.isasyncgenfunction(_unwrapped_call(dunder_unwrapped_call))


def _is_async_gen_callable(call: Callable[..., Any] | None) -> bool:
    if call is None:
        return False  # pragma: no cover
    return _is_async_gen_callable_cached(_CallIdentity(call))


@lru_cache(maxsize=1024)
def _is_coroutine_callable_cached(call_identity: _CallIdentity) -> bool:
    call = call_identity.call
    if inspect.isroutine(_impartial(call)) and iscoroutinefunction(_impartial(call)):
        return True
    if inspect.isroutine(_unwrapped_call(call)) and iscoroutinefunction(
        _unwrapped_call(call)
    ):
        return True
    if inspect.isclass(_unwrapped_call(call)):
        return False
    dunder_call = getattr(_impartial(call), "__call__", None)  # noqa: B004
    if dunder_call is None:
        return False  # pragma: no cover
    if iscoroutinefunction(_impartial(dunder_call)) or iscoroutinefunction(
        _unwrapped_call(dunder_call)
    ):
        return True
    dunder_unwrapped_call = getattr(_unwrapped_call(call), "__call__", None)  # noqa: B004
    if dunder_unwrapped_call is None:
        return False  # pragma: no cover
    return iscoroutinefunction(
        _impartial(dunder_unwrapped_call)
    ) or iscoroutinefunction(_unwrapped_call(dunder_unwrapped_call))


def _is_coroutine_callable(call: Callable[..., Any] | None) -> bool:
    if call is None:
        return False  # pragma: no cover
    return _is_coroutine_callable_cached(_CallIdentity(call))


def _get_computed_scope(*, dependant: Dependant) -> str | None:
    if dependant.scope:
        return dependant.scope
    if _is_gen_callable(dependant.call) or _is_async_gen_callable(dependant.call):
        return "request"
    return None
