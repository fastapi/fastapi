import inspect
import sys
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union, cast

from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase
from fastapi.types import (
    DependencyScope,
    EndpointDependencyCacheKey,
    EndpointDependencyScope,
    LifespanDependencyCacheKey,
    LifespanDependencyScope,
)
from typing_extensions import TypeAlias

if sys.version_info >= (3, 13):  # pragma: no cover
    from inspect import iscoroutinefunction
else:  # pragma: no cover
    from asyncio import iscoroutinefunction


@dataclass
class SecurityRequirement:
    security_scheme: SecurityBase
    scopes: Optional[Sequence[str]] = None


@dataclass
class _BaseDependant:
    call: Optional[Callable[..., Any]]
    scope: DependencyScope

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


@dataclass
class LifespanDependant(_BaseDependant):
    scope: LifespanDependencyScope
    caller: Callable[..., Any]
    call: Callable[..., Any]
    dependencies: List["LifespanDependant"] = field(default_factory=list)
    use_cache: bool = True
    name: Optional[str] = None
    index: Optional[int] = None

    @cached_property
    def cache_key(self) -> LifespanDependencyCacheKey:
        if self.use_cache:
            return self.call
        elif self.name is not None:
            return self.caller, self.name
        else:
            assert self.index is not None, (
                "Lifespan dependency must have an associated name or index."
            )
            return self.caller, self.index


@dataclass
class EndpointDependant(_BaseDependant):
    name: Optional[str] = None
    index: Optional[int] = None
    call: Optional[Callable[..., Any]] = None
    use_cache: bool = True
    scope: EndpointDependencyScope = None
    path_params: List[ModelField] = field(default_factory=list)
    query_params: List[ModelField] = field(default_factory=list)
    header_params: List[ModelField] = field(default_factory=list)
    cookie_params: List[ModelField] = field(default_factory=list)
    body_params: List[ModelField] = field(default_factory=list)
    endpoint_dependencies: List["EndpointDependant"] = field(default_factory=list)
    lifespan_dependencies: List[LifespanDependant] = field(default_factory=list)
    security_requirements: List[SecurityRequirement] = field(default_factory=list)
    request_param_name: Optional[str] = None
    websocket_param_name: Optional[str] = None
    http_connection_param_name: Optional[str] = None
    response_param_name: Optional[str] = None
    background_tasks_param_name: Optional[str] = None
    security_scopes_param_name: Optional[str] = None
    security_scopes: Optional[List[str]] = None
    path: Optional[str] = None

    @cached_property
    def cache_key(self) -> EndpointDependencyCacheKey:
        return (
            self.call,
            tuple(sorted(set(self.security_scopes or []))),
            self.computed_scope or "",
        )

    @cached_property
    def computed_scope(self) -> Union[str, None]:
        if self.scope:
            return self.scope
        if self.is_gen_callable or self.is_async_gen_callable:
            return "request"
        return None

    # Kept for backwards compatibility
    @property
    def dependencies(self) -> Tuple[Union["EndpointDependant", LifespanDependant], ...]:
        lifespan_dependencies = cast(
            List[Union[EndpointDependant, LifespanDependant]],
            self.lifespan_dependencies,
        )
        endpoint_dependencies = cast(
            List[Union[EndpointDependant, LifespanDependant]],
            self.endpoint_dependencies,
        )

        return tuple(lifespan_dependencies + endpoint_dependencies)


# Kept for backwards compatibility
Dependant: TypeAlias = EndpointDependant
