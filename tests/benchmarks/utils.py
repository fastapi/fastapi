from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends, FastAPI

LAST_DEPENDENCY_INDEX = 100
ROUTE_COUNT = 20
ROUTE_PATH_PREFIX = "/openapi-route-"


def create_openapi_app() -> FastAPI:
    app = FastAPI()
    dependencies: dict[int, Callable[..., Any]] = {}

    def create_dependency(index: int) -> Callable[..., Any]:
        if index == LAST_DEPENDENCY_INDEX:

            def dependency(query_value: int = index) -> str:
                return str(query_value)

            dependency.__name__ = f"dependency_{index}"
            return dependency

        next_dependency = dependencies[index + 1]

        async def dependency(
            sub_dependency: Annotated[str, Depends(next_dependency)],
            query_value: int = index,
        ) -> str:
            return f"{query_value} -> {sub_dependency}"

        dependency.__name__ = f"dependency_{index}"
        return dependency

    for index in reversed(range(LAST_DEPENDENCY_INDEX + 1)):
        dependencies[index] = create_dependency(index)

    async def endpoint(
        value: Annotated[str, Depends(dependencies[0])],
    ) -> dict[str, str]:
        return {"value": value}

    for index in range(ROUTE_COUNT):
        app.add_api_route(f"{ROUTE_PATH_PREFIX}{index}", endpoint, methods=["GET"])

    return app


def generate_openapi(app: FastAPI) -> dict[str, Any]:
    app.openapi_schema = None
    return app.openapi()
