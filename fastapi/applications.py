from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import routing
from fastapi.concurrency import AsyncExitStack
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.params import Depends
from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import Receive, Scope, Send


class FastAPI(Starlette):
    """Creates an application instance.

    Attributes:
        default_response_class (Type[Response]): [description]
        dependency_overrides (Dict[Callable, Callable]): [description]
        description (str): [description]
        docs_url (Optional[str]): [description]
        exception_handlers (Dict[Union[int, Type[Exception]], Callable]): A dictionary
            mapping either integer status codes, or exception class types onto callables
            which handle the exceptions. Exception handler callables should be of the
            form `handler(request, exc) -> response` and may be be either standard
            functions, or async functions.
        extra (Any): [description]
        middleware_stack (ASGIApp): [description]
        openapi_url (str): [description]
        openapi_tags (Optional[List[Dict[str, Any]]]): [description]
        openapi_version (str): [description]
        openapi_schema (Optional[Dict[str, Any]]) [description]
        redoc_url (Optional[str]): [description]
        root_path (str): [description]
        root_path_in_servers (bool): [description]
        router (routing.APIRouter): [description]
        servers (List[Dict[str, Union[str, Any]]]): [description]
        state (State): Store arbitrary state.
        swagger_ui_oauth2_redirect_url (Optional[str]): [description]
        swagger_ui_init_oauth (Optional[dict]): [description]
        title (str): [description]
        user_middleware (List[Middleware]): [description]
        version (str): [description]
    """

    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[BaseRoute]] = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        default_response_class: Type[Response] = JSONResponse,
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[dict] = None,
        middleware: Optional[Sequence[Middleware]] = None,
        exception_handlers: Optional[
            Dict[Union[int, Type[Exception]], Callable]
        ] = None,
        on_startup: Optional[Sequence[Callable]] = None,
        on_shutdown: Optional[Sequence[Callable]] = None,
        openapi_prefix: str = "",
        root_path: str = "",
        root_path_in_servers: bool = True,
        **extra: Any,
    ) -> None:
        self.default_response_class = default_response_class
        self._debug = debug
        self.state = State()
        self.router: routing.APIRouter = routing.APIRouter(
            routes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )
        self.exception_handlers = (
            {} if exception_handlers is None else dict(exception_handlers)
        )

        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack = self.build_middleware_stack()

        self.title = title
        self.description = description
        self.version = version
        self.servers = servers or []
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        # TODO: remove when discarding the openapi_prefix parameter
        if openapi_prefix:
            logger.warning(
                '"openapi_prefix" has been deprecated in favor of "root_path", which '
                "follows more closely the ASGI standard, is simpler, and more "
                "automatic. Check the docs at "
                "https://fastapi.tiangolo.com/advanced/sub-applications/"
            )
        self.root_path = root_path or openapi_prefix
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.extra = extra
        self.dependency_overrides: Dict[Callable, Callable] = {}

        self.openapi_version = "3.0.2"

        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        self.openapi_schema: Optional[Dict[str, Any]] = None
        self.setup()

    def openapi(self) -> Dict:
        """[summary]

        Returns:
            Dict: [description]
        """
        if not self.openapi_schema:
            self.openapi_schema = get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                description=self.description,
                routes=self.routes,
                tags=self.openapi_tags,
                servers=self.servers,
            )
        return self.openapi_schema

    def setup(self) -> None:
        """[summary]"""
        if self.openapi_url:
            urls = (server_data.get("url") for server_data in self.servers)
            server_urls = {url for url in urls if url}

            async def openapi(req: Request) -> JSONResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                if root_path not in server_urls:
                    if root_path and self.root_path_in_servers:
                        self.servers.insert(0, {"url": root_path})
                        server_urls.add(root_path)
                return JSONResponse(self.openapi())

            self.add_route(self.openapi_url, openapi, include_in_schema=False)
        if self.openapi_url and self.docs_url:

            async def swagger_ui_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                oauth2_redirect_url = self.swagger_ui_oauth2_redirect_url
                if oauth2_redirect_url:
                    oauth2_redirect_url = root_path + oauth2_redirect_url
                return get_swagger_ui_html(
                    openapi_url=openapi_url,
                    title=self.title + " - Swagger UI",
                    oauth2_redirect_url=oauth2_redirect_url,
                    init_oauth=self.swagger_ui_init_oauth,
                )

            self.add_route(self.docs_url, swagger_ui_html, include_in_schema=False)

            if self.swagger_ui_oauth2_redirect_url:

                async def swagger_ui_redirect(req: Request) -> HTMLResponse:
                    return get_swagger_ui_oauth2_redirect_html()

                self.add_route(
                    self.swagger_ui_oauth2_redirect_url,
                    swagger_ui_redirect,
                    include_in_schema=False,
                )
        if self.openapi_url and self.redoc_url:

            async def redoc_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                return get_redoc_html(
                    openapi_url=openapi_url, title=self.title + " - ReDoc"
                )

            self.add_route(self.redoc_url, redoc_html, include_in_schema=False)
        self.add_exception_handler(HTTPException, http_exception_handler)
        self.add_exception_handler(
            RequestValidationError, request_validation_exception_handler
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.root_path:
            scope["root_path"] = self.root_path
        if AsyncExitStack:
            async with AsyncExitStack() as stack:
                scope["fastapi_astack"] = stack
                await super().__call__(scope, receive, send)
        else:
            await super().__call__(scope, receive, send)  # pragma: no cover

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[List[str]] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
    ) -> None:
        """[summary]

        Args:
            path (str): [description]
            endpoint (Callable): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            methods (Optional[List[str]], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
        """
        self.router.add_api_route(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
        )

    def api_route(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[List[str]] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            methods (Optional[List[str]], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """

        def decorator(func: Callable) -> Callable:
            self.router.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags or [],
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses or {},
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=response_model_exclude_unset,
                response_model_exclude_defaults=response_model_exclude_defaults,
                response_model_exclude_none=response_model_exclude_none,
                include_in_schema=include_in_schema,
                response_class=response_class or self.default_response_class,
                name=name,
            )
            return func

        return decorator

    def add_api_websocket_route(
        self, path: str, endpoint: Callable, name: Optional[str] = None
    ) -> None:
        """[summary]

        Args:
            path (str): [description]
            endpoint (Callable): [description]
            name (Optional[str], optional): [description]. Defaults to None.
        """
        self.router.add_api_websocket_route(path, endpoint, name=name)

    def websocket(self, path: str, name: Optional[str] = None) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            name (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """

        def decorator(func: Callable) -> Callable:
            self.add_api_websocket_route(path, func, name=name)
            return func

        return decorator

    def include_router(
        self,
        router: routing.APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        default_response_class: Optional[Type[Response]] = None,
    ) -> None:
        """[summary]

        Args:
            router (routing.APIRouter): [description]
            prefix (str, optional): [description]. Defaults to "".
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            default_response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
        """
        self.router.include_router(
            router,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=responses or {},
            default_response_class=default_response_class
            or self.default_response_class,
        )

    def get(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.get(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def put(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.put(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def post(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.post(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def delete(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.delete(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            operation_id=operation_id,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def options(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.options(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def head(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.head(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def patch(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.patch(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def trace(
        self,
        path: str,
        *,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[routing.APIRoute]] = None,
    ) -> Callable:
        """[summary]

        Args:
            path (str): [description]
            response_model (Optional[Type[Any]], optional): [description]. Defaults to None.
            status_code (int, optional): [description]. Defaults to 200.
            tags (Optional[List[str]], optional): [description]. Defaults to None.
            dependencies (Optional[Sequence[Depends]], optional): [description]. Defaults to None.
            summary (Optional[str], optional): [description]. Defaults to None.
            description (Optional[str], optional): [description]. Defaults to None.
            response_description (str, optional): [description]. Defaults to "Successful Response".
            responses (Optional[Dict[Union[int, str], Dict[str, Any]]], optional): [description]. Defaults to None.
            deprecated (Optional[bool], optional): [description]. Defaults to None.
            operation_id (Optional[str], optional): [description]. Defaults to None.
            response_model_include (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_exclude (Optional[Union[SetIntStr, DictIntStrAny]], optional): [description]. Defaults to None.
            response_model_by_alias (bool, optional): [description]. Defaults to True.
            response_model_exclude_unset (bool, optional): [description]. Defaults to False.
            response_model_exclude_defaults (bool, optional): [description]. Defaults to False.
            response_model_exclude_none (bool, optional): [description]. Defaults to False.
            include_in_schema (bool, optional): [description]. Defaults to True.
            response_class (Optional[Type[Response]], optional): [description]. Defaults to None.
            name (Optional[str], optional): [description]. Defaults to None.
            callbacks (Optional[List[routing.APIRoute]], optional): [description]. Defaults to None.

        Returns:
            Callable: [description]
        """
        return self.router.trace(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )
