# Testing Lifespan Events

When you need your `lifespan` (or the `startup` and `shutdown` event handlers) to run in your tests, you can use the `TestClient` with a `with` statement:

```Python hl_lines="9-13  24-28"
{!../../../docs_src/app_testing/tutorial003.py!}
```
