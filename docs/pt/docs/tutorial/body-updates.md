# Corpo - Atualizações { #body-updates }

## Atualização de dados existentes com `PUT` { #update-replacing-with-put }

Para atualizar um item, você pode usar a operação <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT" class="external-link" target="_blank">HTTP `PUT`</a>.

Você pode usar `jsonable_encoder` para converter os dados de entrada em dados que podem ser armazenados como JSON (por exemplo, com um banco de dados NoSQL). Por exemplo, convertendo `datetime` em `str`.

{* ../../docs_src/body_updates/tutorial001_py310.py hl[28:33] *}

`PUT` é usado para receber dados que devem substituir os dados existentes.

### Aviso sobre a substituição { #warning-about-replacing }

Isso significa que, se você quiser atualizar o item `bar` usando `PUT` com um corpo contendo:

```Python
{
    "name": "Barz",
    "price": 3,
    "description": None,
}
```

Como ele não inclui o atributo já armazenado `"tax": 20.2`, o modelo de entrada assumiria o valor padrão de `"tax": 10.5`.

E os dados seriam salvos com esse "novo" `tax` de `10.5`.

## Atualizações parciais com `PATCH` { #partial-updates-with-patch }

Você também pode usar a operação <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH" class="external-link" target="_blank">HTTP `PATCH`</a> para atualizar parcialmente os dados.

Isso significa que você pode enviar apenas os dados que deseja atualizar, deixando o restante intacto.

/// note | Nota

`PATCH` é menos comumente usado e conhecido do que `PUT`.

E muitas equipes usam apenas `PUT`, mesmo para atualizações parciais.

Você é **livre** para usá-los como preferir, **FastAPI** não impõe restrições.

Mas este guia te dá uma ideia de como eles são destinados a serem usados.

///

### Usando o parâmetro `exclude_unset` do Pydantic { #using-pydantics-exclude-unset-parameter }

Se você quiser receber atualizações parciais, é muito útil usar o parâmetro `exclude_unset` no método `.model_dump()` do modelo do Pydantic.

Como `item.model_dump(exclude_unset=True)`.

/// info | Informação

No Pydantic v1, o método que era chamado `.dict()` e foi descontinuado (mas ainda suportado) no Pydantic v2. Agora, deve-se usar o método `.model_dump()`.

Os exemplos aqui usam `.dict()` para compatibilidade com o Pydantic v1, mas você deve usar `.model_dump()` a partir do Pydantic v2.

///

Isso gera um `dict` com apenas os dados definidos ao criar o modelo `item`, excluindo os valores padrão.

Então, você pode usar isso para gerar um `dict` com apenas os dados definidos (enviados na solicitação), omitindo valores padrão:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[32] *}

### Usando o parâmetro `update` do Pydantic { #using-pydantics-update-parameter }

Agora, você pode criar uma cópia do modelo existente usando `.model_copy()`, e passar o parâmetro `update` com um `dict` contendo os dados para atualizar.

/// info | Informação

No Pydantic v1, o método era chamado `.copy()`, ele foi descontinuado (mas ainda suportado) no Pydantic v2, e renomeado para `.model_copy()`.

Os exemplos aqui usam `.copy()` para compatibilidade com o Pydantic v1, mas você deve usar `.model_copy()` com o Pydantic v2.

///

Como `stored_item_model.model_copy(update=update_data)`:

{* ../../docs_src/body_updates/tutorial002_py310.py hl[33] *}

### Recapitulando as atualizações parciais { #partial-updates-recap }

Resumindo, para aplicar atualizações parciais você pode:

* (Opcionalmente) usar `PATCH` em vez de `PUT`.
* Recuperar os dados armazenados.
* Colocar esses dados em um modelo do Pydantic.
* Gerar um `dict` sem valores padrão a partir do modelo de entrada (usando `exclude_unset`).
    * Dessa forma, você pode atualizar apenas os valores definidos pelo usuário, em vez de substituir os valores já armazenados com valores padrão em seu modelo.
* Criar uma cópia do modelo armazenado, atualizando seus atributos com as atualizações parciais recebidas (usando o parâmetro `update`).
* Converter o modelo copiado em algo que possa ser armazenado no seu banco de dados (por exemplo, usando o `jsonable_encoder`).
    * Isso é comparável ao uso do método `.model_dump()`, mas garante (e converte) os valores para tipos de dados que possam ser convertidos em JSON, por exemplo, `datetime` para `str`.
* Salvar os dados no seu banco de dados.
* Retornar o modelo atualizado.

{* ../../docs_src/body_updates/tutorial002_py310.py hl[28:35] *}

/// tip | Dica

Você pode realmente usar essa mesma técnica com uma operação HTTP `PUT`.

Mas o exemplo aqui usa `PATCH` porque foi criado para esses casos de uso.

///

/// note | Nota

Observe que o modelo de entrada ainda é validado.

Portanto, se você quiser receber atualizações parciais que possam omitir todos os atributos, precisará ter um modelo com todos os atributos marcados como opcionais (com valores padrão ou `None`).

Para distinguir os modelos com todos os valores opcionais para **atualizações** e modelos com valores obrigatórios para **criação**, você pode usar as ideias descritas em [Modelos Adicionais](extra-models.md){.internal-link target=_blank}.

///
