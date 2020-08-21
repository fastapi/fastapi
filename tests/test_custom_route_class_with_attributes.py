from typing import Callable

import pytest
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

app = FastAPI()


class CustomAPIRoute(APIRoute):
    x_type = "A"

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request.state.params = self.params
            response = await original_route_handler(request)
            return response

        return custom_route_handler


router = APIRouter(route_class=CustomAPIRoute, metadata=["params"])

params = ["Foo", "Bar"]


@router.get("/use_params", params=params)
def get_use_params(request: Request):
    return request.state.params


@router.get("/without_params")
def get_without_params(request: Request):
    return request.state.params


app.include_router(router)

client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint,status_code,expected",
    [
        ("/use_params", 200, params),
        ("/without_params", 200, None),
        # ("/unused_params", 200, None),
    ],
)
def test_valid_custom_api_route(endpoint, status_code, expected):
    response = client.get(endpoint)
    assert response.status_code == status_code
    assert response.json() == expected


def test_invalid_custom_api_route():
    router = APIRouter(route_class=CustomAPIRoute, metadata=["params"])

    with pytest.raises(AssertionError):

        @router.get("/unused_params", not_used_param=None)
        def get_unused_params():
            return None
