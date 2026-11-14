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

{* ../../docs_src/cookie_param_models/tutorial001.py hl[9:12,16] *}

O **FastAPI** irá **extrair** os dados para **cada campo** dos **cookies** recebidos na requisição e lhe fornecer o modelo Pydantic que você definiu.

## Verifique a Documentação { #check-the-docs }

Você pode ver os cookies definidos na IU da documentação em `/docs`:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// note | Nota

Tenha em mente que, como os **navegadores lidam com cookies** de maneira especial e por baixo dos panos, eles **não** permitem facilmente que o **JavaScript** lide com eles.

Se você for na **IU da documentação da API** em `/docs` você poderá ver a **documentação** para cookies das suas *operações de rota*.

Mas mesmo que você **adicione os dados** e clique em "Executar", pelo motivo da IU da documentação trabalhar com **JavaScript**, os cookies não serão enviados, e você verá uma mensagem de **erro** como se você não tivesse escrito nenhum dado.

///

## Proíba Cookies Adicionais { #forbid-extra-cookies }

Em alguns casos especiais (provavelmente não muito comuns), você pode querer **restringir** os cookies que você deseja receber.

Agora a sua API possui o poder de controlar o seu próprio <dfn title="Isso é uma brincadeira, só por precaução. Isso não tem nada a ver com consentimentos de cookies, mas é engraçado que até a API consegue rejeitar os coitados dos cookies. Coma um biscoito. 🍪">consentimento de cookie</dfn>. 🤪🍪

Você pode utilizar a configuração do modelo Pydantic para proibir com `forbid` qualquer campo `extra`:

{* ../../docs_src/cookie_param_models/tutorial002.py hl[10] *}

Se o cliente tentar enviar alguns **cookies extras**, ele receberá uma resposta de **erro**.

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

## Combine Modelos de Parâmetros { #combine-parameter-models }

Você pode combinar vários modelos de parâmetros de cookie com parâmetros de cookie individuais e dependências. Cada modelo é extraído e validado de forma independente, conforme explicado para [modelos de parâmetros de query](query-param-models.md#combine-parameter-models).

A configuração `extra` de cada modelo se aplica a todos os parâmetros de cookie, incluindo os declarados em outros modelos ou dependências. Com `extra="forbid"`, qualquer cookie fora desse modelo é rejeitado. Com `extra="allow"`, esses cookies são incluídos como campos extras do modelo.

## Modelos Opcionais de Parâmetros de Cookie { #optional-cookie-parameter-models }

Declare um modelo de parâmetros de cookie com `| None` e um valor padrão de `None` para tornar o grupo opcional.

{* ../../docs_src/cookie_param_models/tutorial003.py hl[15] *}

Se nem `theme` nem `locale` forem enviados, `preferences` será `None`. Se qualquer um deles for enviado, o FastAPI validará o modelo e exigirá ambos os campos.

As mesmas regras para valores padrão, campos extras e OpenAPI se aplicam, assim como nos [modelos opcionais de parâmetros de query](query-param-models.md#optional-query-parameter-models).

## Resumo { #summary }

Você consegue utilizar **modelos Pydantic** para declarar <dfn title="Coma um último biscoito antes de você ir embora. 🍪">**cookies**</dfn> no **FastAPI**. 😎
