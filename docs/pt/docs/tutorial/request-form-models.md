# Modelos de Formulários

Você pode utilizar **Modelos Pydantic** para declarar **campos de formulários** no FastAPI.

/// info | "Informação"

Para utilizar formulários, instale primeiramente o <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Certifique-se de criar um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, ativá-lo, e então instalar. Por exemplo:

```console
$ pip install python-multipart
```

///

/// note | "Nota"

Isto é suportado desde a versão `0.113.0` do FastAPI. 🤓

///

## Modelos Pydantic para Formulários

Você precisa apenas declarar um **modelo Pydantic** com os campos que deseja receber como **campos de formulários**, e então declarar o parâmetro como um `Form`:

//// tab | Python 3.9+

```Python hl_lines="9-11  15"
{!> ../../../docs_src/request_form_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8-10  14"
{!> ../../../docs_src/request_form_models/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="7-9  13"
{!> ../../../docs_src/request_form_models/tutorial001.py!}
```

////

O **FastAPI** irá **extrair** as informações para **cada campo** dos **dados do formulário** na requisição e dar para você o modelo Pydantic que você definiu.

## Confira os Documentos

Você pode verificar na UI de documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## Proibir Campos Extras de Formulários

Em alguns casos de uso especiais (provavelmente não muito comum), você pode desejar **restringir** os campos do formulário para aceitar apenas os declarados no modelo Pydantic. E **proibir** qualquer campo **extra**.

/// note | "Nota"

Isso é suportado deste a versão `0.114.0` do FastAPI. 🤓

///

Você pode utilizar a configuração de modelo do Pydantic para `proibir` qualquer campo `extra`:

//// tab | Python 3.9+

```Python hl_lines="12"
{!> ../../../docs_src/request_form_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/request_form_models/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="10"
{!> ../../../docs_src/request_form_models/tutorial002.py!}
```

////

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

## Resumo

Você pode utilizar modelos Pydantic para declarar campos de formulários no FastAPI. 😎
