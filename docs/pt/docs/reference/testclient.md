# Cliente de Teste - `TestClient`

Você pode usar a classe `TestClient` para testar aplicações FastAPI sem criar uma conexão HTTP e socket real, apenas comunicando diretamente com o código do FastAPI.

Leia mais sobre isso em [FastAPI documentação sobre Testes](https://fastapi.tiangolo.com/tutorial/testing/).

Você pode importá-la diretamente de `fastapi.testclient`:

```python
from fastapi.testclient import TestClient
```

::: fastapi.testclient.TestClient
