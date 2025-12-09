import time
from typing import Any, Awaitable, Callable, List, Optional, Set, Union

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute


async def health_check(request: Request):
    """
    Health check endpoint
    """
    return Response(content="OK", status_code=200)


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"{self.name} route duration: {duration}")
            print(f"{self.name} route response: {response}")
            print(f"{self.name} route response headers: {response.headers}")
            return response

        return custom_route_handler


class AppRouter(APIRouter):
    def __init__(self, prefix="", name="Global", tags: list = None, **kwargs):
        self.name = name
        tags = tags or []
        tags.insert(0, name)
        super().__init__(prefix=prefix, tags=tags, **kwargs)
        self._parent: Optional[AppRouter] = None
        self._add_health_check()

    @property
    def request_name_prefix(self):
        return (
            f"{self._parent.request_name_prefix}.{self.name}"
            if self._parent
            else self.name
        )

    def _add_health_check(self):
        """
        Adding default health check route for all new routers
        """
        self.add_api_route(
            "/healthz", endpoint=health_check, methods=["GET"], name="health-check"
        )

    def include_router(self, router: "AppRouter", **kwargs):
        """
        Include another router into this router.
        """
        router._parent = self
        super().include_router(router, **kwargs)

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        methods: Union[Set[str], List[str]],  # noqa
        name: str,
        **kwargs,
    ):
        name = f"{self.request_name_prefix}.{name}"
        return super().add_api_route(
            path,
            endpoint,
            methods=methods,
            name=name,
            **kwargs,
        )

    def add_route(
        self,
        path: str,
        endpoint: Callable[[Request], Union[Awaitable[Response], Response]],
        methods: Union[List[str], None] = None,
        name: Union[str, None] = None,
        include_in_schema: bool = True,
    ) -> None:
        name = f"{self.request_name_prefix}.{name}"
        return super().add_route(
            path,
            endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )


app = FastAPI(route_class=TimedRoute, router_class=AppRouter)
model = AppRouter(prefix="/model", name="Model", route_class=TimedRoute)
item = AppRouter(prefix="/{model_id}/item", name="Item", route_class=TimedRoute)


async def create_model(request: Request):
    """
    Create a model
    """
    print("Model created")
    route: TimedRoute = request.scope["route"]
    router: AppRouter = request.scope["router"]
    return JSONResponse(
        {
            "route_class": route.__class__.__name__,
            "route_name": route.name,
            "router_class": router.__class__.__name__,
        },
        status_code=200,
    )


model.add_api_route(
    path="/create", endpoint=create_model, methods=["POST"], name="create-model"
)


async def create_item(request: Request):
    """
    Create an item
    """
    print("Item created")
    route: TimedRoute = request.scope["route"]
    router: AppRouter = request.scope["router"]
    return JSONResponse(
        {
            "route_class": route.__class__.__name__,
            "route_name": route.name,
            "router_class": router.__class__.__name__,
        },
        status_code=200,
    )


item.add_api_route(
    path="/create", endpoint=create_item, methods=["POST"], name="create-item"
)

model.include_router(item)
app.include_router(model)
