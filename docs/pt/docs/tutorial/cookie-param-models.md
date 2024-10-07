# Modelos de Parâmetros de Cookie

Se você possui um grupo de **cookies** que estão relacionados, você pode criar um **modelo Pydantic** para declará-los. 🍪

Isso lhe permitiria **reutilizar o modelo** em **diversos lugares** e também declarar validações e metadata para todos os parâmetros de uma vez. 😎

/// note | Nota

Isso é suportado desde a versão `0.115.0` do FastAPI. 🤓

///

/// tip | Dica

Essa mesma técnica se aplica para `Query`, `Cookie`, e `Header`. 😎

///

## Cookies com Modelos Pydantic

Declare o parâmetro de **cookie** que você precisa em um **modelo Pydantic**, e depois declare o parâmetro como um `Cookie`:

//// tab | Python 3.10+

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10-13  17"
{!> ../../../docs_src/cookie_param_models/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="7-10  14"
{!> ../../../docs_src/cookie_param_models/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="9-12  16"
{!> ../../../docs_src/cookie_param_models/tutorial001.py!}
```

////

O **FastAPI** irá **extrair** os dados para **cada campo** dos **cookies** recebidos na requisição e lhe fornecer o modelo Pydantic que você definiu.

## Verifique os Documentos

Você pode ver os cookies definidos na IU dos documentos em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | Informação

Tenha em mente que, como os **navegadores lidam com cookies** de maneira especial e por baixo dos panos, eles **não** permitem facilmente que o **JavaScript** lidem com eles.

Se você for na **IU de documentos da API** em `/docs` você poderá ver a **documentação** para cookies das suas *operações de rotas*.

Mas mesmo que você **adicionar os dados** e clicar em "Executar", pelo motivo da IU dos documentos trabalharem com **JavaScript**, os cookies não serão enviados, e você verá uma mensagem de **erro** como se você não tivesse escrito nenhum dado.

///

## Proibir Cookies Adicionais

Em alguns casos especiais (provavelmente não muito comuns), você pode querer **restringir** os cookies que você deseja receber.

Agora a sua API possui o poder de contrar o seu próprio <abbr title="Isso é uma brincadeira, só por precaução. Isso não tem nada a ver com consentimentos de cookies, mas é engraçado que até a API consegue rejeitar os coitados dos cookies. Coma um biscoito. 🍪">consentimento de cookie</abbr>. 🤪🍪


 Você pode utilizar a configuração do modelo Pydantic para `proibir` qualquer campo `extra`.


//// tab | Python 3.9+

```Python hl_lines="10"
{!> ../../../docs_src/cookie_param_models/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/cookie_param_models/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="10"
{!> ../../../docs_src/cookie_param_models/tutorial002.py!}
```

////

Se o cliente tentar enviar alguns **cookies extras**, eles receberão um retorno de **erro**.

Coitados dos banners de cookies com todo o seu esforço para obter o seu consentimento para a <abbr title="Isso é uma outra piada. Não preste atenção em mim. Beba um café com o seu cookie. ☕">API rejeitá-lo</abbr>. 🍪

Por exemplo, se o cliente tentar enviar um cookie `santa_tracker` com o valor de `good-list-please`, o cliente receberá uma resposta de **erro** informando que o <abbr title="O papai noel desaprova a falta de biscoitos. 🎅 Ok, chega de piadas com os cookies.">cookie `santa_tracker` is not allowed</abbr>:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Resumo

Você consegue utilizar **modelos Pydantic** para declarar <abbr title="Coma um último biscoito antes de você ir embora. 🍪">**cookies**</abbr> no **FastAPI**. 😎
