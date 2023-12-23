# WebSockets

Bei der Definition von WebSockets deklarieren Sie normalerweise einen Parameter vom Typ `WebSocket` und können damit Daten vom Client lesen und an ihn senden. Er wird direkt von Starlette bereitgestellt, Sie können ihn aber von `fastapi` importieren:

```python
from fastapi import WebSocket
```

!!! tip "Tipp"
    Wenn Sie Abhängigkeiten definieren möchten, die sowohl mit HTTP als auch mit WebSockets kompatibel sein sollen, können Sie einen Parameter definieren, der eine `HTTPConnection` anstelle eines `Request` oder eines `WebSocket` akzeptiert.

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

Wenn ein Client die Verbindung trennt, wird eine `WebSocketDisconnect`-Exception ausgelöst, die Sie abfangen können.

Sie können diese direkt von `fastapi` importieren:

```python
from fastapi import WebSocketDisconnect
```

::: fastapi.WebSocketDisconnect

## WebSockets – zusätzliche Klassen

Zusätzliche Klassen für die Handhabung von WebSockets.

Werden direkt von Starlette bereitgestellt, Sie können sie jedoch von `fastapi` importieren:

```python
from fastapi.websockets import WebSocketDisconnect, WebSocketState
```

::: fastapi.websockets.WebSocketDisconnect

::: fastapi.websockets.WebSocketState
