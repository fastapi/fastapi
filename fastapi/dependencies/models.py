from typing import Callable, List, Sequence

from fastapi.security.base import SecurityBase

try:
    from pydantic.fields import ModelField
except ImportError:  # pragma: nocover
    # TODO: remove when removing support for Pydantic < 1.0.0
    from pydantic.fields import Field as ModelField  # type: ignore

param_supported_types = (str, int, float, bool)


class SecurityRequirement:
    def __init__(self, security_scheme: SecurityBase, scopes: Sequence[str] = None):
        self.security_scheme = security_scheme
        self.scopes = scopes


class Dependant:
    def __init__(
        self,
        *,
        path_params: List[ModelField] = None,
        query_params: List[ModelField] = None,
        header_params: List[ModelField] = None,
        cookie_params: List[ModelField] = None,
        body_params: List[ModelField] = None,
        dependencies: List["Dependant"] = None,
        security_schemes: List[SecurityRequirement] = None,
        name: str = None,
        call: Callable = None,
        request_param_name: str = None,
        websocket_param_name: str = None,
        response_param_name: str = None,
        background_tasks_param_name: str = None,
        security_scopes_param_name: str = None,
        security_scopes: List[str] = None,
        use_cache: bool = True,
        path: str = None,
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
