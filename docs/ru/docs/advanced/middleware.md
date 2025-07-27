# Продвинутые Middleware

В основном учебнике вы прочитали, как добавить [Custom Middleware](../tutorial/middleware.md){.internal-link target=_blank} в ваше приложение.

Также вы узнали, как обрабатывать [CORS с помощью `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

В этой секции мы рассмотрим, как использовать другие middlewares.

## Добавление ASGI middlewares

Так как **FastAPI** основан на Starlette и реализует спецификацию <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>, вы можете использовать любое ASGI middleware.

Middleware не обязательно должен быть создан для FastAPI или Starlette, чтобы работать, до тех пор, пока он следует спецификации ASGI.

В общем, ASGI middlewares - это классы, которые ожидают получить ASGI приложение в качестве первого аргумента.

Таким образом, в документации для сторонних ASGI middlewares вероятно, вас попросят сделать что-то похожее на:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Но FastAPI (на самом деле Starlette) предоставляет более простой способ сделать это, который гарантирует, что внутренние middleware будут правильно обрабатывать ошибки сервера и пользовательские обработчики исключений.

Для этого используйте `app.add_middleware()` (как в примере для CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` принимает класс middleware в качестве первого аргумента и любые дополнительные аргументы, которые будут переданы в middleware.

## Встроенные middlewares

**FastAPI** включает несколько middlewares для общих случаев использования, дальше мы рассмотрим как их использовать.

/// note | Технические детали

Для следующих примеров вы также могли бы использовать `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** предоставляет несколько middlewares в `fastapi.middleware` просто для вашего удобства, как разработчика. Но большинство доступных middlewares приходят непосредственно из Starlette.

///

## `HTTPSRedirectMiddleware`

Обеспечивает, чтобы все входящие запросы были либо `https`, либо `wss`.

Любой входящий запрос на `http` или `ws` будет перенаправлен на защищённую схему.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware`

Обеспечивает, чтобы все входящие запросы имели правильно установленный заголовок `Host`, чтобы защититься от атак посредством подмены заголовка HTTP Host.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

Поддерживаются следующие аргументы:

* `allowed_hosts` - Список доменных имён, которые должны быть разрешены в качестве имён хоста. Поддерживаются подстановочные домены, такие как `*.example.com`, для совпадения с поддоменами. Чтобы разрешить любое имя хоста, либо используйте `allowed_hosts=["*"]`, либо пропустите middleware.

Если входящий запрос проходит проверку неправильно, то будет отправлен ответ `400`.

## `GZipMiddleware`

Обрабатывает GZip ответы для любого запроса, который включает `"gzip"` в заголовке `Accept-Encoding`.

Middleware обрабатывает как стандартные, так и потоковые ответы.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

Поддерживаются следующие аргументы:

* `minimum_size` - Не использовать GZip для ответов, размер которых меньше этого минимума в байтах. По умолчанию `500`.
* `compresslevel` - Используется во время GZip сжатия. Это целое число в диапазоне от 1 до 9. Значение по умолчанию `9`. Меньшее значение приводит к более быстрому сжатию, но большим размерам файлов, в то время как большее значение приводит к более медленному сжатию, но меньшим размерам файлов.

## Другие middlewares

Существует много других ASGI middlewares.

Например:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">Uvicorn's `ProxyHeadersMiddleware`</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Чтобы увидеть другие доступные middlewares, ознакомьтесь с <a href="https://www.starlette.io/middleware/" class="external-link" target="_blank">документацией по Middlewares от Starlette</a> и <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">ASGI Awesome List</a>.
