# Modelos de Parâmetros de Cookie { #cookie-parameter-models }

Se você possui um grupo de **cookies** que estão relacionados, você pode criar um **modelo Pydantic** para declará-los. 🍪

Isso lhe permitiria **reutilizar o modelo** em **diversos lugares** e também declarar validações e metadata para todos os parâmetros de uma vez. 😎

/// note | Nota

Isso é suportado desde a versão `0.115.0` do FastAPI. 🤓

///

/// tip | Dica

Essa mesma técnica se aplica para `Query`, `Cookie`, e `Header`. 😎

///

## Cookies com Modelos Pydantic { #cookies-with-a-pydantic-model }

Declare os parâmetros de **cookie** de que você precisa em um **modelo Pydantic**, e depois declare o parâmetro como `Cookie`:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

O **FastAPI** irá **extrair** os dados para **cada campo** dos **cookies** recebidos na requisição e lhe fornecer o modelo Pydantic que você definiu.

## Verifique a Documentação { #check-the-docs }

Você pode ver os cookies definidos na IU da documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | Nota

Tenha em mente que, como os **navegadores lidam com cookies** de maneira especial e por baixo dos panos, eles **não** permitem facilmente que o **JavaScript** lidem com eles.

Se você for na **IU da documentação da API** em `/docs` você poderá ver a **documentação** para cookies das suas *operações de rotas*.

Mas mesmo que você **adicionar os dados** e clicar em "Executar", pelo motivo da IU da documentação trabalhar com **JavaScript**, os cookies não serão enviados, e você verá uma mensagem de **erro** como se você não tivesse escrito nenhum dado.

///

## Proibir Cookies Adicionais { #forbid-extra-cookies }

Em alguns casos especiais (provavelmente não muito comuns), você pode querer **restringir** os cookies que você deseja receber.

Agora a sua API possui o poder de controlar o seu próprio <dfn title="Isso é uma brincadeira, só por precaução. Isso não tem nada a ver com consentimentos de cookies, mas é engraçado que até a API consegue rejeitar os coitados dos cookies. Coma um biscoito. 🍪">consentimento de cookie</dfn>. 🤪🍪

Você pode utilizar a configuração do modelo Pydantic para `proibir` qualquer campo `extra`:

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

Se o cliente tentar enviar alguns **cookies extras**, eles receberão um retorno de **erro**.

Coitados dos banners de cookies com todo o seu esforço para obter o seu consentimento para a <dfn title="Isso é uma outra piada. Não preste atenção em mim. Beba um café com o seu cookie. ☕">API rejeitá-lo</dfn>. 🍪

Por exemplo, se o cliente tentar enviar um cookie `santa_tracker` com o valor de `good-list-please`, o cliente receberá uma resposta de **erro** informando que o `santa_tracker` <dfn title="O papai noel desaprova a falta de biscoitos. 🎅 Ok, chega de piadas com os cookies.">cookie não é permitido</dfn>:

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

## Resumo { #summary }

Você consegue utilizar **modelos Pydantic** para declarar <dfn title="Coma um último biscoito antes de você ir embora. 🍪">**cookies**</dfn> no **FastAPI**. 😎
