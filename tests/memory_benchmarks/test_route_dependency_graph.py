import sys
from collections.abc import Callable
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute

if "--codspeed" not in sys.argv:
    pytest.skip(
        "Benchmark tests are skipped by default; run with --codspeed.",
        allow_module_level=True,
    )

LAST_DEPENDENCY_INDEX = 100
ROUTE_COUNT = 20
ROUTE_PATH_PREFIX = "/route-"


def _create_app() -> FastAPI:
    app = FastAPI()
    dependencies: dict[int, Callable[..., Any]] = {}

    def create_dependency(index: int) -> Callable[..., Any]:
        if index == LAST_DEPENDENCY_INDEX:

            def dependency() -> str:
                return str(index)

            dependency.__name__ = f"dependency_{index}"
            return dependency

        next_dependency = dependencies[index + 1]

        async def dependency(
            sub_dependency: Annotated[str, Depends(next_dependency)],
        ) -> str:
            return f"{index} -> {sub_dependency}"

        dependency.__name__ = f"dependency_{index}"
        return dependency

    for index in reversed(range(LAST_DEPENDENCY_INDEX + 1)):
        dependencies[index] = create_dependency(index)

    async def endpoint(
        value: Annotated[str, Depends(dependencies[0])],
    ) -> dict[str, str]:
        return {"value": value}

    for index in range(ROUTE_COUNT):
        app.add_api_route(f"{ROUTE_PATH_PREFIX}{index}", endpoint)

    return app


def test_route_dependency_graph(benchmark) -> None:
    app = benchmark(_create_app)
    api_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path.startswith(ROUTE_PATH_PREFIX)
    ]
    assert len(api_routes) == ROUTE_COUNT
