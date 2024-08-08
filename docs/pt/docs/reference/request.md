# Classe `Request`

Você pode declarar um parâmetro em uma *função de operação de rota* ou dependência como sendo do tipo `Request` e então você pode acessar diretamente o objeto de requisição bruto, sem nenhuma validação, etc.

Você pode importá-la diretamente de `fastapi`:

```python
from fastapi import Request
```

!!! tip | "Dica"
    Quando você quiser definir dependências que devem ser compatíveis com ambos HTTP e WebSockets, você pode definir um parâmetro que recebe um `HTTPConnection` em vez de um `Request` ou um `WebSocket`.

::: fastapi.Request
