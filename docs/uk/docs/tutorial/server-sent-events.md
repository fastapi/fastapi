# Події, надіслані сервером (SSE) { #server-sent-events-sse }

Ви можете транслювати дані клієнту за допомогою **Server-Sent Events** (SSE).

Це подібно до [Потік JSON Lines](stream-json-lines.md), але використовує формат `text/event-stream`, який нативно підтримується браузерами через [API `EventSource`](https://developer.mozilla.org/en-US/docs/Web/API/EventSource).

/// info | Інформація

Додано у FastAPI 0.135.0.

///

## Що таке Server-Sent Events { #what-are-server-sent-events }

SSE - це стандарт для трансляції даних із сервера до клієнта по HTTP.

Кожна подія - це невеликий текстовий блок із «полями» на кшталт `data`, `event`, `id` та `retry`, розділений порожніми рядками.

Виглядає так:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE часто використовують для стрімінгу чатів ШІ, живих сповіщень, логів і спостережуваності, а також інших випадків, коли сервер надсилає оновлення клієнту.

/// tip | Порада

Якщо ви хочете транслювати бінарні дані, наприклад відео чи аудіо, перегляньте просунутий посібник: [Потік даних](../advanced/stream-data.md).

///

## Стрімінг SSE у FastAPI { #stream-sse-with-fastapi }

Щоб транслювати SSE з FastAPI, використовуйте `yield` у вашій *функції операції шляху* і встановіть `response_class=EventSourceResponse`.

Імпортуйте `EventSourceResponse` з `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

Кожен елемент, повернений через `yield`, кодується як JSON і надсилається в полі `data:` події SSE.

Якщо ви оголосите тип повернення як `AsyncIterable[Item]`, FastAPI використає його, щоб **перевіряти**, **документувати** і **серіалізувати** дані за допомогою Pydantic.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | Порада

Оскільки Pydantic серіалізує це на боці **Rust**, ви отримаєте значно вищу **продуктивність**, ніж якби не оголошували тип повернення.

///

### Не-async *функції операцій шляху* { #non-async-path-operation-functions }

Ви також можете використовувати звичайні функції `def` (без `async`) і використовувати `yield` так само.

FastAPI подбає про коректне виконання, щоб воно не блокувало цикл подій.

Оскільки в цьому випадку функція не async, коректним типом повернення буде `Iterable[Item]`:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### Без типу повернення { #no-return-type }

Можна також опустити тип повернення. FastAPI використає [`jsonable_encoder`](./encoder.md), щоб конвертувати дані і надіслати їх.

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

Якщо вам потрібно встановити поля SSE, такі як `event`, `id`, `retry` або `comment`, ви можете повертати через `yield` об'єкти `ServerSentEvent` замість звичайних даних.

Імпортуйте `ServerSentEvent` з `fastapi.sse`:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

Поле `data` завжди кодується як JSON. Ви можете передати будь-яке значення, яке можна серіалізувати в JSON, включно з моделями Pydantic.

## Сирі дані { #raw-data }

Якщо потрібно надіслати дані **без** кодування в JSON, використовуйте `raw_data` замість `data`.

Це корисно для надсилання попередньо відформатованого тексту, рядків логів або спеціальних значень <dfn title="Значення, яке використовується для позначення особливої умови або стану">«значення-сторож»</dfn>, як-от `[DONE]`.

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | Примітка

`data` і `raw_data` взаємовиключні. У кожному `ServerSentEvent` ви можете встановити лише одне з них.

///

## Відновлення з `Last-Event-ID` { #resuming-with-last-event-id }

Коли браузер перепідключається після розриву з'єднання, він надсилає останній отриманий `id` у заголовку `Last-Event-ID`.

Ви можете прочитати його як параметр заголовка і використати, щоб відновити потік із місця, де клієнт зупинився:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## SSE з POST { #sse-with-post }

SSE працює з **будь-яким HTTP-методом**, не лише з `GET`.

Це корисно для протоколів на кшталт [MCP](https://modelcontextprotocol.io), які транслюють SSE через `POST`:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## Технічні деталі { #technical-details }

FastAPI реалізує деякі найкращі практики SSE «з коробки».

- Надсилати **коментар «keep alive» `ping`** кожні 15 секунд, коли не було жодного повідомлення, щоб запобігти закриттю з'єднання деякими проксі, як рекомендовано у [Специфікації HTML: Події, надіслані сервером](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes).
- Встановити заголовок `Cache-Control: no-cache`, щоб **запобігти кешуванню** потоку.
- Встановити спеціальний заголовок `X-Accel-Buffering: no`, щоб **запобігти буферизації** у деяких проксі, наприклад Nginx.

Вам не потрібно нічого з цим робити, воно працює «з коробки». 🤓
