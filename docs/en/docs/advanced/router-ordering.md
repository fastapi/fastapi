# Automatic Route Reordering { #automatic-route-reordering }

FastAPI automatically reorders routes at startup so that **static routes** are matched
before **dynamic routes**. This prevents situations where a dynamic route like `/{id}`
could shadow a static route like `/users/admin`.

## Why It Matters { #why-it-matters }

Consider the following routes:

- `/users/admin` — a static route.
- `/users/{user_id}` — a dynamic route.

Without automatic reordering, a request to `/users/admin` might incorrectly match the
dynamic route `/users/{user_id}` instead of the intended static route.

FastAPI ensures that:

1. Routes with fewer dynamic segments (`{}`) are prioritized.
2. Among routes with the same number of dynamic segments, routes with more static segments come first.

## Example { #example }

{* ../../docs_src/automatic_routes_reordering/tutorial001.py *}

> In this example, static `/items/stats` and dynamic `/items/{item_id}` routes are registered together.

## Result { #result }

```
GET /items/123 → {"item_id":123}
GET /items/stats → {"status": "ok"}
```

## Result Without Route Reordering { #result-without-reordering }

```
GET /items/123 → {"item_id":123}
GET /items/stats → {
    "detail": [
        {
            "type":"int_parsing",
            "loc":["path","item_id"],
            "msg":"Input should be a valid integer,
            unable to parse string as an integer",
            "input":"stats"
        }
    ]
}
```

Note: You do not need to call any special method—FastAPI handles route
reordering automatically when the application starts.
