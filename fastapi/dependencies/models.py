from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union, cast

from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase
from typing_extensions import TypeAlias


@dataclass
class SecurityRequirement:
    security_scheme: SecurityBase
    scopes: Optional[Sequence[str]] = None


LifespanDependantCacheKey: TypeAlias = Union[
    Tuple[Callable[..., Any], Union[str, int]], Callable[..., Any]
]


@dataclass
class LifespanDependant:
    call: Callable[..., Any]
    caller: Callable[..., Any]
    dependencies: List["LifespanDependant"] = field(default_factory=list)
    name: Optional[str] = None
    use_cache: bool = True
    index: Optional[int] = None
    cache_key: LifespanDependantCacheKey = field(init=False)

    def __post_init__(self) -> None:
        if self.use_cache:
            self.cache_key = self.call
        elif self.name is not None:
            self.cache_key = (self.caller, self.name)
        else:
            assert self.index is not None, (
                "Lifespan dependency must have an associated name or index."
            )
            self.cache_key = (self.caller, self.index)


EndpointDependantCacheKey: TypeAlias = Tuple[
    Optional[Callable[..., Any]], Tuple[str, ...]
]


@dataclass
class EndpointDependant:
    endpoint_dependencies: List["EndpointDependant"] = field(default_factory=list)
    lifespan_dependencies: List[LifespanDependant] = field(default_factory=list)
    name: Optional[str] = None
    call: Optional[Callable[..., Any]] = None
    use_cache: bool = True
    index: Optional[int] = None
    cache_key: Tuple[Optional[Callable[..., Any]], Tuple[str, ...]] = field(init=False)
    path_params: List[ModelField] = field(default_factory=list)
    query_params: List[ModelField] = field(default_factory=list)
    header_params: List[ModelField] = field(default_factory=list)
    cookie_params: List[ModelField] = field(default_factory=list)
    body_params: List[ModelField] = field(default_factory=list)
    security_requirements: List[SecurityRequirement] = field(default_factory=list)
    request_param_name: Optional[str] = None
    websocket_param_name: Optional[str] = None
    http_connection_param_name: Optional[str] = None
    response_param_name: Optional[str] = None
    background_tasks_param_name: Optional[str] = None
    security_scopes_param_name: Optional[str] = None
    security_scopes: Optional[List[str]] = None
    path: Optional[str] = None

    def __post_init__(self) -> None:
        self.cache_key = (self.call, tuple(sorted(set(self.security_scopes or []))))

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
Dependant = EndpointDependant
CacheKey: TypeAlias = Union[EndpointDependantCacheKey, LifespanDependantCacheKey]
