# Testing WebSockets

You can use the same `TestClient` to test WebSockets.

For this, you use the `TestClient` in a `with` statement, connecting to the WebSocket:

```Python hl_lines="27-31"
{!../../../docs_src/app_testing/tutorial002.py!}
```

!!! note
    For more details, check Starlette's documentation for <a href="https://www.starlette.io/testclient/#testing-websocket-sessions" class="external-link" target="_blank">testing WebSockets</a>.
