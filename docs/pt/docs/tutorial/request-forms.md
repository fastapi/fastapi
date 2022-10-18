# Dados de Formulário

Quando você precisar receber campos de um formulário ao invés de JSON, você pode usar o `Form`.

!!! info "Informação"
    Para usar o `Form`, primeiro instale <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    E.g. `pip install python-multipart`.

## Importando `Form`

Importando `Form` pela `fastapi`:

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## Definindo um parâmetro `Form`

Crie parâmetros `Form` da mesma maneira que você criaria para `Body` ou `Query`:

```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

Por exemplo, em uma das maneiras em que a especificação OAuth2 pode ser usada (chamada de "password flow") é obrigatório enviar um `username` e uma `password` como campos de formulário.

A <abbr title="specification">especificação</abbr> requer que os campos sejam exatamente nomeados como `username` e `password`, e que sejam enviados como campos de formulário, não como JSON.

Com o `Form` você pode declarar as mesmas configurações que `Body` (e `Query`, `Path`, `Cookie`), incluindo validações, exemplos, alias (e.g. `user-name` ao invés de `username`), etc.

!!! info "Informação"
    `Form` é uma classe que herda diretamente de `Body`.

!!! tip "Dica"
    Para declarar corpos de formulário, você deve usar explicitamente o `Form`, porque sem ele os parâmetros serão interpretados como parâmetros de busca (query) ou parâmetros de corpo (JSON).

## Sobre "Campos de Formulário"

A maneira que os formulários HTTP (`<form></form>`) enviam dados para o servidor normalmente usa uma codificação especial para aqueles dados, diferente do JSON.

**FastAPI** irá garantir a leitura dos dados do lugar certo ao invés de um JSON.

!!! note "Detalhes Técnicos"
    Dados de formulário são normalmente codificados usando o "media type" `application/x-www-form-urlencoded`.

    Mas quando o formulário possui arquivos, ele é codificado como `multipart/form-data`. Você vai ler mais sobre mexer com arquivos no próximo capítulo.

    Se você quer ler mais sobre essas codificações e campos de formulário, dirija-se até a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> documentação da web para <code>POST</code></a>.

!!! warning "Aviso"
    Você pode declarar múltiplos parâmetros `Form` em uma operação de caminho (path), mas você não pode declarar junto de um campo `Body` que espera receber um JSON, pois a requisição vai ter o corpo codificado usando `application/x-www-form-urlencoded` ao invés de  `application/json`.

    Isso não é uma limitação da **FastAPI**, faz parte do protocolo HTTP.

## Recapitulando

Use `Form` para declarar dados de formulário como parâmetros de entrada.
