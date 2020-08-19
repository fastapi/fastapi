from typing import Callable, Iterable, Optional

import pytest
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

app = FastAPI()


class APIRouteWithoutConstructor(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.params = self.params
            response = await original_route_handler(request)
            return response

        return custom_route_handler


class APIRouteWithConstructor(APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        params: Optional[Iterable[str]] = None,
        **kwargs
    ) -> None:
        super().__init__(path, endpoint, **kwargs)
        self.params = params

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.params = self.params
            response = await original_route_handler(request)
            return response

        return custom_route_handler


router_with_constructor = APIRouter(route_class=APIRouteWithConstructor)
router_without_constructor = APIRouter(route_class=APIRouteWithoutConstructor)


params = ["Foo", "Bar"]


@router_without_constructor.get("/use_params", params=params)
@router_with_constructor.get("/use_params", params=params)
def get_use_params(request: Request):
    return request.state.params


@router_without_constructor.get("/without_params")
@router_with_constructor.get("/without_params")
def get_without_params(request: Request):
    return request.state.params


@router_without_constructor.get("/unused_params", not_used_params=None)
@router_with_constructor.get("/unused_params", not_used_param=None)
def get_unused_params():
    return None


app.include_router(router_with_constructor, prefix="/with")
app.include_router(router_without_constructor, prefix="/without")

client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint,status_code,expected",
    [
        ("/with/use_params", 200, params),
        ("/with/without_params", 200, None),
        ("/with/unused_params", 200, None),
        ("/without/use_params", 200, params),
    ],
)
def test_valid_custom_api_route(endpoint, status_code, expected):
    response = client.get(endpoint)
    assert response.status_code == status_code
    assert response.json() == expected


@pytest.mark.parametrize(
    "endpoint", ["/without/without_params", "/without/unused_params"],
)
def test_invalid_custom_api_route(endpoint):
    with pytest.raises(AttributeError):
        client.get(endpoint)
