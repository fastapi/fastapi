from typing import Callable, Iterable, Optional

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

app = FastAPI()


class CustomAPIRoute(APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        permissions: Optional[Iterable[str]] = None,
        **kwargs
    ) -> None:
        super().__init__(path, endpoint, **kwargs)
        self.permissions = permissions

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.permissions = self.permissions
            response = await original_route_handler(request)
            return response

        return custom_route_handler


class CustomAPIRouter(APIRouter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route_class = CustomAPIRoute

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        permissions: Optional[Iterable[str]] = None,
        **kwargs
    ) -> None:
        route = self.route_class(
            path=path, endpoint=endpoint, permissions=permissions, **kwargs
        )
        print("permissions" in dir(route))
        self.routes.append(route)

    def api_route(
        self, path: str, *, permissions: Optional[Iterable[str]] = None, **kwargs
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_api_route(path, func, permissions=permissions, **kwargs)
            return func

        return decorator

    def get(
        self, path: str, *, permissions: Optional[Iterable[str]] = None, **kwargs
    ) -> Callable:
        return self.api_route(path, permissions=permissions, **kwargs)


router = CustomAPIRouter()

_permissions = ["Foo", "Bar"]


@router.get("/", permissions=_permissions)
def home(request: Request):
    return request.state.permissions


app.include_router(router)

client = TestClient(app)


def test_route_class():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == _permissions
