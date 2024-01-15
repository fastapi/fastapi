# Dados do formulário

Quando você precisar receber campos de formulário ao invés de JSON, você pode usar `Form`.

!!! info "Informação"
    Para usar formulários, primeiro instale <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    Ex: `pip install python-multipart`.

## Importe `Form`

Importe `Form` de `fastapi`:

```Python hl_lines="1"
{!../../../docs_src/request_forms/tutorial001.py!}
```

## Declare parâmetros de `Form`

Crie parâmetros de formulário da mesma forma que você faria para `Body` ou `Query`:

```Python hl_lines="7"
{!../../../docs_src/request_forms/tutorial001.py!}
```

Por exemplo, em uma das maneiras que a especificação OAuth2 pode ser usada (chamada "fluxo de senha"), é necessário enviar um `username` e uma `password` como campos do formulário.

A <abbr title="especificação">spec</abbr> exige que os campos sejam exatamente nomeados como `username` e `password` e sejam enviados como campos de formulário, não JSON.

Com `Form` você pode declarar os mesmos metadados e validação que com `Body` (e `Query`, `Path`, `Cookie`).

!!! info "Informação"
    `Form` é uma classe que herda diretamente de `Body`.

!!! tip "Dica"
    Para declarar corpos de formulário, você precisa usar `Form` explicitamente, porque sem ele os parâmetros seriam interpretados como parâmetros de consulta ou parâmetros de corpo (JSON).

## Sobre "Campos de formulário"

A forma como os formulários HTML (`<form></form>`) enviam os dados para o servidor normalmente usa uma codificação "especial" para esses dados, é diferente do JSON.

O **FastAPI** fará a leitura desses dados no lugar certo em vez de JSON.

!!! note "Detalhes técnicos"
    Os dados dos formulários são normalmente codificados usando o "tipo de mídia" `application/x-www-form-urlencoded`.

     Mas quando o formulário inclui arquivos, ele é codificado como `multipart/form-data`. Você lerá sobre como lidar com arquivos no próximo capítulo.

    Se você quiser ler mais sobre essas codificações e campos de formulário, vá para o <a href="https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs para <code>POST</code></a>.

!!! warning "Aviso"
    Você pode declarar vários parâmetros `Form` em uma *operação de caminho*, mas não pode declarar campos `Body` que espera receber como JSON, pois a solicitação terá o corpo codificado usando `application/x-www- form-urlencoded` em vez de `application/json`.

    Esta não é uma limitação do **FastAPI**, é parte do protocolo HTTP.

## Recapitulando

Use `Form` para declarar os parâmetros de entrada de dados de formulário.
