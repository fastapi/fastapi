import inspect
import sys
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Union

from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase
from fastapi.types import DependencyCacheKey
from typing_extensions import Literal

if sys.version_info >= (3, 13):  # pragma: no cover
    from inspect import iscoroutinefunction
else:  # pragma: no cover
    from asyncio import iscoroutinefunction


@dataclass
class SecurityRequirement:
    security_scheme: SecurityBase
    scopes: Optional[Sequence[str]] = None


@dataclass
class Dependant:
    path_params: List[ModelField] = field(default_factory=list)
    query_params: List[ModelField] = field(default_factory=list)
    header_params: List[ModelField] = field(default_factory=list)
    cookie_params: List[ModelField] = field(default_factory=list)
    body_params: List[ModelField] = field(default_factory=list)
    dependencies: List["Dependant"] = field(default_factory=list)
    security_requirements: List[SecurityRequirement] = field(default_factory=list)
    name: Optional[str] = None
    call: Optional[Callable[..., Any]] = None
    request_param_name: Optional[str] = None
    websocket_param_name: Optional[str] = None
    http_connection_param_name: Optional[str] = None
    response_param_name: Optional[str] = None
    background_tasks_param_name: Optional[str] = None
    security_scopes_param_name: Optional[str] = None
    own_oauth_scopes: Optional[List[str]] = None
    parent_oauth_scopes: Optional[List[str]] = None
    use_cache: bool = True
    path: Optional[str] = None
    scope: Union[Literal["function", "request"], None] = None

    @cached_property
    def oauth_scopes(self) -> List[str]:
        scopes = self.parent_oauth_scopes.copy() if self.parent_oauth_scopes else []
        # This doesn't use a set to preserve order, just in case
        for scope in self.own_oauth_scopes or []:
            if scope not in scopes:
                scopes.append(scope)
        return scopes

    @cached_property
    def cache_key(self) -> DependencyCacheKey:
        scopes_for_cache = (
            tuple(sorted(set(self.oauth_scopes or []))) if self._uses_scopes else ()
        )
        return (
            self.call,
            scopes_for_cache,
            self.computed_scope or "",
        )

    @cached_property
    def _uses_scopes(self) -> bool:
        if self.own_oauth_scopes:
            return True
        if self.security_scopes_param_name is not None:
            return True
        for sub_dep in self.dependencies:
            if sub_dep._uses_scopes:
                return True
        return False

    @cached_property
    def is_gen_callable(self) -> bool:
        if inspect.isgeneratorfunction(self.call):
            return True
        dunder_call = getattr(self.call, "__call__", None)  # noqa: B004
        return inspect.isgeneratorfunction(dunder_call)

    @cached_property
    def is_async_gen_callable(self) -> bool:
        if inspect.isasyncgenfunction(self.call):
            return True
        dunder_call = getattr(self.call, "__call__", None)  # noqa: B004
        return inspect.isasyncgenfunction(dunder_call)

    @cached_property
    def is_coroutine_callable(self) -> bool:
        if inspect.isroutine(self.call):
            return iscoroutinefunction(self.call)
        if inspect.isclass(self.call):
            return False
        dunder_call = getattr(self.call, "__call__", None)  # noqa: B004
        return iscoroutinefunction(dunder_call)

    @cached_property
    def computed_scope(self) -> Union[str, None]:
        if self.scope:
            return self.scope
        if self.is_gen_callable or self.is_async_gen_callable:
            return "request"
        return None
