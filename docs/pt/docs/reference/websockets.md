# WebSockets

Ao definir WebSockets, você normalmente declara um parâmetro do tipo `WebSocket` e com ele pode ler dados do cliente e enviar dados para ele.

Isso é fornecido diretamente pelo Starlette, mas você pode importá-lo de `fastapi`:

```python
from fastapi import WebSocket
```

!!! tip "Dica"
    Quando você quiser definir dependências que devem ser compatíveis com HTTP e WebSockets, você pode definir um parâmetro que aceite um `HTTPConnection` em vez de um `Request` ou um `WebSocket`.

::: fastapi.WebSocket
    options:
        members:
            - scope
            - app
            - url
            - base_url
            - headers
            - query_params
            - path_params
            - cookies
            - client
            - state
            - url_for
            - client_state
            - application_state
            - receive
            - send
            - accept
            - receive_text
            - receive_bytes
            - receive_json
            - iter_text
            - iter_bytes
            - iter_json
            - send_text
            - send_bytes
            - send_json
            - close

Quando um cliente se desconecta, uma exceção `WebSocketDisconnect` é levantada, e você pode capturá-la.

Você pode importá-la diretamente de `fastapi`:

```python
from fastapi import WebSocketDisconnect
```

::: fastapi.WebSocketDisconnect

## WebSockets - classes adicionais

Classes adicionais para manipular WebSockets.

Fornecidas diretamente pelo Starlette, mas você pode importá-las de `fastapi`:

```python
from fastapi.websockets import WebSocketDisconnect, WebSocketState
```

::: fastapi.websockets.WebSocketDisconnect

::: fastapi.websockets.WebSocketState
