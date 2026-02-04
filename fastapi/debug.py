"""Static dependency-graph introspection for the debug endpoint.

Nothing in this module executes any user callable.  It walks the already-built
Dependant trees that live on each APIRoute and serialises them to plain dicts.
"""

from collections.abc import Sequence
from typing import Any

from fastapi.dependencies.models import Dependant, _impartial, _unwrapped_call


def _resolve_callable_name(call: Any) -> str:
    """Return the display name of a callable, unwrapping partials and decorators."""
    if call is None:
        return "<unknown>"
    unwrapped = _unwrapped_call(call)
    if unwrapped is None:  # pragma: no cover
        return "<unknown>"
    # For classes the __name__ is the class name; for functions it is the
    # function name.  Both are what we want.
    return getattr(unwrapped, "__name__", type(unwrapped).__name__)


def _resolve_callable_module(call: Any) -> str:
    """Return the module path of a callable, unwrapping partials and decorators."""
    if call is None:
        return "<unknown>"
    unwrapped = _unwrapped_call(call)
    if unwrapped is None:  # pragma: no cover
        return "<unknown>"
    return getattr(unwrapped, "__module__", "<unknown>")


def build_dependency_graph(
    dependant: Dependant,
    *,
    _path_seen: frozenset[Any] | None = None,
) -> dict[str, Any]:
    """Serialise one Dependant node (and its entire sub-tree) to a plain dict.

    Cycle / repeat detection operates on the *current root-to-node path* only.
    The same callable appearing in two sibling branches is NOT flagged — only
    an actual ancestor repeat on the same path triggers ``cached_repeat: true``.
    """
    if _path_seen is None:
        _path_seen = frozenset()

    cache_key = dependant.cache_key
    is_repeat = cache_key in _path_seen

    node: dict[str, Any] = {
        "callable_name": _resolve_callable_name(dependant.call),
        "callable_module": _resolve_callable_module(dependant.call),
        "scope": dependant.computed_scope,
        "is_yield": dependant.is_gen_callable or dependant.is_async_gen_callable,
        "is_async": dependant.is_async_gen_callable or dependant.is_coroutine_callable,
        "security_scopes": list(dependant.oauth_scopes) if dependant.oauth_scopes else [],
        "is_security_scheme": dependant._is_security_scheme,
    }

    if is_repeat:
        # Ancestor repeat on this path — stop recursion here.
        node["cached_repeat"] = True
        node["sub_dependencies"] = []
    else:
        # Extend the path with the current node before recursing into children.
        extended_path = _path_seen | {cache_key}
        node["sub_dependencies"] = [
            build_dependency_graph(sub, _path_seen=extended_path)
            for sub in dependant.dependencies
        ]

    return node


def get_all_route_graphs(routes: Sequence[Any]) -> list[dict[str, Any]]:
    """Build the full debug payload from a list of registered routes.

    Non-APIRoute entries (e.g. Mount, plain Starlette Route) are skipped.
    """
    # Import here to avoid circular imports at module load time.
    from fastapi.routing import APIRoute

    result: list[dict[str, Any]] = []
    for route in routes:
        if not isinstance(route, APIRoute):
            continue
        entry: dict[str, Any] = {
            "path": route.path_format,
            "methods": sorted(route.methods) if route.methods else [],
            "operation_id": route.unique_id,
            "dependency_graph": build_dependency_graph(route.dependant),
        }
        result.append(entry)
    return result
