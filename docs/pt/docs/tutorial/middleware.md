# Middleware

Você pode adicionar middleware à suas aplicações **FastAPI**.

Um "middleware" é uma função que manipula cada **request** antes de ser processada por qualquer *operação de caminho* específica. E também cada **response** antes de retorná-la.

* Ele pega cada **request** que chega ao seu aplicativo.
* Ele pode então fazer algo com essa **request** ou executar qualquer código necessário.
* Então ele passa a **request** para ser processada pelo resto do aplicativo (por alguma *operação de caminho*).
* Ele então pega a **response** gerada pelo aplicativo (por alguma *operação de caminho*).
* Ele pode fazer algo com essa **response** ou executar qualquer código necessário.
* Então ele retorna a **response**.

!!! note "Detalhes técnicos"
    Se você tiver dependências com `yield`, o código de saída será executado *depois* do middleware.

    Se houver alguma tarefa em segundo plano (documentada posteriormente), ela será executada *depois* de todo o middleware.

## Criar um middleware

Para criar um middleware, use o decorador `@app.middleware("http")` logo acima de uma função.

A função middleware recebe:

* A `request`.
* Uma função `call_next` que receberá o `request` como um parâmetro.
    * Esta função passará a `request` para a *operação de caminho* correspondente.
    * Então ela retorna a `response` gerada pela *operação de caminho* correspondente.
* Você pode então modificar ainda mais o `response` antes de retorná-lo.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! tip
    Tenha em mente que cabeçalhos proprietários personalizados podem ser adicionados <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando o prefixo 'X-'</a>.

    Mas se você tiver cabeçalhos personalizados desejando que um cliente em um navegador esteja apto a ver, você precisa adicioná-los às suas configurações CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) usando o parâmetro `expose_headers` documentado em <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Documentos CORS da Starlette</a>.

!!! note "Detalhes técnicos"
    Você também pode usar `from starlette.requests import Request`.

    **FastAPI** fornece isso como uma conveniência para você, o desenvolvedor. Mas vem diretamente da Starlette.

### Antes e depois da `response`

Você pode adicionar código para ser executado com a `request`, antes que qualquer *operação de caminho* o receba.

E também depois que a `response` é gerada, antes de retorná-la.

Por exemplo, você pode adicionar um cabeçalho personalizado `X-Process-Time` contendo o tempo em segundos que levou para processar a solicitação e gerar uma resposta:

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## Outros middlewares

Mais tarde, você pode ler mais sobre outros middlewares no [Guia do usuário avançado: Middleware avançado](../advanced/middleware.md){.internal-link target=_blank}.

Você lerá sobre como manipular <abbr title="Cross-Origin Resource Sharing">CORS</abbr> com um middleware na próxima seção.
