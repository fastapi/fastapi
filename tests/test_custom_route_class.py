import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from starlette.routing import Route

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


from collections.abc import Callable, Sequence
from typing import Any


class LegacyAPIRoute(APIRoute):
    """Route subclass with explicit __init__ matching the pre-strict_content_type signature."""

    def __init__(
        self,
        path: str,
        endpoint: "Callable[..., Any]",
        *,
        response_model: Any = None,
        status_code: "int | None" = None,
        tags: "list[str] | None" = None,
        dependencies: "Sequence[Any] | None" = None,
        summary: "str | None" = None,
        description: "str | None" = None,
        response_description: str = "Successful Response",
        responses: "dict[int | str, dict[str, Any]] | None" = None,
        deprecated: "bool | None" = None,
        methods: "set[str] | list[str] | None" = None,
        operation_id: "str | None" = None,
        response_model_include: "Any | None" = None,
        response_model_exclude: "Any | None" = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Any = None,
        name: "str | None" = None,
        dependency_overrides_provider: "Any | None" = None,
        callbacks: "list[Any] | None" = None,
        openapi_extra: "dict[str, Any] | None" = None,
        generate_unique_id_function: Any = None,
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
            name=name,
            dependency_overrides_provider=dependency_overrides_provider,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )


def test_legacy_route_class_with_explicit_init() -> None:
    """Custom APIRoute subclasses with explicit constructors (pre-strict_content_type)
    should work with APIRouter.add_api_route without raising TypeError."""
    app = FastAPI()
    router = APIRouter(route_class=LegacyAPIRoute)

    @router.get("/items")
    def read_items():
        return {"items": []}

    app.include_router(router)

    client = TestClient(app)
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"items": []}
