# `Request`-Klasse

Sie können einen Parameter in einer *Pfadoperation-Funktion* oder einer Abhängigkeit als vom Typ `Request` deklarieren und dann direkt auf das Requestobjekt zugreifen, ohne jegliche Validierung, usw.

Sie können es direkt von `fastapi` importieren:

```python
from fastapi import Request
```

!!! tip "Tipp"
    Wenn Sie Abhängigkeiten definieren möchten, die sowohl mit HTTP als auch mit WebSockets kompatibel sein sollen, können Sie einen Parameter definieren, der eine `HTTPConnection` anstelle eines `Request` oder eines `WebSocket` akzeptiert.

::: fastapi.Request
