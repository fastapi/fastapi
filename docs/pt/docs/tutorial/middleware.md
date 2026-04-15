# Middleware { #middleware }

Você pode adicionar middleware à suas aplicações **FastAPI**.

Um "middleware" é uma função que manipula cada **requisição** antes de ser processada por qualquer *operação de rota* específica. E também cada **resposta** antes de retorná-la.

* Ele pega cada **requisição** que chega ao seu aplicativo.
* Ele pode então fazer algo com essa **requisição** ou executar qualquer código necessário.
* Então ele passa a **requisição** para ser processada pelo resto do aplicativo (por alguma *operação de rota*).
* Ele então pega a **resposta** gerada pelo aplicativo (por alguma *operação de rota*).
* Ele pode fazer algo com essa **resposta** ou executar qualquer código necessário.
* Então ele retorna a **resposta**.

/// note | Detalhes Técnicos

Se você tiver dependências com `yield`, o código de saída será executado *depois* do middleware.

Se houver alguma tarefa em segundo plano (abordada na seção [Tarefas em segundo plano](background-tasks.md), que você verá mais adiante), ela será executada *depois* de todo o middleware.

///

## Criar um middleware { #create-a-middleware }

Para criar um middleware, use o decorador `@app.middleware("http")` logo acima de uma função.

A função middleware recebe:

* A `request`.
* Uma função `call_next` que receberá o `request` como um parâmetro.
    * Esta função passará a `request` para a *operação de rota* correspondente.
    * Então ela retorna a `response` gerada pela *operação de rota* correspondente.
* Você pode então modificar ainda mais o `response` antes de retorná-lo.

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | Dica

Tenha em mente que cabeçalhos proprietários personalizados podem ser adicionados [usando o prefixo `X-`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

Mas se você tiver cabeçalhos personalizados desejando que um cliente em um navegador esteja apto a ver, você precisa adicioná-los às suas configurações CORS ([CORS (Cross-Origin Resource Sharing)](cors.md)) usando o parâmetro `expose_headers` documentado na [Documentação CORS da Starlette](https://www.starlette.dev/middleware/#corsmiddleware).

///

/// note | Detalhes Técnicos

Você também pode usar `from starlette.requests import Request`.

**FastAPI** fornece isso como uma conveniência para você, o desenvolvedor. Mas vem diretamente da Starlette.

///

### Antes e depois da `response` { #before-and-after-the-response }

Você pode adicionar código para ser executado com a `request`, antes que qualquer *operação de rota* o receba.

E também depois que a `response` é gerada, antes de retorná-la.

Por exemplo, você pode adicionar um cabeçalho personalizado `X-Process-Time` contendo o tempo em segundos que levou para processar a solicitação e gerar uma resposta:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | Dica

Aqui usamos [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) em vez de `time.time()` porque ele pode ser mais preciso para esses casos de uso. 🤓

///

## Ordem de execução de múltiplos middlewares { #multiple-middleware-execution-order }

Quando você adiciona múltiplos middlewares usando o decorador `@app.middleware()` ou o método `app.add_middleware()`, cada novo middleware envolve a aplicação, formando uma pilha. O último middleware adicionado é o mais externo, e o primeiro é o mais interno.

No caminho da requisição, o middleware mais externo roda primeiro.

No caminho da resposta, ele roda por último.

Por exemplo:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Isso resulta na seguinte ordem de execução:

* **Requisição**: MiddlewareB → MiddlewareA → rota

* **Resposta**: rota → MiddlewareA → MiddlewareB

Esse comportamento de empilhamento garante que os middlewares sejam executados em uma ordem previsível e controlável.

## Outros middlewares { #other-middlewares }

Mais tarde, você pode ler mais sobre outros middlewares no [Guia do usuário avançado: Middleware avançado](../advanced/middleware.md).

Você lerá sobre como manipular <abbr title="Cross-Origin Resource Sharing">CORS</abbr> com um middleware na próxima seção.
