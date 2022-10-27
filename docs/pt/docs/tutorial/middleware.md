# Middleware

Você pode adicionar middlewares nas suas aplicações **FastAPI**.

Um "middleware" é uma função que trabalha com todas as **requisições (requests)** antes delas serem processadas por qualquer *operação de caminho*. E também com todas as **respostas (responses)** antes delas serem retornadas.

* Ele pega cada **requisição** que chega para sua aplicação.
* Depois, ele pode fazer algo com essa **requisição** ou rodar qualquer código necessário.
* Depois, ele passa a **requisição** para ser processada pelo resto da aplicação (por alguma *operação de caminho*).
* Depois, ele pega a **resposta** gerada pela aplicação (por alguma *operação de caminho*).
* Ele pode fazer algo com essa **resposta** ou rodar qualquer código necessário. 
* Depois ele retorna a **resposta**.

!!! note "Detalhes Técnicos"
    Se você tem dependências com `yield`, o código de saída vai rodar *depois* do middleware.

    Se não existe nenhuma tarefa rodando por trás (documentada depois), eles irão rodar *depois* de todo o middleware.

## Crie um middleware

Para criar um middleware você usa o decorador `@app.middleware("http")` na linha de cima de uma função.

A função middleware recebe:

* A `requisição`.
* Uma função `call_next` que vai receber a `requisição` como um parâmetro.
    * Essa função vai passar a `requisição` para a *operação de caminho* correspondente.
    * Depois ela retorna a `resposta` gerada pela *peração de caminho* correspondente.
* Depois, você pode modificar a `resposta` antes de retorná-la.

```Python hl_lines="8-9  11  14"
{!../../../docs_src/middleware/tutorial001.py!}
```

!!! tip "Dica"
    Tenha em mente que propriedades de cabeçalho customizáveis podem ser adicionadas <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">usando o prefixo 'X-'</a>.

    Mas se você tem cabeçalhos customizados que você deseja que o cliente em um navegador veja, você precisa adicioná-los nas sua configurações do CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) usando o parâmetro `expose_headers` documentado na <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">documentação do CORS do Starlette</a>.

!!! note "Detalhes Técnicos"
    Você também pode usar `from starlette.requests import Request`.

    **FastAPI** providencia isso como uma conveniência para você, o desenvolvedor. Mas isso vem diretamente do Starlette.

### Antes e depois da `resposta`

Você pode adicionar código para ser rodado com a `requisição`, antes de qualquer *operação de caminho* receber ela.

E também depois da `resposta` ser gerada, antes de retorná-la.

Por exemplo, você poderia adicionar um cabeçalho customizado `X-Process-Time` contendo o tempo em segundos que a requisição levou para ser processada e gerar uma resposta: 

```Python hl_lines="10  12-13"
{!../../../docs_src/middleware/tutorial001.py!}
```

## Outros middlewares

Você pode ler mais sobre outros middlewares em [Guia de usuário Avançado: Middlewares Avançados](../advanced/middleware.md){.internal-link target=_blank}.

Você vai ler sobre como tratar <abbr title="Cross-Origin Resource Sharing">o CORS</abbr> com um middleware na próxima seção.