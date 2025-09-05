# Продвинутое использование Middleware

В основном руководстве вы узнали, как добавить [пользовательский Middleware](../tutorial/middleware.md){.internal-link target=_blank} в ваше приложение.

А также вы узнали, как обрабатывать [CORS с использованием `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

В этом разделе мы увидим, как использовать другие middleware.

## Добавление ASGI middleware

Так как **FastAPI** основан на Starlette и реализует спецификацию <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>, вы можете использовать любой ASGI middleware.

Для работы middleware не обязательно должны быть созданы специально для FastAPI или Starlette, достаточно того, чтобы они следовали спецификации ASGI.

В общем случае, ASGI middleware представляют собой классы, которые ожидают получение ASGI приложения в качестве первого аргумента.

Таким образом, в документации для сторонних ASGI middleware, скорее всего, будет указано сделать следующее:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Но FastAPI (на самом деле Starlette) предоставляет более простой способ сделать это, обеспечивая правильную обработку ошибок сервера и работу пользовательских обработчиков ошибок.

Для этого используйте `app.add_middleware()` (как в примере для CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` принимает класс middleware в качестве первого аргумента и любые дополнительные аргументы, которые должны быть переданы в middleware.

## Интегрированные middleware

**FastAPI** включает несколько middleware для общих случаев использования, далее мы рассмотрим, как их использовать.

/// note | Технические детали

В следующих примерах вы также можете использовать `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** предоставляет несколько middleware в `fastapi.middleware` исключительно для удобства разработчика. Но большинство доступных middleware поступает непосредственно из Starlette.

///

## `HTTPSRedirectMiddleware`

Обеспечивает, чтобы все входящие запросы были перенаправлены на `https` или `wss`.

Любой входящий запрос на `http` или `ws` будет перенаправлен на защищенную схему.

{* ../../docs_src/advanced_middleware/tutorial001.py hl[2,6] *}

## `TrustedHostMiddleware`

Обеспечивает наличие корректно заданного HTTP-заголовка `Host` во всех входящих запросах для защиты от атак на основе HTTP-заголовка Host.

{* ../../docs_src/advanced_middleware/tutorial002.py hl[2,6:8] *}

Поддерживаются следующие аргументы:

* `allowed_hosts` - список доменных имен, которые разрешены в качестве имен хостов. Разрешены шаблоны доменов, такие как `*.example.com`, для соответствия поддоменам. Для разрешения всех имен хостов можно использовать `allowed_hosts=["*"]` или вовсе не добавлять middleware.

Если входящий запрос не валидируется, отправляется ответ с кодом `400`.

## `GZipMiddleware`

Обрабатывает GZip-ответы для любого запроса, который включает `"gzip"` в HTTP-заголовке `Accept-Encoding`.

Middleware будет обрабатывать как стандартные, так и потоковые HTTP-ответы.

{* ../../docs_src/advanced_middleware/tutorial003.py hl[2,6] *}

Поддерживаются следующие аргументы:

* `minimum_size` - не выполнять GZip сжатие для HTTP-ответов, которые меньше этого минимального размера в байтах. По умолчанию `500`.
* `compresslevel` - используется во время GZip сжатия. Это число в диапазоне от 1 до 9. По умолчанию `9`. Меньшее значение приводит к более быстрому сжатию, но большему размеру файлов, в то время как большее значение приводит к более медленному сжатию, но меньшему размеру файлов.

## Другие middleware

Существует много других ASGI middleware.

Например:

* <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">`ProxyHeadersMiddleware` от Uvicorn</a>
* <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Чтобы увидеть другие доступные middleware, ознакомьтесь с <a href="https://www.starlette.io/middleware/" class="external-link" target="_blank">документацией Starlette по Middleware</a> и <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">списком ASGI Awesome List</a>.
