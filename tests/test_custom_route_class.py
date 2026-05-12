from collections.abc import Sequence
from enum import Enum
from typing import Any, Callable

import pytest
from fastapi import APIRouter, FastAPI, params
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from fastapi.types import IncEx
from fastapi.utils import generate_unique_id
from inline_snapshot import snapshot
from starlette.routing import BaseRoute, Route

app = FastAPI()


class APIRouteA(APIRoute):
    x_type = "A"


class APIRouteB(APIRoute):
    x_type = "B"


class APIRouteC(APIRoute):
    x_type = "C"


router_a = APIRouter(route_class=APIRouteA)
router_b = APIRouter(route_class=APIRouteB)
router_c = APIRouter(route_class=APIRouteC)


@router_a.get("/")
def get_a():
    return {"msg": "A"}


@router_b.get("/")
def get_b():
    return {"msg": "B"}


@router_c.get("/")
def get_c():
    return {"msg": "C"}


router_b.include_router(router=router_c, prefix="/c")
router_a.include_router(router=router_b, prefix="/b")
app.include_router(router=router_a, prefix="/a")


client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/a", 200, {"msg": "A"}),
        ("/a/b", 200, {"msg": "B"}),
        ("/a/b/c", 200, {"msg": "C"}),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_route_classes():
    routes = {}
    for r in app.router.routes:
        assert isinstance(r, Route)
        routes[r.path] = r
    assert getattr(routes["/a/"], "x_type") == "A"  # noqa: B009
    assert getattr(routes["/a/b/"], "x_type") == "B"  # noqa: B009
    assert getattr(routes["/a/b/c/"], "x_type") == "C"  # noqa: B009


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/a/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "summary": "Get A",
                        "operationId": "get_a_a__get",
                    }
                },
                "/a/b/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "summary": "Get B",
                        "operationId": "get_b_a_b__get",
                    }
                },
                "/a/b/c/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                        "summary": "Get C",
                        "operationId": "get_c_a_b_c__get",
                    }
                },
            },
        }
    )

def test_custom_api_route_without_strict_content_type():
    """
    Regression test for #15503:
    Custom APIRoute classes that explicitly list the previous
    __init__ parameters (without strict_content_type) should still
    work when registered via APIRouter.
    """

    class LegacyRoute(APIRoute):
        def __init__(
            self,
            path: str,
            endpoint: Callable[..., Any],
            *,
            response_model: Any = Default(None),
            status_code: int | None = None,
            tags: list[str | Enum] | None = None,
            dependencies: Sequence[params.Depends] | None = None,
            summary: str | None = None,
            description: str | None = None,
            response_description: str = "Successful Response",
            responses: dict[int | str, dict[str, Any]] | None = None,
            deprecated: bool | None = None,
            name: str | None = None,
            methods: set[str] | list[str] | None = None,
            operation_id: str | None = None,
            response_model_include: IncEx | None = None,
            response_model_exclude: IncEx | None = None,
            response_model_by_alias: bool = True,
            response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False,
            response_model_exclude_none: bool = False,
            include_in_schema: bool = True,
            response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
            dependency_overrides_provider: Any | None = None,
            callbacks: list[BaseRoute] | None = None,
            openapi_extra: dict[str, Any] | None = None,
            generate_unique_id_function: Callable[[APIRoute], str]
            | DefaultPlaceholder = Default(generate_unique_id),
        ) -> None:
            super().__init__(
                path,
                endpoint,
                response_model=response_model,
                status_code=status_code,
                tags=tags,
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses,
                deprecated=deprecated,
                name=name,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=response_model_exclude_unset,
                response_model_exclude_defaults=response_model_exclude_defaults,
                response_model_exclude_none=response_model_exclude_none,
                include_in_schema=include_in_schema,
                response_class=response_class,
                dependency_overrides_provider=dependency_overrides_provider,
                callbacks=callbacks,
                openapi_extra=openapi_extra,
                generate_unique_id_function=generate_unique_id_function,
            )

    app_legacy = FastAPI()
    router_legacy = APIRouter(route_class=LegacyRoute)

    @router_legacy.get("/items")
    def read_items():
        return {"ok": True}

    # This must not raise TypeError
    app_legacy.include_router(router_legacy)

    client_legacy = TestClient(app_legacy)
    response = client_legacy.get("/items")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_custom_api_route_with_kwargs():
    """
    Custom APIRoute classes using **kwargs should still receive
    strict_content_type and work correctly.
    """

    class KwargsRoute(APIRoute):
        def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            super().__init__(path, endpoint, **kwargs)

    app_kwargs = FastAPI()
    router_kwargs = APIRouter(route_class=KwargsRoute)

    @router_kwargs.get("/items")
    def read_items_kwargs():
        return {"ok": True}

    app_kwargs.include_router(router_kwargs)

    client_kwargs = TestClient(app_kwargs)
    response = client_kwargs.get("/items")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
