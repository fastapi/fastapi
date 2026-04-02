# Eventos Enviados pelo Servidor (SSE) { #server-sent-events-sse }

Você pode transmitir dados para o cliente usando Server-Sent Events (SSE).

Isso é semelhante a [Stream de JSON Lines](stream-json-lines.md), mas usa o formato `text/event-stream`, que é suportado nativamente pelos navegadores com a [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

/// info | Informação

Adicionado no FastAPI 0.135.0.

///

## O que são Server-Sent Events? { #what-are-server-sent-events }

SSE é um padrão para transmitir dados do servidor para o cliente via HTTP.

Cada evento é um pequeno bloco de texto com “campos” como `data`, `event`, `id` e `retry`, separados por linhas em branco.

Fica assim:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE é comumente usado para streaming de chat de IA, notificações em tempo real, logs e observabilidade, e outros casos em que o servidor envia atualizações para o cliente.

/// tip | Dica

Se você quiser transmitir dados binários, por exemplo vídeo ou áudio, veja o guia avançado: [Stream de Dados](../advanced/stream-data.md).

///

## Transmitir SSE com FastAPI { #stream-sse-with-fastapi }

Para transmitir SSE com FastAPI, use `yield` na sua função de operação de rota e defina `response_class=EventSourceResponse`.

Importe `EventSourceResponse` de `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Cada item produzido é codificado como JSON e enviado no campo `data:` de um evento SSE.

Se você declarar o tipo de retorno como `AsyncIterable[Item]`, o FastAPI o usará para validar, documentar e serializar os dados com o Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Dica

Como o Pydantic fará a serialização no lado em **Rust**, você terá um desempenho muito maior do que se não declarar um tipo de retorno.

///

### *Funções de operação de rota* não assíncronas { #non-async-path-operation-functions }

Você também pode usar funções `def` normais (sem `async`) e usar `yield` da mesma forma.

O FastAPI garantirá a execução correta para não bloquear o event loop.

Como, neste caso, a função não é assíncrona, o tipo de retorno adequado seria `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Sem tipo de retorno { #no-return-type }

Você também pode omitir o tipo de retorno. O FastAPI usará o [`jsonable_encoder`](./encoder.md) para converter os dados e enviá-los.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Se você precisar definir campos de SSE como `event`, `id`, `retry` ou `comment`, você pode produzir objetos `ServerSentEvent` em vez de dados simples.

Importe `ServerSentEvent` de `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

O campo `data` é sempre codificado como JSON. Você pode passar qualquer valor que possa ser serializado como JSON, incluindo modelos do Pydantic.

## Dados brutos { #raw-data }

Se você precisar enviar dados sem codificação JSON, use `raw_data` em vez de `data`.

Isto é útil para enviar texto pré-formatado, linhas de log ou valores <dfn title="um valor usado para indicar uma condição ou estado especial">"sentinela"</dfn> especiais como `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Nota

`data` e `raw_data` são mutuamente exclusivos. Você só pode definir um deles em cada `ServerSentEvent`.

///

## Retomando com `Last-Event-ID` { #resuming-with-last-event-id }

Quando um navegador se reconecta após uma queda na conexão, ele envia o último `id` recebido no cabeçalho `Last-Event-ID`.

Você pode lê-lo como um parâmetro de cabeçalho e usá-lo para retomar o stream de onde o cliente parou:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE com POST { #sse-with-post }

SSE funciona com qualquer método HTTP, não apenas `GET`.

Isso é útil para protocolos como o [MCP](https://modelcontextprotocol.io) que fazem stream de SSE via `POST`:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Detalhes Técnicos { #technical-details }

O FastAPI implementa algumas boas práticas de SSE prontas para uso.

- Enviar um comentário de keep alive `ping` a cada 15 segundos quando não houver mensagens, para evitar que alguns proxies fechem a conexão, como sugerido na [especificação HTML: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes).
- Definir o cabeçalho `Cache-Control: no-cache` para evitar o cache do stream.
- Definir o cabeçalho especial `X-Accel-Buffering: no` para evitar buffering em alguns proxies como o Nginx.

Você não precisa fazer nada, isso funciona automaticamente. 🤓
