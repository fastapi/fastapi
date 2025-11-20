# Modelos de Parâmetros de Consulta { #query-parameter-models }

Se você possui um grupo de **parâmetros de consultas** que são relacionados, você pode criar um **modelo Pydantic** para declará-los.

Isso permitiria que você **reutilizasse o modelo** em **diversos lugares**, e também declarasse validações e metadados de todos os parâmetros de uma única vez. 😎

/// note | Nota

Isso é suportado desde o FastAPI versão `0.115.0`. 🤓

///

## Parâmetros de Consulta com um Modelo Pydantic { #query-parameters-with-a-pydantic-model }

Declare os **parâmetros de consulta** que você precisa em um **modelo Pydantic**, e então declare o parâmetro como `Query`:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

O **FastAPI** **extrairá** os dados para **cada campo** dos **parâmetros de consulta** presentes na requisição, e fornecerá o modelo Pydantic que você definiu.


## Verifique os Documentos { #check-the-docs }

Você pode ver os parâmetros de consulta nos documentos de IU em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Restrinja Parâmetros de Consulta Extras { #forbid-extra-query-parameters }

Em alguns casos especiais (provavelmente não muito comuns), você queira **restrinjir** os parâmetros de consulta que deseja receber.

Você pode usar a configuração do modelo Pydantic para `forbid` (proibir) qualquer campo `extra`:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Caso um cliente tente enviar alguns dados **extras** nos **parâmetros de consulta**, eles receberão um retorno de **erro**.

Por exemplo, se o cliente tentar enviar um parâmetro de consulta `tool` com o valor `plumbus`, como:

```http
https://example.com/items/?limit=10&tool=plumbus
```

Eles receberão um retorno de **erro** informando-os que o parâmentro de consulta `tool` não é permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Resumo { #summary }

Você pode utilizar **modelos Pydantic** para declarar **parâmetros de consulta** no **FastAPI**. 😎

/// tip | Dica

Alerta de spoiler: você também pode utilizar modelos Pydantic para declarar cookies e cabeçalhos, mas você irá ler sobre isso mais a frente no tutorial. 🤫

///
