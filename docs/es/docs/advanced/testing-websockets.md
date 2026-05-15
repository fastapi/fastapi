# Probando WebSockets { #testing-websockets }

Puedes usar el mismo `TestClient` para probar WebSockets.

Para esto, usas el `TestClient` en un statement `with`, conectándote al WebSocket:

{* ../../docs_src/app_testing/tutorial002_py310.py hl[27:31] *}

/// note | Nota

Para más detalles, revisa la documentación de Starlette sobre [probar WebSockets](https://www.starlette.dev/testclient/#testing-websocket-sessions).

///
