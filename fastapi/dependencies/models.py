from typing import Callable, List, Optional, Sequence

from fastapi.security.base import SecurityBase
from pydantic.fields import ModelField

param_supported_types = (str, int, float, bool)


class SecurityRequirement:
    def __init__(
        self, security_scheme: SecurityBase, scopes: Optional[Sequence[str]] = None
    ):
        self.security_scheme = security_scheme
        self.scopes = scopes


class Dependant:
    def __init__(
        self,
        *,
        path_params: Optional[List[ModelField]] = None,
        query_params: Optional[List[ModelField]] = None,
        header_params: Optional[List[ModelField]] = None,
        cookie_params: Optional[List[ModelField]] = None,
        body_params: Optional[List[ModelField]] = None,
        dependencies: Optional[List["Dependant"]] = None,
        security_schemes: Optional[List[SecurityRequirement]] = None,
        name: Optional[str] = None,
        call: Optional[Callable] = None,
        request_param_name: Optional[str] = None,
        websocket_param_name: Optional[str] = None,
        http_connection_param_name: Optional[str] = None,
        response_param_name: Optional[str] = None,
        background_tasks_param_name: Optional[str] = None,
        security_scopes_param_name: Optional[str] = None,
        security_scopes: Optional[List[str]] = None,
        use_cache: bool = True,
        path: Optional[str] = None,
    ) -> None:
        self.path_params = path_params or []
        self.query_params = query_params or []
        self.header_params = header_params or []
        self.cookie_params = cookie_params or []
        self.body_params = body_params or []
        self.dependencies = dependencies or []
        self.security_requirements = security_schemes or []
        self.request_param_name = request_param_name
        self.websocket_param_name = websocket_param_name
        self.http_connection_param_name = http_connection_param_name
        self.response_param_name = response_param_name
        self.background_tasks_param_name = background_tasks_param_name
        self.security_scopes = security_scopes
        self.security_scopes_param_name = security_scopes_param_name
        self.name = name
        self.call = call
        self.use_cache = use_cache
        # Store the path to be able to re-generate a dependable from it in overrides
        self.path = path
        # Save the cache key at creation to optimize performance
        self.cache_key = (self.call, tuple(sorted(set(self.security_scopes or []))))
