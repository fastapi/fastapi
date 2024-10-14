# Cookies de Resposta

## Usando um parâmetro `Response`

Você pode declarar um parâmetro do tipo `Response` na sua *função de operação de rota*.

E então você pode definir cookies nesse objeto de resposta *temporário*.

```Python hl_lines="1  8-9"
{!../../docs_src/response_cookies/tutorial002.py!}
```

Em seguida, você pode retornar qualquer objeto que precise, como normalmente faria (um `dict`, um modelo de banco de dados, etc).

E se você declarou um `response_model`, ele ainda será usado para filtrar e converter o objeto que você retornou.

**FastAPI** usará essa resposta *temporária* para extrair os cookies (também os cabeçalhos e código de status) e os colocará na resposta final que contém o valor que você retornou, filtrado por qualquer `response_model`.

Você também pode declarar o parâmetro `Response` em dependências e definir cookies (e cabeçalhos) nelas.

## Retornando uma `Response` diretamente

Você também pode criar cookies ao retornar uma `Response` diretamente no seu código.

Para fazer isso, você pode criar uma resposta como descrito em [Retornando uma Resposta Diretamente](response-directly.md){.internal-link target=_blank}.

Então, defina os cookies nela e a retorne:

```Python hl_lines="10-12"
{!../../docs_src/response_cookies/tutorial001.py!}
```

/// tip | Dica

Lembre-se de que se você retornar uma resposta diretamente em vez de usar o parâmetro `Response`, FastAPI a retornará diretamente.

Portanto, você terá que garantir que seus dados sejam do tipo correto. E.g. será compatível com JSON se você estiver retornando um `JSONResponse`.

E também que você não esteja enviando nenhum dado que deveria ter sido filtrado por um `response_model`.

///

### Mais informações

/// note | "Detalhes Técnicos"

Você também poderia usar `from starlette.responses import Response` ou `from starlette.responses import JSONResponse`.

**FastAPI** fornece as mesmas `starlette.responses` em `fastapi.responses` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria das respostas disponíveis vem diretamente do Starlette.

E como o `Response` pode ser usado frequentemente para definir cabeçalhos e cookies, o **FastAPI** também o fornece em `fastapi.Response`.

///

Para ver todos os parâmetros e opções disponíveis, verifique a <a href="https://www.starlette.io/responses/#set-cookie" class="external-link" target="_blank">documentação no Starlette</a>.
