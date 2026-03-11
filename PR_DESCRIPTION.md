# Add `dependency_scope="lifespan"` for application-lifetime dependencies

Closes #617 (Further develop startup and shutdown events).

## Summary

Adds a third dependency scope **`lifespan`** to `Depends()`. Lifespan-scoped dependencies are evaluated **once** when the application starts, reused for every request, and cleaned up when the application shuts down. This enables shared resources (e.g. database connection pools, HTTP clients) to be injected via the existing dependency system without globals or manual `on_event("startup")` / `on_event("shutdown")` wiring.

## Example

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

def get_db_pool():
    pool = create_engine("postgresql://...")
    yield pool
    pool.dispose()

@app.get("/users")
def list_users(
    db: Annotated[Engine, Depends(get_db_pool, scope="lifespan")]
):
    return db.execute("SELECT * FROM users").fetchall()
```

- `get_db_pool` runs once at startup; the same `pool` is injected for every request.
- On shutdown, the code after `yield` runs (e.g. `pool.dispose()`).

## Changes

### 1. Public API

- **`fastapi/params.py`**: `Depends.scope` type extended to `Literal["function", "request", "lifespan"]`.
- **`fastapi/param_functions.py`**: `Depends(..., scope=...)` accepts `"lifespan"`; docstring updated.

### 2. Dependency model and resolution

- **`fastapi/dependencies/models.py`**: `Dependant.scope` and `computed_scope` support `"lifespan"`.
- **`fastapi/dependencies/utils.py`**:
  - `get_dependant(..., scope=...)`: accepts `"lifespan"`; validation: lifespan-scoped deps may only depend on other lifespan-scoped deps.
  - `solve_dependencies(..., solving_lifespan_deps=False)`: when `solving_lifespan_deps` is False (request path), lifespan-scoped deps are read only from the pre-seeded cache; when True (startup path), they are run and stored in the cache. Generator cleanup uses the lifespan `AsyncExitStack`.

### 3. Lifespan integration

- **`fastapi/applications.py`**:
  - `_wrap_lifespan_with_dependency_cache(original)`: wraps the user’s (or default) lifespan so that before entering it we run all lifespan-scoped dependencies and store the cache on `app.state.fastapi_lifespan_dependency_cache`.
  - `FastAPI` always passes a wrapped lifespan to the router and sets `router._fastapi_app = self` so the wrapper can access the app.
  - When the user does not pass a custom `lifespan`, the wrapper still runs and uses the default lifespan (`_DefaultLifespan`) for the inner context.
- **`fastapi/routing.py`**:
  - `_collect_lifespan_dependants(router)`: collects all unique lifespan-scoped dependants from the router’s routes.
  - `_run_lifespan_dependencies(router, dependency_cache, lifespan_stack)`: builds a synthetic dependant, creates a minimal request with the lifespan stack in scope, and calls `solve_dependencies(..., solving_lifespan_deps=True)` to fill the cache.
  - HTTP and WebSocket handlers pass a **copy** of `app.state.fastapi_lifespan_dependency_cache` into `solve_dependencies` so request-scoped values do not pollute the shared cache.

### 4. Tests

- **`tests/test_dependency_lifespan_scope.py`**: tests that a lifespan-scoped dependency is started once at startup, reused for multiple requests, and stopped once at shutdown; works with a custom lifespan; and that the same instance is injected across requests.

## Backward compatibility

- Existing `scope="function"` and `scope="request"` behavior is unchanged.
- If no lifespan-scoped dependency is used, the wrapper is a no-op (cache stays empty; request path creates a fresh cache per request as today).
- `on_event("startup")` / `on_event("shutdown")` and the `lifespan=` context manager continue to work as before.

## Notes

- Lifespan-scoped dependencies must not depend on request- or function-scoped dependencies; the reverse is allowed (endpoints can depend on lifespan-scoped deps).
- If a lifespan-scoped dependency is declared but the application is run without going through the normal lifespan (e.g. test client without entering lifespan), a clear `DependencyScopeError` is raised when the dependency is first resolved.
