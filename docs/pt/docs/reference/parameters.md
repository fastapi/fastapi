# Parâmetros de Requisição

Informações de Referência para Parâmetros de Requisição

Estas são funções especiais que você pode colocar em parâmetros de *função de operação de rota* ou funções de dependência com `Annotated` para obter dados da requisição.

Inclui:

* `Query()`
* `Path()`
* `Body()`
* `Cookie()`
* `Header()`
* `Form()`
* `File()`

Você pode importá-la diretamente de `fastapi`:

```python
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

::: fastapi.Query

::: fastapi.Path

::: fastapi.Body

::: fastapi.Cookie

::: fastapi.Header

::: fastapi.Form

::: fastapi.File
