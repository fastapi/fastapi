from __future__ import annotations

from contextlib import AsyncExitStack
from typing import TYPE_CHECKING, Any, Callable, Dict, List

from fastapi.dependencies.models import LifespanDependant
from fastapi.dependencies.utils import solve_lifespan_dependant
from fastapi.routing import APIRoute, APIWebSocketRoute
from fastapi.types import LifespanDependencyCacheKey

if TYPE_CHECKING:  # pragma: nocover
    from fastapi import FastAPI


def _get_lifespan_dependants(app: FastAPI) -> List[LifespanDependant]:
    lifespan_dependants_cache: Dict[LifespanDependencyCacheKey, LifespanDependant] = {}
    for route in app.router.routes:
        if not isinstance(route, (APIWebSocketRoute, APIRoute)):
            continue

        for sub_dependant in route.lifespan_dependencies:
            if sub_dependant.cache_key in lifespan_dependants_cache:
                continue

            lifespan_dependants_cache[sub_dependant.cache_key] = sub_dependant

    return list(lifespan_dependants_cache.values())


async def resolve_lifespan_dependants(
    *, app: FastAPI, async_exit_stack: AsyncExitStack
) -> Dict[LifespanDependencyCacheKey, Callable[..., Any]]:
    lifespan_dependants = _get_lifespan_dependants(app)
    dependency_cache: Dict[LifespanDependencyCacheKey, Callable[..., Any]] = {}
    for lifespan_dependant in lifespan_dependants:
        solved_dependency = await solve_lifespan_dependant(
            dependant=lifespan_dependant,
            dependency_overrides_provider=app,
            dependency_cache=dependency_cache,
            async_exit_stack=async_exit_stack,
        )

        dependency_cache.update(solved_dependency.dependency_cache)

    return dependency_cache
