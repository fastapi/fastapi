# События, отправляемые сервером (SSE) { #server-sent-events-sse }

Вы можете передавать данные потоком клиенту, используя Server-Sent Events (SSE).

Это похоже на [Стриминг JSON Lines](stream-json-lines.md), но использует формат `text/event-stream`, который нативно поддерживается браузерами через [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

/// info | Информация

Добавлено в FastAPI 0.135.0.

///

## Что такое Server-Sent Events? { #what-are-server-sent-events }

SSE — это стандарт для потоковой передачи данных с сервера на клиента по HTTP.

Каждое событие — это небольшой текстовый блок с «полями», такими как `data`, `event`, `id` и `retry`, разделёнными пустыми строками.

Это выглядит так:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE часто используют для стриминга ответов ИИ в чатах, живых уведомлений, логов и наблюдаемости, а также в других случаях, когда сервер «проталкивает» обновления клиенту.

/// tip | Совет

Если вам нужно стримить бинарные данные, например видео или аудио, посмотрите расширенное руководство: [Stream Data](../advanced/stream-data.md).

///

## Стриминг SSE с FastAPI { #stream-sse-with-fastapi }

Чтобы стримить SSE с FastAPI, используйте `yield` в своей функции-обработчике пути и укажите `response_class=EventSourceResponse`.

Импортируйте `EventSourceResponse` из `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Каждый возвращаемый через `yield` элемент кодируется как JSON и отправляется в поле `data:` события SSE.

Если вы объявите тип возврата как `AsyncIterable[Item]`, FastAPI будет использовать его, чтобы выполнить **валидацию**, добавить **документацию** и **сериализовать** данные с помощью Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Совет

Так как Pydantic будет сериализовать это на стороне **Rust**, вы получите значительно более высокую **производительность**, чем если не объявите тип возврата.

///

### Несинхронные функции-обработчики пути { #non-async-path-operation-functions }

Вы также можете использовать обычные функции `def` (без `async`) и применять `yield` тем же образом.

FastAPI проследит, чтобы выполнение прошло корректно и не блокировало цикл событий.

Так как в этом случае функция не async, правильным типом возврата будет `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Без объявленного типа возврата { #no-return-type }

Вы также можете опустить тип возврата. FastAPI использует [`jsonable_encoder`](./encoder.md) для преобразования данных и их отправки.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Если вам нужно задать поля SSE, такие как `event`, `id`, `retry` или `comment`, вы можете возвращать через `yield` объекты `ServerSentEvent` вместо обычных данных.

Импортируйте `ServerSentEvent` из `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

Поле `data` всегда кодируется как JSON. Вы можете передавать любое значение, сериализуемое в JSON, включая Pydantic-модели.

## Необработанные данные { #raw-data }

Если нужно отправлять данные без JSON-кодирования, используйте `raw_data` вместо `data`.

Это полезно для отправки заранее отформатированного текста, строк логов или специальных значений <dfn title="Значение, используемое для обозначения особого условия или состояния">«сентинель»</dfn>, например `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Примечание

`data` и `raw_data` взаимно исключают друг друга. В каждом `ServerSentEvent` можно задать только одно из них.

///

## Возобновление с `Last-Event-ID` { #resuming-with-last-event-id }

Когда браузер переподключается после обрыва соединения, он отправляет последний полученный `id` в HTTP-заголовке `Last-Event-ID`.

Вы можете прочитать его как параметр заголовка и использовать, чтобы возобновить поток с того места, где клиент остановился:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE с POST { #sse-with-post }

SSE работает с любым HTTP-методом, не только с `GET`.

Это полезно для таких протоколов, как [MCP](https://modelcontextprotocol.io), которые стримят SSE по `POST`:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Технические детали { #technical-details }

FastAPI из коробки реализует некоторые лучшие практики для SSE.

- Отправлять комментарий «ping» для поддержания соединения («keep alive») каждые 15 секунд, когда нет сообщений, чтобы предотвратить закрытие соединения некоторыми прокси, как рекомендовано в [HTML specification: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes).
- Устанавливать заголовок `Cache-Control: no-cache`, чтобы предотвратить кэширование потока.
- Устанавливать специальный заголовок `X-Accel-Buffering: no`, чтобы предотвратить буферизацию в некоторых прокси, например Nginx.

Вам не нужно ничего настраивать, это работает из коробки. 🤓
