## Testing Events, `startup` and `shutdown`

When you need your event handlers (`startup` and `shutdown`) to run in your tests, you can use the `TestClient` with a `with` statement:

```Python hl_lines="9 10 11 12 20 21 22 23 24"
{!./src/app_testing/tutorial003.py!}
```