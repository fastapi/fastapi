# Modelos de Parâmetros do Cabeçalho

Se você possui um grupo de **parâmetros de cabeçalho** relacionados, você pode criar um **modelo do Pydantic** para declará-los.

Isso vai lhe permitir **reusar o modelo** em **múltiplos lugares** e também declarar validações e metadadados para todos os parâmetros de uma vez. 😎

/// note | Nota

Isso é possível desde a versão `0.115.0` do FastAPI. 🤓

///

## Parâmetros do Cabeçalho com um Modelo Pydantic

Declare os **parâmetros de cabeçalho** que você precisa em um **modelo do Pydantic**, e então declare o parâmetro como `Header`:

//// tab | Python 3.10+

```Python hl_lines="9-14  18"
{!> ../../docs_src/header_param_models/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9-14  18"
{!> ../../docs_src/header_param_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10-15  19"
{!> ../../docs_src/header_param_models/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="7-12  16"
{!> ../../docs_src/header_param_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="9-14  18"
{!> ../../docs_src/header_param_models/tutorial001_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="7-12  16"
{!> ../../docs_src/header_param_models/tutorial001_py310.py!}
```

////

O **FastAPI** irá **extrair** os dados de **cada campo** a partir dos **cabeçalhos** da requisição e te retornará o modelo do Pydantic que você definiu.

### Checando a documentação

Você pode ver os headers necessários na interface gráfica da documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

### Proibindo Cabeçalhos adicionais

Em alguns casos de uso especiais (provavelmente não muito comuns), você pode querer **restringir** os cabeçalhos que você quer receber.

Você pode usar a configuração dos modelos do Pydantic para proibir (`forbid`) quaisquer campos `extra`:

//// tab | Python 3.10+

```Python hl_lines="10"
{!> ../../docs_src/header_param_models/tutorial002_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../docs_src/header_param_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../docs_src/header_param_models/tutorial002_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="8"
{!> ../../docs_src/header_param_models/tutorial002_py310.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="10"
{!> ../../docs_src/header_param_models/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="10"
{!> ../../docs_src/header_param_models/tutorial002.py!}
```

////

Se um cliente tentar enviar alguns **cabeçalhos extra**, eles irão receber uma resposta de **erro**.

Por exemplo, se o cliente tentar enviar um cabeçalho `tool` com o valor `plumbus`, ele irá receber uma resposta de **erro** informando que o parâmetro do cabeçalho `tool` não é permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Resumo

Você pode utilizar **modelos do Pydantic** para declarar **cabeçalhos** no **FastAPI**. 😎
