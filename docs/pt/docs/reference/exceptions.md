# Exceções - `HTTPException` e `WebSocketException`

Essas são as exceções que você pode lançar para mostrar erros ao cliente.

Quando você lança uma exceção, como aconteceria com o Python normal, o restante da execução é abortado. Dessa forma, você pode lançar essas exceções de qualquer lugar do código para abortar uma solicitação e mostrar o erro ao cliente.

Você pode usar:

* `HTTPException`
* `WebSocketException`

Essas exceções podem ser importadas diretamente do `fastapi`:

```python
from fastapi import HTTPException, WebSocketException
```

::: fastapi.HTTPException

::: fastapi.WebSocketException
