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

## Verifique a Documentação { #check-the-docs }

Você pode ver os parâmetros de consulta na IU da documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Restrinja Parâmetros de Consulta Extras { #forbid-extra-query-parameters }

Em alguns casos especiais (provavelmente não muito comuns), você pode querer **restringir** os parâmetros de consulta que deseja receber.

Você pode usar a configuração do modelo Pydantic para `forbid` qualquer campo `extra`:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Caso um cliente tente enviar alguns dados **extras** nos **parâmetros de consulta**, eles receberão um retorno de **erro**.

Por exemplo, se o cliente tentar enviar um parâmetro de consulta `tool` com o valor `plumbus`, como:

```http
https://example.com/items/?limit=10&tool=plumbus
```

Eles receberão um retorno de **erro** informando-os que o parâmetro de consulta `tool` não é permitido:

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

## Combine Modelos de Parâmetros { #combine-parameter-models }

Você pode declarar vários modelos de parâmetros de consulta e combiná-los com parâmetros de consulta individuais ou dependências.

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

Os parâmetros da requisição permanecem no mesmo nível.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

Não há chaves `pagination` ou `filters` na string de consulta. Cada modelo valida os parâmetros de consulta de forma independente, com seus próprios valores padrão, validadores de campo e de modelo. O mesmo se aplica quando os modelos ou parâmetros individuais são declarados em dependências.

Se os modelos compartilham um nome ou alias de parâmetro, cada modelo valida esse parâmetro da requisição de forma independente. Use nomes ou aliases distintos para valores independentes. O OpenAPI lista um parâmetro compartilhado apenas uma vez, assim como faz com parâmetros compartilhados com dependências, portanto as declarações compartilhadas deveriam descrever o mesmo tipo e as mesmas restrições.

A configuração `extra` de cada modelo se aplica a todos os parâmetros de consulta, incluindo os declarados em outros modelos ou dependências. Com `extra="forbid"`, qualquer parâmetro fora desse modelo é rejeitado. Com `extra="allow"`, esses parâmetros são incluídos como extras do modelo.

Isso também funciona para modelos `Header` e `Cookie`.

## Modelos Opcionais de Parâmetros de Consulta { #optional-query-parameter-models }

Declare um modelo de parâmetros de consulta com `| None` e um valor padrão de `None` para tornar o grupo opcional.

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

Se nem `start` nem `end` forem enviados, `date_range` será `None`. Se qualquer um deles for enviado, o FastAPI validará o modelo e exigirá ambos os campos.

Usar `| None` sem um valor padrão ainda torna o parâmetro obrigatório.

Parâmetros extras seguem a configuração `extra` do modelo. Extras ignorados não fazem com que o modelo seja considerado presente.

O OpenAPI lista os campos do grupo individualmente e os marca como opcionais.

Você também pode declarar [modelos de parâmetros de cabeçalho](header-param-models.md#optional-header-parameter-models) e [modelos de parâmetros de cookie](cookie-param-models.md#optional-cookie-parameter-models) opcionais.

## Resumo { #summary }

Você pode utilizar **modelos Pydantic** para declarar **parâmetros de consulta** no **FastAPI**. 😎

/// tip | Dica

Alerta de spoiler: você também pode utilizar modelos Pydantic para declarar cookies e cabeçalhos, mas você irá ler sobre isso mais a frente no tutorial. 🤫

///
