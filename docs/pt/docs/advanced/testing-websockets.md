# Testando WebSockets { #testing-websockets }

Você pode usar o mesmo `TestClient` para testar WebSockets.

Para isso, você utiliza o `TestClient` dentro de uma instrução `with`, conectando com o WebSocket:

{* ../../docs_src/app_testing/tutorial002_py310.py hl[27:31] *}

/// note | Nota

Para mais detalhes, confira a documentação do Starlette para [testar WebSockets](https://www.starlette.dev/testclient/#testing-websocket-sessions).

///
