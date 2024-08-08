# Classe `HTTPConnection`

Quando você deseja definir dependências que devem ser compatíveis tanto com HTTP quanto com WebSockets, você pode definir um parâmetro que recebe uma `HTTPConnection` em vez de uma `Request` ou um `WebSocket`.

Você pode importá-la diretamente de `fastapi.requests`:

```python
from fastapi.requests import HTTPConnection
```

::: fastapi.requests.HTTPConnection
