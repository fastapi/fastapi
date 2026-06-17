# Dados do formulário { #form-data }

Quando você precisar receber campos de formulário em vez de JSON, você pode usar `Form`.

/// note | Nota

Para usar formulários, primeiro instale [`python-multipart`](https://github.com/Kludex/python-multipart).

Certifique-se de criar um [ambiente virtual](../virtual-environments.md), ativá-lo e então instalá-lo, por exemplo:

```console
$ pip install python-multipart
```

///

## Importe `Form` { #import-form }

Importe `Form` de `fastapi`:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## Defina parâmetros de `Form` { #define-form-parameters }

Crie parâmetros de formulário da mesma forma que você faria para `Body` ou `Query`:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

Por exemplo, em uma das maneiras que a especificação OAuth2 pode ser usada (chamada "fluxo de senha"), é necessário enviar um `username` e uma `password` como campos do formulário.

A <dfn title="especificação">especificação</dfn> exige que os campos sejam exatamente nomeados como `username` e `password` e sejam enviados como campos de formulário, não JSON.

Com `Form` você pode declarar as mesmas configurações que com `Body` (e `Query`, `Path`, `Cookie`), incluindo validação, exemplos, um alias (por exemplo, `user-name` em vez de `username`), etc.

/// note | Nota

`Form` é uma classe que herda diretamente de `Body`.

///

/// tip | Dica

Para declarar corpos de formulário, você precisa usar `Form` explicitamente, porque sem ele os parâmetros seriam interpretados como parâmetros de consulta ou parâmetros de corpo (JSON).

///

## Sobre "Campos de formulário" { #about-form-fields }

A forma como os formulários HTML (`<form></form>`) enviam os dados para o servidor normalmente usa uma codificação "especial" para esses dados, é diferente do JSON.

O **FastAPI** fará a leitura desses dados no lugar certo em vez de JSON.

/// note | Detalhes Técnicos

Os dados dos formulários são normalmente codificados usando o "media type" `application/x-www-form-urlencoded`.

Mas quando o formulário inclui arquivos, ele é codificado como `multipart/form-data`. Você lerá sobre como lidar com arquivos no próximo capítulo.

Se você quiser ler mais sobre essas codificações e campos de formulário, vá para o [<abbr title="Mozilla Developer Network - Rede de Desenvolvedores da Mozilla">MDN</abbr> web docs para `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).

///

/// warning | Atenção

Você pode declarar vários parâmetros `Form` em uma *operação de rota*, mas não pode declarar campos `Body` que espera receber como JSON, pois a requisição terá o corpo codificado usando `application/x-www-form-urlencoded` em vez de `application/json`.

Isso não é uma limitação do **FastAPI**, é parte do protocolo HTTP.

///

## Recapitulando { #recap }

Use `Form` para declarar os parâmetros de entrada de dados de formulário.
