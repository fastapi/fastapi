# Server-Sent Events (SSE) { #server-sent-events-sse }

Puedes enviar datos en streaming al cliente usando **Server-Sent Events** (SSE).

Esto es similar a [Stream JSON Lines](stream-json-lines.md), pero usa el formato `text/event-stream`, que los navegadores soportan de forma nativa con la [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

/// info | Información

Añadido en FastAPI 0.135.0.

///

## ¿Qué son los Server-Sent Events? { #what-are-server-sent-events }

SSE es un estándar para hacer streaming de datos desde el servidor al cliente sobre HTTP.

Cada evento es un pequeño bloque de texto con “campos” como `data`, `event`, `id` y `retry`, separados por líneas en blanco.

Se ve así:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE se usa comúnmente para streaming de chat de IA, notificaciones en vivo, logs y observabilidad, y otros casos donde el servidor envía actualizaciones al cliente.

/// tip | Consejo

Si quieres hacer streaming de datos binarios, por ejemplo video o audio, Revisa la guía avanzada: [Stream Data](../advanced/stream-data.md).

///

## Streaming de SSE con FastAPI { #stream-sse-with-fastapi }

Para hacer streaming de SSE con FastAPI, usa `yield` en tu path operation function y establece `response_class=EventSourceResponse`.

import `EventSourceResponse` de `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Cada ítem producido con `yield` se codifica como JSON y se envía en el campo `data:` de un evento SSE.

Si declaras el tipo de retorno como `AsyncIterable[Item]`, FastAPI lo usará para **validar**, **documentar** y **serializar** los datos usando Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Consejo

Como Pydantic lo serializará en el lado de **Rust**, obtendrás un **rendimiento** mucho mayor que si no declaras un tipo de retorno.

///

### No async *path operation functions* { #non-async-path-operation-functions }

También puedes usar funciones `def` normales (sin `async`), y usar `yield` de la misma manera.

FastAPI se asegurará de ejecutarlo correctamente para que no bloquee el event loop.

Como en este caso la función no es async, el tipo de retorno correcto sería `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Sin tipo de retorno { #no-return-type }

También puedes omitir el tipo de retorno. FastAPI usará el [`jsonable_encoder`](./encoder.md) para convertir los datos y enviarlos.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Si necesitas configurar campos SSE como `event`, `id`, `retry` o `comment`, puedes hacer `yield` de objetos `ServerSentEvent` en lugar de datos simples.

import `ServerSentEvent` de `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

El campo `data` siempre se codifica como JSON. Puedes pasar cualquier valor que pueda serializarse como JSON, incluidos modelos de Pydantic.

## Datos sin procesar { #raw-data }

Si necesitas enviar datos **sin** codificarlos a JSON, usa `raw_data` en lugar de `data`.

Esto es útil para enviar texto preformateado, líneas de log, o valores especiales de <dfn title="Un valor usado para indicar una condición o estado especial">"centinela"</dfn> como `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Nota

`data` y `raw_data` son mutuamente excluyentes. Solo puedes establecer uno de ellos en cada `ServerSentEvent`.

///

## Reanudar con `Last-Event-ID` { #resuming-with-last-event-id }

Cuando un navegador se reconecta después de una caída de la conexión, envía el último `id` recibido en el header `Last-Event-ID`.

Puedes leerlo como un parámetro de header y usarlo para reanudar el stream desde donde el cliente se quedó:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE con `POST` { #sse-with-post }

SSE funciona con **cualquier método HTTP**, no solo con `GET`.

Esto es útil para protocolos como [MCP](https://modelcontextprotocol.io) que hacen streaming de SSE sobre `POST`:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Detalles técnicos { #technical-details }

FastAPI implementa algunas mejores prácticas de SSE desde el primer momento.

- Enviar un comentario de **"keep alive" `ping`** cada 15 segundos cuando no ha habido ningún mensaje, para evitar que algunos proxies cierren la conexión, como se sugiere en la [Especificación HTML: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes).
- Configurar el header `Cache-Control: no-cache` para **evitar el almacenamiento en caché** del stream.
- Configurar un header especial `X-Accel-Buffering: no` para **evitar el buffering** en algunos proxies como Nginx.

No tienes que hacer nada, funciona tal cual viene. 🤓
