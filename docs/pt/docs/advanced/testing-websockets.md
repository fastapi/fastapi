# Testando WebSockets

Você pode usar o mesmo `TestClient` para testar WebSockets.

Para isso, você utiliza o `TestClient` dentro de uma instrução `with`, conectando com o WebSocket:

```Python hl_lines="27-31"
{!../../../docs_src/app_testing/tutorial002.py!}
```

/// note | "Nota"

Para mais detalhes, confira a documentação do Starlette para <a href="https://www.starlette.io/testclient/#testing-websocket-sessions" class="external-link" target="_blank">testar WebSockets</a>.

///
