# Modelos de Formulários { #form-models }

Você pode utilizar **Modelos Pydantic** para declarar **campos de formulários** no FastAPI.

/// info | Informação

Para utilizar formulários, instale primeiramente o [`python-multipart`](https://github.com/Kludex/python-multipart).

Certifique-se de criar um [ambiente virtual](../virtual-environments.md), ativá-lo, e então instalar. Por exemplo:

```console
$ pip install python-multipart
```

///

/// note | Nota

Isto é suportado desde a versão `0.113.0` do FastAPI. 🤓

///

## Modelos Pydantic para Formulários { #pydantic-models-for-forms }

Você precisa apenas declarar um **modelo Pydantic** com os campos que deseja receber como **campos de formulários**, e então declarar o parâmetro como um `Form`:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

O **FastAPI** irá **extrair** as informações para **cada campo** dos **dados do formulário** na requisição e dar para você o modelo Pydantic que você definiu.

## Confira os Documentos { #check-the-docs }

Você pode verificar na UI de documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Proibir Campos Extras de Formulários { #forbid-extra-form-fields }

Em alguns casos de uso especiais (provavelmente não muito comum), você pode desejar **restringir** os campos do formulário para aceitar apenas os declarados no modelo Pydantic. E **proibir** qualquer campo **extra**.

/// note | Nota

Isso é suportado desde a versão `0.114.0` do FastAPI. 🤓

///

Você pode utilizar a configuração de modelo do Pydantic para `proibir` qualquer campo `extra`:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

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

## Resumo { #summary }

Você pode utilizar modelos Pydantic para declarar campos de formulários no FastAPI. 😎
