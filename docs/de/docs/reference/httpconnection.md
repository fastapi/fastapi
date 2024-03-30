# `HTTPConnection`-Klasse

Wenn Sie Abhängigkeiten definieren möchten, die sowohl mit HTTP als auch mit WebSockets kompatibel sein sollen, können Sie einen Parameter definieren, der eine `HTTPConnection` anstelle eines `Request` oder eines `WebSocket` akzeptiert.

Sie können diese von `fastapi.requests` importieren:

```python
from fastapi.requests import HTTPConnection
```

::: fastapi.requests.HTTPConnection
