import inspect
import sys
from collections.abc import Callable
from typing import Any

import pytest
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute

if "--codspeed" not in sys.argv:
    pytest.skip(
        "Benchmark tests are skipped by default; run with --codspeed.",
        allow_module_level=True,
    )

LAST_DEPENDENCY_INDEX = 100
ENDPOINT_PARAMETER_COUNT = 50
ROUTE_PATH = "/dynamic-health"


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
            sub_dependency: str = Depends(next_dependency),
        ) -> str:
            return f"{index} -> {sub_dependency}"

        dependency.__name__ = f"dependency_{index}"
        return dependency

    for index in reversed(range(LAST_DEPENDENCY_INDEX + 1)):
        dependencies[index] = create_dependency(index)

    def create_endpoint() -> Callable[..., Any]:
        parameters = [
            inspect.Parameter(
                name=f"arg_{index}",
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=Depends(dependencies[index]),
                annotation=str,
            )
            for index in range(ENDPOINT_PARAMETER_COUNT)
        ]

        async def endpoint(**kwargs: str) -> dict[str, int]:
            return {"parameter_count": len(kwargs)}

        endpoint_with_signature: Any = endpoint
        endpoint_with_signature.__signature__ = inspect.Signature(parameters)
        return endpoint

    for method in ("GET", "POST"):
        app.add_api_route(
            ROUTE_PATH,
            create_endpoint(),
            methods=[method],
        )

    return app


def test_dependency_graph(benchmark) -> None:
    app = benchmark(_create_app)
    dynamic_routes = [
        route
        for route in app.routes
        if isinstance(route, APIRoute) and route.path == ROUTE_PATH
    ]
    assert len(dynamic_routes) == 2
    assert {method for route in dynamic_routes for method in route.methods} == {
        "GET",
        "POST",
    }
