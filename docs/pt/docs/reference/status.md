# Status Codes

Você pode importar o módulo `status` de `fastapi`:

```python
from fastapi import status
```

`status` é fornecido diretamente pelo Starlette.

Ele contém um grupo de constantes nomeadas (variáveis) com códigos de status HTTP representados por números inteiros.

Por exemplo:

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* etc.

É conveniente acessar rapidamente os códigos de status HTTP (e WebSocket) em sua aplicação, usando o recurso de autocompletar para o nome sem precisar lembrar dos códigos de status inteiros de memória.

Leia mais sobre isso em [FastAPI documentação sobre Códigos de Status de Resposta](https://fastapi.tiangolo.com/tutorial/response-status-code/).

## Exemplo

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

::: fastapi.status
