# Router-Level Exception Handlers { #router-level-exception-handlers }

In the [Tutorial - Handling Errors](../tutorial/handling-errors.md){.internal-link target=_blank} you learned how to add custom exception handlers to your **FastAPI** application using `@app.exception_handler()`.

Those handlers apply **globally** to all routes in the application.

But sometimes you want to handle exceptions differently depending on which part of your application raised them. For example, a group of routes related to payments might need different error handling than routes for user profiles.

You can do this by adding **exception handlers directly to an `APIRouter`**.

## Add Exception Handlers to a Router { #add-exception-handlers-to-a-router }

You can pass `exception_handlers` when creating an `APIRouter`, using the same format as with the `FastAPI` app — a dictionary where keys are exception classes (or status codes) and values are handler functions:

{* ../../docs_src/handling_errors/tutorial007_py310.py hl[10:20] *}

Now, if a `UnicornException` is raised in any route within this router, the router's handler will catch it.

Routes outside this router are **not affected** by the router's exception handlers.

## Router Handlers Override App Handlers { #router-handlers-override-app-handlers }

If both the app and a router define a handler for the same exception, the **router's handler takes priority** for routes within that router. The app-level handler still applies to all other routes.

{* ../../docs_src/handling_errors/tutorial008_py310.py hl[13:21,44:49] *}

In this example:

* A request to `/magic/unicorns/yolo` uses the **global** handler (the `magic_router` doesn't define its own).
* A request to `/special/unicorns/yolo` uses the **router-level** handler (defined on the `special_router`).

This lets you customize error handling per section of your API while keeping a sensible default at the app level.

## Using `add_exception_handler` { #using-add-exception-handler }

You can also add exception handlers to a router after creation, using the `add_exception_handler()` method:

```python
router = APIRouter()
router.add_exception_handler(UnicornException, unicorn_exception_handler)
```

This works the same as passing `exception_handlers` in the constructor.

## Nested Router Precedence { #nested-router-precedence }

When routers are nested (a router includes another router), exception handlers follow this precedence order (highest to lowest):

1. The **innermost (child) router**'s handlers
2. The **parent router**'s handlers
3. The **app-level** handlers

This means a child router can override its parent's handlers for its own routes.

## Status Code Handlers { #status-code-handlers }

Just like app-level handlers, you can use **integer status codes** as keys to handle specific HTTP error responses:

```python
from starlette.exceptions import HTTPException

def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Custom 404: resource not found"},
    )

router = APIRouter(
    exception_handlers={404: not_found_handler}
)
```

## Recap { #recap }

* Pass `exception_handlers` to `APIRouter()` to scope handlers to that router's routes.
* Use `router.add_exception_handler()` to add handlers after creation.
* Router-level handlers **override** app-level handlers for the same exception type.
* Routes **outside** the router are unaffected.
* Nested routers follow **child > parent > app** precedence.
