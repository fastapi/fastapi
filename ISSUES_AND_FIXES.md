# RubberDuck MCP analysis: PR issues and proposed fixes

This document summarizes the issues identified (from CI and code analysis) and the fixes applied or recommended.

---

## 1. **`AttributeError: 'FastAPI' object has no attribute '_shutdown'`** (fixed)

**Cause:** `_DefaultLifespan` expects a router (with `_startup` / `_shutdown`). When no custom `lifespan` is passed, the wrapper was calling `original(app)` where `app` is the FastAPI instance. The default lifespan lambda was then effectively `_DefaultLifespan(app)` instead of `_DefaultLifespan(app.router)`.

**Fix (already in your branch):** In `fastapi/applications.py`, the default lifespan is built with the router, not the app:

```python
_inner_lifespan = (
    lifespan
    if lifespan is not None
    else (
        lambda app: routing._DefaultLifespan(
            getattr(app, "router", app)
        )
    )
)
```

So when the framework passes the FastAPI instance, `original(app)` runs the lambda and returns `_DefaultLifespan(app.router)`, which has `_startup`/`_shutdown`. No code change needed for this item.

---

## 2. **Lifespan cache not run when framework passes FastAPI as `app`** (fixed in this session)

**Cause:** In `_wrap_lifespan_with_dependency_cache`, we used:

```python
fastapi_app = getattr(app, "_fastapi_app", None)
```

We set `_fastapi_app` only on the **router** (`self.router._fastapi_app = self`). When the ASGI server runs the lifespan, it passes the **FastAPI** instance as `app`, which has no `_fastapi_app` attribute, so `fastapi_app` was `None` and we never ran lifespan-scoped dependencies or set the cache.

**Fix applied:** Resolve the FastAPI app whether the framework passes the FastAPI instance or the router:

```python
# Resolve FastAPI app: framework may pass FastAPI (has .router) or router (has ._fastapi_app).
fastapi_app = (
    app
    if hasattr(app, "router")
    else getattr(app, "_fastapi_app", None)
)
```

- When `app` is the **FastAPI** instance, it has `.router` → use `app` as `fastapi_app`.
- When `app` is the **router** (e.g. mounted app), use `app._fastapi_app`.

**File:** `fastapi/applications.py` (in `_wrap_lifespan_with_dependency_cache`).

---

## 3. **`AttributeError: 'async_generator' object has no attribute '__aexit__'`** (fixed)

**Cause:** When the user passes a plain async generator or sync generator lifespan (no `@asynccontextmanager`), `original(app)` returns a generator object. The wrapper was calling `orig_cm.__aenter__()` and `orig_cm.__aexit__()` on it, but generators do not have `__aexit__`, so tests like `test_router_async_generator_lifespan` and `test_router_sync_generator_lifespan` failed.

**Fix applied:** Normalize the lifespan **before** wrapping (in `FastAPI.__init__`), so that the function we pass to `_wrap_lifespan_with_dependency_cache` always returns an async context manager when called with `app`:

- `inspect.isasyncgenfunction(lifespan)` → use `asynccontextmanager(lifespan)` (same as `APIRouter`).
- `inspect.isgeneratorfunction(lifespan)` → use `routing._wrap_gen_lifespan_context(lifespan)` (same as `APIRouter`).
- Else (e.g. `@asynccontextmanager` or default) → use as-is.

Then `_wrap_lifespan_with_dependency_cache` always receives a callable that returns an ACM; the wrapper no longer needs to normalize the result of `original(app)`.

**File:** `fastapi/applications.py` (`_inner_lifespan` construction and `_wrap_lifespan_with_dependency_cache` docstring).

---

## 4. **Label check failed** (manual step)

**Error:**
`required 1 of 'breaking', 'security', 'feature', 'bug', 'refactor', 'upgrade', 'docs', 'lang-all', 'internal', but found 0`

**Fix:** On GitHub, open your PR → in the right sidebar under **Labels**, add the **`feature`** label. No code change.

---

## 5. **Pre-commit / formatting** (run locally)

**Fix:** In your FastAPI repo:

```bash
cd /Users/marcomarinucci/repos/fastapi
pip install pre-commit   # or: uv tool install pre-commit
pre-commit run --all-files
```

Fix any reported issues (e.g. ruff format), then commit and push. The PR’s pre-commit job should then pass.

---

## 6. **Benchmark / Test failures** (if any remain)

If CI still shows failing tests:

1. Run the lifespan tests locally:
   ```bash
   uv run pytest tests/test_dependency_lifespan_scope.py -v
   ```
2. Run the full test suite for the areas you changed:
   ```bash
   uv run pytest tests/ -v -k "lifespan or dependency" --no-header -q
   ```
3. If a specific test or benchmark fails, paste the **exact traceback** or log and we can target that next.

---

## Summary of code changes in this session

| File | Change |
|------|--------|
| `fastapi/applications.py` | In `_wrap_lifespan_with_dependency_cache`, resolve `fastapi_app` so it works when the framework passes either the FastAPI instance (has `router`) or the router (has `_fastapi_app`). |

All other fixes (router passed to `_DefaultLifespan`, router passed to `_run_lifespan_dependencies`) were already present in your branch.

---

## RubberDuck MCP tools used

- **Codebase intelligence:** `analyze_repository` (essentiaMarco/fastapi, branch `feature/lifespan-dependency-scope`) to scan the PR branch.
- **Semantic intelligence:** `load_repo` (essentiaMarco/fastapi, subpath `fastapi`) to load and analyze `applications.py`, `routing.py`, `dependencies/utils.py`, etc.
- **plan_change:** Impact analysis for the lifespan wrapper fix (risk: low; change confined to lifespan handling).

If you want, we can next focus on a specific failing CI job (e.g. one test or benchmark) and derive a concrete patch from the logs.
