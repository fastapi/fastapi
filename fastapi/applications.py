from typing import Any, Callable, Dict, List, Type

from starlette.applications import Starlette
from starlette.exceptions import ExceptionMiddleware, HTTPException
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.lifespan import LifespanMiddleware
from starlette.responses import JSONResponse


from fastapi import routing
from fastapi.openapi.utils import get_swagger_ui_html, get_openapi, get_redoc_html


async def http_exception(request, exc: HTTPException):
    print(exc)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


class FastAPI(Starlette):
    def __init__(
        self,
        debug: bool = False,
        template_directory: str = None,
        title: str = "Fast API",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: str = "/openapi.json",
        swagger_ui_url: str = "/docs",
        redoc_url: str = "/redoc",
        **extra: Dict[str, Any],
    ) -> None:
        self._debug = debug
        self.router = routing.APIRouter()
        self.exception_middleware = ExceptionMiddleware(self.router, debug=debug)
        self.error_middleware = ServerErrorMiddleware(
            self.exception_middleware, debug=debug
        )
        self.lifespan_middleware = LifespanMiddleware(self.error_middleware)
        self.schema_generator = None
        self.template_env = self.load_template_env(template_directory)

        self.title = title
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.swagger_ui_url = swagger_ui_url
        self.redoc_url = redoc_url
        self.extra = extra

        self.openapi_version = "3.0.2"

        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"

        if self.swagger_ui_url or self.redoc_url:
            assert self.openapi_url, "The openapi_url is required for the docs"
        self.setup()

    def setup(self):
        if self.openapi_url:
            self.add_route(
                self.openapi_url,
                lambda req: JSONResponse(
                    get_openapi(
                        title=self.title,
                        version=self.version,
                        openapi_version=self.openapi_version,
                        description=self.description,
                        routes=self.routes,
                    )
                ),
                include_in_schema=False,
            )
        if self.swagger_ui_url:
            self.add_route(
                self.swagger_ui_url,
                lambda r: get_swagger_ui_html(openapi_url=self.openapi_url, title=self.title + " - Swagger UI"),
                include_in_schema=False,
            )
        if self.redoc_url:
            self.add_route(
                self.redoc_url,
                lambda r: get_redoc_html(openapi_url=self.openapi_url, title=self.title + " - ReDoc"),
                include_in_schema=False,
            )
        self.add_exception_handler(HTTPException, http_exception)

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> None:
        self.router.add_api_route(
            path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def api_route(
        self,
        path: str,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.router.add_api_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
                tags=tags or [],
                summary=summary,
                description=description,
                operation_id=operation_id,
                deprecated=deprecated,
                response_type=response_type,
                response_description=response_description,
                response_code=response_code,
                response_wrapper=response_wrapper,
            )
            return func

        return decorator

    def get(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.get(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def put(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.put(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def post(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.post(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def delete(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.delete(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def options(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.options(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def head(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.head(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def patch(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.patch(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def trace(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.trace(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )
