# Modelos de Formulários { #form-models }

Você pode utilizar **Modelos Pydantic** para declarar **campos de formulários** no FastAPI.

/// note | Nota

Para utilizar formulários, instale primeiramente o [`python-multipart`](https://github.com/Kludex/python-multipart).

Adicione-o ao seu projeto:

```console
$ uv add python-multipart
```

///

/// note | Nota

Isto é suportado desde a versão `0.113.0` do FastAPI. 🤓

///

## Modelos Pydantic para Formulários { #pydantic-models-for-forms }

Você precisa apenas declarar um **modelo Pydantic** com os campos que deseja receber como **campos de formulários**, e então declarar o parâmetro como um `Form`:

{* ../../docs_src/request_form_models/tutorial001.py hl[9:11,15] *}

O **FastAPI** irá **extrair** as informações para **cada campo** dos **dados do formulário** na requisição e dar para você o modelo Pydantic que você definiu.

Para [caixas de seleção HTML](request-forms.md#boolean-form-fields), declare campos booleanos com o valor padrão `False`.

## Confira a Documentação { #check-the-docs }

Você pode verificar na UI de documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Proíba Campos Extras de Formulários { #forbid-extra-form-fields }

Em alguns casos de uso especiais (provavelmente não muito comum), você pode desejar **restringir** os campos do formulário para aceitar apenas os declarados no modelo Pydantic. E **proibir** qualquer campo **extra**.

/// note | Nota

Isso é suportado desde a versão `0.114.0` do FastAPI. 🤓

///

Você pode utilizar a configuração de modelo do Pydantic para definir `forbid` para qualquer campo `extra`:

{* ../../docs_src/request_form_models/tutorial002.py hl[12] *}

Caso um cliente tente enviar informações adicionais, ele receberá um retorno de **erro**.

Por exemplo, se o cliente tentar enviar os campos de formulário:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

Ele receberá um retorno de erro informando-o que o campo `extra` não é permitido:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Combine Modelos de Formulários { #combine-form-models }

Você pode combinar vários modelos de formulários com parâmetros `Form` individuais.

{* ../../docs_src/request_form_models/tutorial003.py hl[9:14,19:21] *}

O cliente envia `name`, `tags` e `token` como campos de formulário. Cada modelo valida os campos do formulário de forma independente.

A configuração `extra` de cada modelo se aplica a todos os campos do formulário, incluindo campos e arquivos declarados em outros parâmetros ou dependências. Com `extra="forbid"`, qualquer campo fora desse modelo é rejeitado. Com `extra="allow"`, esses campos são incluídos como extras do modelo.

Se várias declarações usarem o mesmo nome de campo de formulário, cada uma validará o valor desse campo. Use tipos e restrições compatíveis para campos compartilhados, para que o esquema OpenAPI possa descrevê-los de forma consistente.

## Modelos de Formulários Opcionais { #optional-form-models }

Declare um modelo de formulário com `| None` e um valor padrão `None` para tornar o grupo opcional.

{* ../../docs_src/request_form_models/tutorial005.py hl[17] *}

Se nem `name` nem `age` forem enviados, `profile` será `None`. Se qualquer um deles for enviado, o FastAPI validará o modelo e exigirá ambos os campos. Um valor vazio enviado também conta como fornecimento de um campo.

Usar `| None` sem um valor padrão ainda torna o parâmetro obrigatório.

Campos extras seguem a configuração `extra` do modelo. Extras ignorados não fazem com que o modelo seja considerado presente.

Um modelo opcional que contenha apenas caixas de seleção desmarcadas é omitido. Envie um valor como `enabled=false` para fornecê-lo explicitamente.

## Uniões Opcionais de Modelos de Formulários { #optional-unions-of-form-models }

Você também pode usar uma união opcional de modelos.

{* ../../docs_src/request_form_models/tutorial006.py hl[9:16,21] *}

Se nenhum campo de formulário for enviado, `contact` será `None`. Envie `kind=person` com `name`, ou `kind=company` com `company_name`. O discriminador seleciona qual modelo validar.

## Combine Uniões de Modelos de Formulários { #combine-unions-of-form-models }

Você pode combinar uniões com outros modelos de formulários, parâmetros `Form` individuais e parâmetros `File`. Cada união é validada de forma independente.

{* ../../docs_src/request_form_models/tutorial007.py hl[31:35] *}

Envie todos os campos no mesmo formulário. Por exemplo, envie `contact_type=person`, `name=Rick`, `notification_type=email`, `email=rick@example.com` e `token=secret`.

Omita os campos de notificação para deixar `notification` como `None`.

## Modelos de Formulários e Arquivos { #form-models-and-files }

Você também pode combinar um modelo de formulário com [parâmetros de arquivo](request-files.md).

{* ../../docs_src/request_form_models/tutorial004.py hl[14] *}

Aqui, o cliente envia o campo `name` e o arquivo `avatar` usando `multipart/form-data`.

## Resumo { #summary }

Você pode utilizar modelos Pydantic para declarar campos de formulários no FastAPI. 😎
