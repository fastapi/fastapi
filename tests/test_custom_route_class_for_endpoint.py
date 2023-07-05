from typing import Callable
from urllib.request import Request

import pytest
from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

app = FastAPI()
router = APIRouter()


class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            if "test_header" not in request.headers:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            return await original_route_handler(request)

        return custom_route_handler


@router.get("/a")
def get_a():
    return {"msg": "A"}


@router.get("/b", route_class_override=CustomRoute)
def get_b():
    return {"msg": "B"}


app.include_router(router=router, prefix="")


client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,headers",
    [
        ("/a", 200, {"test_header": "value"}),
        ("/a", 200, None),
        ("/b", 200, {"test_header": "value"}),
        ("/b", 400, None),
    ],
    ids=[
        "/a with test_header header",
        "/a without test_header headers",
        "/b with test_header headers",
        "/b without test_header headers",
    ],
)
def test_get_path(path, expected_status, headers):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
