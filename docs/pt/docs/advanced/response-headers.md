# Cabeçalhos de resposta

## Usando um parâmetro `Response`

Você pode declarar um parâmetro do tipo `Response` na sua *função de operação de rota* (assim como você pode fazer para cookies).

Então você pode definir os cabeçalhos nesse objeto de resposta *temporário*.

```Python hl_lines="1  7-8"
{!../../docs_src/response_headers/tutorial002.py!}
```

Em seguida você pode retornar qualquer objeto que precisar, da maneira que faria normalmente (um `dict`, um modelo de banco de dados, etc.).

Se você declarou um `response_model`, ele ainda será utilizado para filtrar e converter o objeto que você retornou.

**FastAPI** usará essa resposta *temporária* para extrair os cabeçalhos (cookies e código de status também) e os colocará na resposta final que contém o valor que você retornou, filtrado por qualquer `response_model`.

Você também pode declarar o parâmetro `Response` em dependências e definir cabeçalhos (e cookies) nelas.

## Retornar uma `Response` diretamente

Você também pode adicionar cabeçalhos quando retornar uma `Response` diretamente.

Crie uma resposta conforme descrito em [Retornar uma resposta diretamente](response-directly.md){.internal-link target=_blank} e passe os cabeçalhos como um parâmetro adicional:

```Python hl_lines="10-12"
{!../../docs_src/response_headers/tutorial001.py!}
```

/// note | Detalhes técnicos

Você também pode usar `from starlette.responses import Response` ou `from starlette.responses import JSONResponse`.

**FastAPI** fornece as mesmas `starlette.responses` como `fastapi.responses` apenas como uma conveniência para você, desenvolvedor. Mas a maioria das respostas disponíveis vem diretamente do Starlette.

E como a `Response` pode ser usada frequentemente para definir cabeçalhos e cookies, **FastAPI** também a fornece em `fastapi.Response`.

///

## Cabeçalhos personalizados

Tenha em mente que cabeçalhos personalizados proprietários podem ser adicionados <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando o prefixo 'X-'</a>.

Porém, se voce tiver cabeçalhos personalizados que deseja que um cliente no navegador possa ver, você precisa adicioná-los às suas configurações de CORS (saiba mais em [CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md){.internal-link target=_blank}), usando o parâmetro `expose_headers` descrito na <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">documentação de CORS do Starlette</a>.
