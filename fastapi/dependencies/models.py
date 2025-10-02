from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Set, Tuple

from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase


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
    request_param_names: Set[str] = field(default_factory=set)
    websocket_param_names: Set[str] = field(default_factory=set)
    http_connection_param_names: Set[str] = field(default_factory=set)
    response_param_names: Set[str] = field(default_factory=set)
    background_tasks_param_names: Set[str] = field(default_factory=set)
    security_scopes_param_names: Set[str] = field(default_factory=set)
    security_scopes: Optional[List[str]] = None
    use_cache: bool = True
    path: Optional[str] = None
    cache_key: Tuple[Optional[Callable[..., Any]], Tuple[str, ...]] = field(init=False)

    def __post_init__(self) -> None:
        self.cache_key = (self.call, tuple(sorted(set(self.security_scopes or []))))
