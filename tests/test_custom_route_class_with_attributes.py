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


router = APIRouter(route_class=CustomAPIRoute)

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
