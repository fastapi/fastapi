# Расширенное использование middleware { #advanced-middleware }

В основном руководстве вы читали, как добавить [пользовательское middleware](../tutorial/middleware.md){.internal-link target=_blank} в ваше приложение.

А затем — как работать с [CORS с помощью `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

В этом разделе посмотрим, как использовать другие middleware.

## Добавление ASGI middleware { #adding-asgi-middlewares }

Так как **FastAPI** основан на Starlette и реализует спецификацию <abbr title="Asynchronous Server Gateway Interface – Асинхронный шлюзовой интерфейс сервера">ASGI</abbr>, вы можете использовать любое ASGI middleware.

Middleware не обязательно должно быть сделано специально для FastAPI или Starlette — достаточно, чтобы оно соответствовало спецификации ASGI.

В общем случае ASGI middleware — это классы, которые ожидают получить ASGI‑приложение первым аргументом.

Поэтому в документации к сторонним ASGI middleware, скорее всего, вы увидите что‑то вроде:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Но FastAPI (точнее, Starlette) предоставляет более простой способ, который гарантирует корректную обработку внутренних ошибок сервера и корректную работу пользовательских обработчиков исключений.

Для этого используйте `app.add_middleware()` (как в примере с CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` принимает класс middleware в качестве первого аргумента и любые дополнительные аргументы, которые будут переданы этому middleware.

## Встроенные middleware { #integrated-middlewares }

**FastAPI** включает несколько middleware для распространённых сценариев. Ниже рассмотрим, как их использовать.

/// note | Технические детали

В следующих примерах вы также можете использовать `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** предоставляет несколько middleware в `fastapi.middleware` для удобства разработчика. Но большинство доступных middleware приходит напрямую из Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Гарантирует, что все входящие запросы должны использовать либо `https`, либо `wss`.

Любой входящий запрос по `http` или `ws` будет перенаправлен на безопасную схему.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Гарантирует, что во всех входящих запросах корректно установлен `Host`‑заголовок, чтобы защититься от атак на HTTP‑заголовок Host.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

Поддерживаются следующие аргументы:

- `allowed_hosts` — список доменных имён, которые следует разрешить как имена хостов. Подстановки вида `*.example.com` поддерживаются для сопоставления поддоменов. Чтобы разрешить любой хост, используйте либо `allowed_hosts=["*"]`, либо не добавляйте это middleware.
- `www_redirect` — если установлено в True, запросы к не‑www версиям разрешённых хостов будут перенаправляться на их www‑аналоги. По умолчанию — `True`.

Если входящий запрос не проходит валидацию, будет отправлен ответ `400`.

## `GZipMiddleware` { #gzipmiddleware }

Обрабатывает GZip‑ответы для любых запросов, которые включают `"gzip"` в заголовке `Accept-Encoding`.

Это middleware обрабатывает как обычные, так и потоковые ответы.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

Поддерживаются следующие аргументы:

- `minimum_size` — не сжимать GZip‑ом ответы, размер которых меньше этого минимального значения в байтах. По умолчанию — `500`.
- `compresslevel` — уровень GZip‑сжатия. Целое число от 1 до 9. По умолчанию — `9`. Более низкое значение — быстреее сжатие, но больший размер файла; более высокое значение — более медленное сжатие, но меньший размер файла.

## Другие middleware { #other-middlewares }

Существует много других ASGI middleware.

Например:

- <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">`ProxyHeadersMiddleware` от Uvicorn</a>
- <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Чтобы увидеть другие доступные middleware, посмотрите <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">документацию по middleware в Starlette</a> и <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">список ASGI Awesome</a>.
