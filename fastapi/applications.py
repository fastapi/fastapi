from typing import Any, Callable, Dict, List, Optional, Type

from fastapi import routing
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import AdditionalResponse, AdditionalResponseDescription
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.exceptions import ExceptionMiddleware, HTTPException
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute


async def http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(
            {"detail": exc.detail}, status_code=exc.status_code, headers=headers
        )
    else:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


class FastAPI(Starlette):
    def __init__(
        self,
        debug: bool = False,
        routes: List[BaseRoute] = None,
        template_directory: str = None,
        title: str = "Fast API",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_prefix: str = "",
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        **extra: Dict[str, Any],
    ) -> None:
        self._debug = debug
        self.router: routing.APIRouter = routing.APIRouter(routes)
        self.exception_middleware = ExceptionMiddleware(self.router, debug=debug)
        self.error_middleware = ServerErrorMiddleware(
            self.exception_middleware, debug=debug
        )

        self.title = title
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.openapi_prefix = openapi_prefix.rstrip("/")
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.extra = extra

        self.openapi_version = "3.0.2"

        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"

        if self.docs_url or self.redoc_url:
            assert self.openapi_url, "The openapi_url is required for the docs"
        self.openapi_schema: Optional[Dict[str, Any]] = None
        self.setup()

    def openapi(self) -> Dict:
        if not self.openapi_schema:
            self.openapi_schema = get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                description=self.description,
                routes=self.routes,
                openapi_prefix=self.openapi_prefix,
            )
        return self.openapi_schema

    def setup(self) -> None:
        if self.openapi_url:
            self.add_route(
                self.openapi_url,
                lambda req: JSONResponse(self.openapi()),
                include_in_schema=False,
            )
        if self.openapi_url and self.docs_url:
            self.add_route(
                self.docs_url,
                lambda r: get_swagger_ui_html(
                    openapi_url=self.openapi_prefix + self.openapi_url,
                    title=self.title + " - Swagger UI",
                ),
                include_in_schema=False,
            )
        if self.openapi_url and self.redoc_url:
            self.add_route(
                self.redoc_url,
                lambda r: get_redoc_html(
                    openapi_url=self.openapi_prefix + self.openapi_url,
                    title=self.title + " - ReDoc",
                ),
                include_in_schema=False,
            )
        self.add_exception_handler(HTTPException, http_exception)

    def add_api_route(
            self,
            path: str,
            endpoint: Callable,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            methods: List[str] = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> None:
        self.router.add_api_route(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def api_route(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            methods: List[str] = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.router.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags or [],
                summary=summary,
                description=description,
                response_description=response_description,
                additional_responses=additional_responses,
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                include_in_schema=include_in_schema,
                content_type=content_type,
                name=name,
            )
            return func

        return decorator

    def include_router(
            self,
            router: routing.APIRouter,
            *,
            prefix: str = "",
            tags: List[str] = None,
            additional_responses: AdditionalResponse = [],
    ) -> None:
        self.router.include_router(router, prefix=prefix, tags=tags, additional_responses=additional_responses,)

    def get(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.get(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def put(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.put(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def post(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.post(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def delete(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.delete(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def options(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.options(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def head(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.head(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def patch(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.patch(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )

    def trace(
            self,
            path: str,
            *,
            response_model: Type[BaseModel] = None,
            status_code: int = 200,
            tags: List[str] = None,
            summary: str = None,
            description: str = None,
            response_description: str = "Successful Response",
            additional_responses: AdditionalResponse = [],
            deprecated: bool = None,
            operation_id: str = None,
            include_in_schema: bool = True,
            content_type: Type[Response] = JSONResponse,
            name: str = None,
    ) -> Callable:
        return self.router.trace(
            path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            additional_responses=additional_responses,
            deprecated=deprecated,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
            name=name,
        )
