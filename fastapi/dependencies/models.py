from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Tuple

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
    request_param_names: List[str] = field(default_factory=list)
    websocket_param_names: List[str] = field(default_factory=list)
    http_connection_param_names: List[str] = field(default_factory=list)
    response_param_names: List[str] = field(default_factory=list)
    background_tasks_param_names: List[str] = field(default_factory=list)
    security_scopes_param_names: List[str] = field(default_factory=list)
    security_scopes: Optional[List[str]] = None
    use_cache: bool = True
    path: Optional[str] = None
    cache_key: Tuple[Optional[Callable[..., Any]], Tuple[str, ...]] = field(init=False)

    def __post_init__(self) -> None:
        self.cache_key = (self.call, tuple(sorted(set(self.security_scopes or []))))
