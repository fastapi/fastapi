# Просунуте проміжне програмне забезпечення { #advanced-middleware }

У головному навчальному посібнику ви читали, як додати [Користувацьке проміжне ПЗ](../tutorial/middleware.md){.internal-link target=_blank} до вашого застосунку.

Також ви читали, як обробляти [CORS за допомогою `CORSMiddleware`](../tutorial/cors.md){.internal-link target=_blank}.

У цьому розділі розглянемо, як використовувати інше проміжне ПЗ.

## Додавання middleware ASGI { #adding-asgi-middlewares }

Оскільки **FastAPI** базується на Starlette і реалізує специфікацію <abbr title="Asynchronous Server Gateway Interface - Асинхронний інтерфейс шлюзу сервера">ASGI</abbr>, ви можете використовувати будь-яке проміжне ПЗ ASGI.

Middleware не обов'язково має бути створене саме для FastAPI або Starlette, головне - щоб воно відповідало специфікації ASGI.

Загалом, middleware ASGI — це класи, які очікують отримати застосунок ASGI як перший аргумент.

Тож у документації до сторонніх middleware ASGI вам, імовірно, порадять зробити приблизно так:

```Python
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

Але FastAPI (точніше Starlette) надає простіший спосіб, який гарантує, що внутрішнє middleware обробляє помилки сервера, а користувацькі обробники винятків працюють коректно.

Для цього використовуйте `app.add_middleware()` (як у прикладі для CORS).

```Python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` приймає клас middleware як перший аргумент і будь-які додаткові аргументи, що будуть передані цьому middleware.

## Вбудоване middleware { #integrated-middlewares }

**FastAPI** містить кілька middleware для поширених випадків використання, далі розглянемо, як їх використовувати.

/// note | Технічні деталі

У наступних прикладах ви також можете використовувати `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** надає кілька middleware у `fastapi.middleware` виключно для зручності розробника. Але більшість доступних middleware походять безпосередньо зі Starlette.

///

## `HTTPSRedirectMiddleware` { #httpsredirectmiddleware }

Примушує, щоб усі вхідні запити були або `https`, або `wss`.

Будь-який вхідний запит до `http` або `ws` буде перенаправлено на захищену схему.

{* ../../docs_src/advanced_middleware/tutorial001_py310.py hl[2,6] *}

## `TrustedHostMiddleware` { #trustedhostmiddleware }

Примушує, щоб усі вхідні запити мали коректно встановлений заголовок `Host`, щоб захиститися від атак HTTP Host Header.

{* ../../docs_src/advanced_middleware/tutorial002_py310.py hl[2,6:8] *}

Підтримуються такі аргументи:

- `allowed_hosts` - Список доменних імен, які слід дозволити як імена хостів. Підтримуються домени з «дикою картою», такі як `*.example.com`, для зіставлення піддоменів. Щоб дозволити будь-яке ім'я хоста, або використовуйте `allowed_hosts=["*"]`, або не додавайте це middleware.
- `www_redirect` - Якщо встановлено True, запити до не-www версій дозволених хостів буде перенаправлено до їхніх www-варіантів. Типово `True`.

Якщо вхідний запит не проходить перевірку, буде надіслано відповідь `400`.

## `GZipMiddleware` { #gzipmiddleware }

Обробляє відповіді GZip для будь-якого запиту, що містить `"gzip"` у заголовку `Accept-Encoding`.

Middleware обробляє як стандартні, так і потокові відповіді.

{* ../../docs_src/advanced_middleware/tutorial003_py310.py hl[2,6] *}

Підтримуються такі аргументи:

- `minimum_size` - Не GZip-увати відповіді, менші за цей мінімальний розмір у байтах. Типово `500`.
- `compresslevel` - Використовується під час стиснення GZip. Це ціле число в діапазоні від 1 до 9. Типово `9`. Менше значення дає швидше стиснення, але більший розмір файлів; більше значення дає повільніше стиснення, але менший розмір файлів.

## Інше middleware { #other-middlewares }

Є багато іншого проміжного ПЗ ASGI.

Наприклад:

- <a href="https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py" class="external-link" target="_blank">`ProxyHeadersMiddleware` з Uvicorn</a>
- <a href="https://github.com/florimondmanca/msgpack-asgi" class="external-link" target="_blank">MessagePack</a>

Щоб переглянути інші доступні middleware, ознайомтеся з <a href="https://www.starlette.dev/middleware/" class="external-link" target="_blank">документацією Starlette щодо middleware</a> та <a href="https://github.com/florimondmanca/awesome-asgi" class="external-link" target="_blank">списком ASGI Awesome</a>.
